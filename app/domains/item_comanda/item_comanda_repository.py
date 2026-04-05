import os
import pyarrow as pa
from deltalake import DeltaTable, write_deltalake

class ItemComandaRepository:
    def __init__(self):
        self.data_dir = os.path.join(os.getcwd(), "data")
        self.table_path = os.path.join(self.data_dir, "item_comandas")
        self.seq_file = os.path.join(self.data_dir, "item_comandas.seq")
        
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            
        self._tabela_existe()
        self._sequencia_existe()

    def _tabela_existe(self):
        """Inicializa a tabela Delta se ela não existir."""
        if not os.path.exists(os.path.join(self.table_path, "_delta_log")):
            schema = pa.schema([
                ("id", pa.int64()),
                ("comanda_id", pa.int64()),
                ("produto_id", pa.int64()),
                ("quantidade", pa.int64()),
                ("valor_unitario", pa.decimal(10, 2))
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

    # ---
    
    def insert(self, data: dict) -> dict:
        data["id"] = self._gerar_id()
        
        table = pa.Table.from_pylist([data])
        write_deltalake(self.table_path, table, mode="append")
        return data

    def get(self, record_id: int) -> dict | None:
        dt = self._get_table()
        table = dt.to_pyarrow_table()
        
        mask = pa.compute.equal(table["id"], record_id)
        filtered_table = table.filter(mask)
        
        if filtered_table.num_rows == 0:
            return None
        
        return filtered_table.to_pylist()[0]

    def list(self, page: int, page_size: int) -> list[dict]:
        dt = self._get_table()
        table = dt.to_pyarrow_table()

        start = (page - 1) * page_size
        paged_table = table.slice(start, page_size) if start < table.num_rows else table.slice(0, 0)
        return paged_table.to_pylist()
        

    def update(self, record_id: int, data: dict) -> dict | None:
        dt = self._get_table()
        
        try:
            table = dt.to_pyarrow_table()
            mask = pa.compute.equal(table["id"], record_id)
            
            if table.filter(mask).num_rows == 0:
                return None

            df = table.to_pandas()
            
            for key, value in data.items():
                if key in df.columns:
                    df.loc[df["id"] == record_id, key] = value

            updated_table = pa.Table.from_pandas(df, preserve_index=False)
            write_deltalake(self.table_path, updated_table, mode="overwrite")
            
            updated_row = df[df["id"] == record_id].to_dict('records')  [0]
            return updated_row

        except Exception as e:
            print(f"Erro ao atualizar item da comanda: {e}")
            return None
            
    def delete(self, record_id: int) -> bool:
        dt = self._get_table()
        
        try:
            table = dt.to_pyarrow_table()
            mask = pa.compute.equal(table["id"], record_id)
            filtered_table = table.filter(mask)

            if filtered_table.num_rows == table.num_rows:
                return False

            df = table.to_pandas()
            df = df[df["id"] != record_id]
            updated_table = pa.Table.from_pandas(df, preserve_index=False)
            write_deltalake(self.table_path, updated_table, mode="overwrite")
            return True

        except Exception as e:
            print(f"Erro ao deletar item da comanda: {e}")
            return False

    def count(self, comanda_id: int | None = None) -> int:
        dt = self._get_table()
        return dt.to_pyarrow_table().num_rows

    def vacuum(self, retention_hours: int = 168) -> None:
        dt = self._get_table()
        dt.vacuum(retention_hours=retention_hours, enforce_retention_duration=True)

    def iter_batches(self):
        dt = self._get_table()
        return dt.to_pyarrow_table().iter_batches()
