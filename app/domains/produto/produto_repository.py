class ProdutoRepository:
	def insert(self, data: dict) -> dict:
		raise NotImplementedError("ProdutoRepository.insert ainda não foi implementado")

	def list(self, page: int, page_size: int) -> list[dict]:
		raise NotImplementedError("ProdutoRepository.list ainda não foi implementado")

	def get(self, record_id: int) -> dict | None:
		raise NotImplementedError("ProdutoRepository.get ainda não foi implementado")

	def update(self, record_id: int, data: dict) -> dict | None:
		raise NotImplementedError("ProdutoRepository.update ainda não foi implementado")

	def delete(self, record_id: int) -> bool:
		raise NotImplementedError("ProdutoRepository.delete ainda não foi implementado")

	def count(self) -> int:
		raise NotImplementedError("ProdutoRepository.count ainda não foi implementado")

	def vacuum(self, retention_hours: int = 168) -> None:
		raise NotImplementedError("ProdutoRepository.vacuum ainda não foi implementado")

	def iter_batches(self):
		raise NotImplementedError("ProdutoRepository.iter_batches ainda não foi implementado")
