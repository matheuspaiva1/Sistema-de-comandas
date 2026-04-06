import os
import pyarrow as pa
from deltalake import DeltaTable, write_deltalake

class ComandaRepository:
    def __init__(self):
        self.data_dir = os.path.join(os.getcwd(), "data")
        self.table_path = os.path.join(self.data_dir, "comandas")
        self.seq_file = os.path.join(self.data_dir, "comandas.seq")
        
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            
        self._tabela_existe()
        self._sequencia_existe()

    def _tabela_existe(self):
        """Inicializa a tabela Delta se ela não existir ou estiver corrompida."""
        log_dir = os.path.join(self.table_path, "_delta_log")
        if not os.path.exists(log_dir) or not os.listdir(log_dir):
            if not os.path.exists(self.table_path):
                os.makedirs(self.table_path, exist_ok=True)
            schema = pa.schema([
                ("id", pa.int64()),
                ("numero", pa.int64()),
                ("data_abertura", pa.timestamp('us')),
                ("data_fechamento", pa.timestamp('us')),
                ("cliente_id", pa.int64()),
                ("mesa_id", pa.int64()),
                ("status", pa.string()),
                ("valor_total", pa.float64())
            ])

            tabela_vazia = pa.Table.from_batches([], schema=schema)
            write_deltalake(self.table_path, tabela_vazia, mode="append")

    def _sequencia_existe(self):
        """Inicializa o arquivo de sequência se ele não existir."""
        if not os.path.exists(self.seq_file):
            with open(self.seq_file, "w") as f:
                f.write("0")

    def _get_table(self) -> DeltaTable:
        return DeltaTable(self.table_path)

    def _gerar_id(self) -> int:
        """Lê o valor atual do arquivo .seq, incrementa e salva."""
        with open(self.seq_file, "r+") as f:
            current_id = int(f.read().strip())
            new_id = current_id + 1
            f.seek(0)
            f.write(str(new_id))
            f.truncate()
        return new_id

    # --- Métodos de CRUD ---
    
    def insert(self, data: dict) -> dict:
        data["id"] = self._gerar_id()
        table = pa.Table.from_pylist([data])
        write_deltalake(self.table_path, table, mode="append")
        return data

    def list(self, page: int, page_size: int) -> list[dict]:
        dt = self._get_table()
        
        batches = dt.to_pyarrow_dataset().to_batches(batch_size=page_size)
        
        start_index = (page - 1) * page_size
        end_index = start_index + page_size
        
        rows = []
        current_offset = 0
        
        for batch in batches:
            batch_len = batch.num_rows
            next_offset = current_offset + batch_len
            
            if next_offset > start_index:
                local_start = max(0, start_index - current_offset)
                local_end = min(batch_len, end_index - current_offset)
                
                if local_start < local_end:
                    sliced_batch = batch.slice(local_start, local_end - local_start)
                    rows.extend(pa.Table.from_batches([sliced_batch]).to_pylist())
            
            current_offset = next_offset
            if current_offset >= end_index:
                break
                
        return rows

    def get(self, id: int) -> dict | None:
        dt = self._get_table()
        table = dt.to_pyarrow_table(filters=[("id", "=", id)])
        
        if table.num_rows == 0:
            return None
        
        return table.to_pylist()[0]

    def update(self, id: int, data: dict) -> dict | None:
        dt = self._get_table()
        try:
            table = dt.to_pyarrow_table()
            mask = pa.compute.equal(table["id"], id)
            if table.filter(mask).num_rows == 0:
                return None

            columns = {}
            for col_name in table.schema.names:
                col = table[col_name]
                if col_name in data:
                    new_val = data[col_name]
                    new_col_array = pa.array([new_val] * table.num_rows, type=col.type)
                    col = pa.compute.if_else(mask, new_col_array, col)
                columns[col_name] = col

            updated_table = pa.table(columns, schema=table.schema)
            write_deltalake(self.table_path, updated_table, mode="overwrite")

            updated_row = updated_table.filter(mask).to_pylist()[0]
            return updated_row

        except Exception as e:
            print(f"Erro ao atualizar: {e}")
            return None

    def delete(self, id: int) -> bool:
        dt = self._get_table()
        try:
            table = dt.to_pyarrow_table()
            mask = pa.compute.not_equal(table["id"], id)
            filtered_table = table.filter(mask)
            
            if filtered_table.num_rows == table.num_rows:
                return False
            
            write_deltalake(self.table_path, filtered_table, mode="overwrite")
            return True
        except Exception as e:
            print(f"Erro ao deletar: {e}")
            return False

    def count(self) -> int:
        """Contagem da quantidade de registros - lê apenas metadados/estatísticas sem ler colunas de dados"""
        dt = self._get_table()
        return dt.to_pyarrow_table(columns=[]).num_rows

    def vacuum(self, retention_hours: int = 168):
        """Compacta e limpa versões antigas do Delta Lake."""
        dt = self._get_table()
        dt.vacuum(retention_hours=retention_hours, enforce_retention_duration=False)

    def iter_batches(self, batch_size: int = 1000):
        """Itera sobre os lotes da tabela sem carregar tudo na memória."""
        dt = self._get_table()
        return dt.to_pyarrow_dataset().to_batches(batch_size=batch_size)
