import unittest

from app.models.document import FileDocument
from app.models.product import Product


class DocumentRelationshipTests(unittest.TestCase):
    def test_product_owns_documents(self) -> None:
        self.assertIn("documents", Product.model_fields)
        self.assertNotIn("product", FileDocument.model_fields)


if __name__ == "__main__":
    unittest.main()
