import os

import pyarrow as pa
from deltalake import DeltaTable, write_deltalake

class ProdutoRepository:
	def __init__(self):
		self.data_dir = os.path.join(os.getcwd(), "data")
		self.table_path = os.path.join(self.data_dir, "produtos")
		self.seq_file = os.path.join(self.data_dir, "produtos.seq")

		if not os.path.exists(self.data_dir):
			os.makedirs(self.data_dir)

		self._garantir_tabela()
		self._garantir_sequencia()

	def _garantir_tabela(self):
		"""Inicializa a tabela Delta se ela não existir ou estiver corrompida."""
		log_dir = os.path.join(self.table_path, "_delta_log")
		if not os.path.exists(log_dir) or not os.listdir(log_dir):
			if not os.path.exists(self.table_path):
				os.makedirs(self.table_path, exist_ok=True)
			schema = pa.schema(
				[
					("id", pa.int64()),
					("name", pa.string()),
					("description", pa.string()),
					("price", pa.float64()),
					("active", pa.bool_()),
				]
			)
			tabela_vazia = pa.Table.from_batches([], schema=schema)
			write_deltalake(self.table_path, tabela_vazia, mode="append")

	def _garantir_sequencia(self):
		if not os.path.exists(self.seq_file):
			with open(self.seq_file, "w", encoding="utf-8") as file:
				file.write("0")

	def _get_table(self) -> DeltaTable:
		return DeltaTable(self.table_path)

	def _gerar_id(self) -> int:
		with open(self.seq_file, "r+", encoding="utf-8") as file:
			current_id = int(file.read().strip())
			new_id = current_id + 1
			file.seek(0)
			file.write(str(new_id))
			file.truncate()
		return new_id

	def insert(self, data: dict) -> dict:
		payload = {
			"id": self._gerar_id(),
			"name": data["name"],
			"description": data["description"],
			"price": float(data["price"]),
			"active": bool(data["active"]),
		}

		table = pa.Table.from_pylist([payload])
		write_deltalake(self.table_path, table, mode="append")
		return payload

	def list(self, page: int, page_size: int) -> list[dict]:
		dt = self._get_table()
		table = dt.to_pyarrow_table()

		start = (page - 1) * page_size
		paged_table = (
			table.slice(start, page_size)
			if start < table.num_rows
			else table.slice(0, 0)
		)
		return paged_table.to_pylist()

	def get(self, record_id: int) -> dict | None:
		dt = self._get_table()
		table = dt.to_pyarrow_table()

		mask = pa.compute.equal(table["id"], record_id)
		filtered_table = table.filter(mask)
		if filtered_table.num_rows == 0:
			return None
		return filtered_table.to_pylist()[0]

	def update(self, record_id: int, data: dict) -> dict | None:
		dt = self._get_table()

		try:
			table = dt.to_pyarrow_table()
			mask = pa.compute.equal(table["id"], record_id)
			if table.filter(mask).num_rows == 0:
				return None

			dataframe = table.to_pandas()

			if "name" in data:
				dataframe.loc[dataframe["id"] == record_id, "name"] = data["name"]
			if "description" in data:
				dataframe.loc[dataframe["id"] == record_id, "description"] = data[
					"description"
				]
			if "price" in data:
				dataframe.loc[dataframe["id"] == record_id, "price"] = float(data["price"])
			if "active" in data:
				dataframe.loc[dataframe["id"] == record_id, "active"] = bool(data["active"])

			updated_table = pa.Table.from_pandas(dataframe, preserve_index=False)
			write_deltalake(self.table_path, updated_table, mode="overwrite")

			updated_row = dataframe[dataframe["id"] == record_id].to_dict("records")
			return updated_row[0] if updated_row else None
		except Exception as error:
			print(f"Erro ao atualizar produto: {error}")
			return None

	def delete(self, record_id: int) -> bool:
		dt = self._get_table()

		try:
			table = dt.to_pyarrow_table()
			mask = pa.compute.not_equal(table["id"], record_id)
			filtered_table = table.filter(mask)

			if filtered_table.num_rows == table.num_rows:
				return False

			write_deltalake(self.table_path, filtered_table, mode="overwrite")
			return True
		except Exception as error:
			print(f"Erro ao remover produto: {error}")
			return False

	def count(self) -> int:
		dt = self._get_table()
		return dt.to_pyarrow_table().num_rows

	def vacuum(self, retention_hours: int = 168) -> None:
		dt = self._get_table()
		dt.vacuum(retention_hours=retention_hours, enforce_retention_duration=False)

	def iter_batches(self):
		dt = self._get_table()
		return dt.to_pyarrow_table().to_batches()
