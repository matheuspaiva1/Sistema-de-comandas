import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from faker import Faker
from app.domains.produto.produto_service import create_product
import random

fake = Faker("pt_BR")

def run():
    for _ in range(1000):
        create_product({
            "name": fake.word().capitalize(),
            "description": fake.sentence(nb_words=6),
            "price": round(random.uniform(5, 200), 2),
            "active": fake.boolean()
        })

    print("1000 Produtos criados com sucesso!")

if __name__ == "__main__":
    run()