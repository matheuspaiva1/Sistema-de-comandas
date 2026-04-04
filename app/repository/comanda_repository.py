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
        """Inicializa a tabela Delta se ela não existir."""
        if not os.path.exists(os.path.join(self.table_path, "_delta_log")):
            schema = pa.schema([
                ("id", pa.int64()),
                ("clientId", pa.int64()),
                ("tableId", pa.int64()),
                ("status", pa.string()),
                ("fullValue", pa.float64())
            ])

            # Cria tabela vazia com o schema
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

    def insert(self, data: dict) -> dict:
        data["id"] = self._gerar_id()
        
        # Valores padrão
        if "status" not in data:
            data["status"] = "aberta"
        if "fullValue" not in data:
            data["fullValue"] = 0.0

        table = pa.Table.from_pylist([data])
        write_deltalake(self.table_path, table, mode="append")
        return data

    def list(self, page: int, page_size: int) -> list[dict]:
        dt = self._get_table()
        table = dt.to_pyarrow_table()
        
        start = (page - 1) * page_size
        paged_table = table.slice(start, page_size) if start < table.num_rows else table.slice(0, 0)
        return paged_table.to_pylist()

    def get(self, id: int) -> dict | None:
        dt = self._get_table()
        table = dt.to_pyarrow_table()
        
        mask = pa.compute.equal(table["id"], id)
        filtered_table = table.filter(mask)
        
        if filtered_table.num_rows == 0:
            return None
        
        return filtered_table.to_pylist()[0]

    def update(self, id: int, data: dict) -> dict | None:
        dt = self._get_table()
        try:
            table = dt.to_pyarrow_table()
            mask = pa.compute.equal(table["id"], id)
            if table.filter(mask).num_rows == 0:
                return None
            
            df = table.to_pandas()
            for key, value in data.items():
                if key in df.columns:
                    df.loc[df["id"] == id, key] = value
            
            updated_table = pa.Table.from_pandas(df, preserve_index=False)
            write_deltalake(self.table_path, updated_table, mode="overwrite")
            
            updated_row = df[df["id"] == id].to_dict('records')[0]
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
        dt = self._get_table()
        return dt.to_pyarrow_table().num_rows

    def vacuum(self, retention_hours: int = 168):
        """Compacta e limpa versões antigas do Delta Lake."""
        dt = self._get_table()
        dt.vacuum(retention_hours=retention_hours, enforce_retention_duration=False)

    def iter_batches(self):
        """Itera sobre os lotes da tabela."""
        dt = self._get_table()
        return dt.to_pyarrow_table().to_batches()
