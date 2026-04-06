from faker import Faker
from app.services import comanda_service
import random

fake = Faker("pt_BR")

def run():
    for _ in range(1000):
        comanda_service.create_commands({
            "clientId": random.randint(1, 100),
            "tableId": random.randint(1, 50),
            "status": fake.random_element(elements=("aberta", "fechada", "paga")),
            "fullValue": round(random.uniform(10, 500), 2)
        })

    print("1000 Comandas criadas com sucesso!")

if __name__ == "__main__":
    run()