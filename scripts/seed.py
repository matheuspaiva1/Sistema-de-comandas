from faker import Faker
from app.domains.comanda import comanda_service
from app.domains.comanda.comanda_schema import CreateComandaSchema
import random

fake = Faker("pt_BR")

def run():
    for _ in range(1000):
        itens_aleatorios = [random.randint(1, 10) for _ in range(random.randint(1, 5))]
        
        schema = CreateComandaSchema(
            cliente_id=random.randint(1, 20),
            mesa_id=random.randint(1, 15),
            itens=itens_aleatorios
        )
        
        comanda_service.create_commands(schema)

    print("1000 Comandas criadas com sucesso!")

if __name__ == "__main__":
    run()
