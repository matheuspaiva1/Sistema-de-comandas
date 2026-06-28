"""
Script orquestrador de carregamento de dados fictícios.
Popula o MongoDB com mais de 100 registros por coleção, garantindo restrições e relacionamentos.
"""

import argparse
import asyncio
from datetime import UTC, datetime, timedelta
import random

import beanie
from faker import Faker
import motor.motor_asyncio

from app.core.config import settings
from app.models import Client, Command, Document, Payment, Product, Table
from app.models.command import CommandStatus
from app.models.item_command import ItemCommand
from app.models.payment import PaymentMethod, PaymentStatus
from app.models.product import CategoryEnum
from app.models.table import TableStatus


fake = Faker("pt_BR")


def utc_now() -> datetime:
    """Retorna a data atual em UTC sem timezone para manter compatibilidade com os modelos existentes."""
    return datetime.now(UTC).replace(tzinfo=None)


async def init_mongo() -> None:
    """Inicializa a conexão com MongoDB e registra os documentos Beanie."""
    print(f"Conectando ao MongoDB em {settings.mongo_url}...")
    client = motor.motor_asyncio.AsyncIOMotorClient(settings.mongo_url)
    database = client[settings.database_name]
    await beanie.init_beanie(
        database=database,
        document_models=[Client, Table, Product, Payment, Command, Document],
    )


async def database_has_data() -> bool:
    """Verifica se o banco já possui dados de domínio."""
    return await Product.count() > 0


async def clean_database() -> None:
    """Limpa todas as coleções de domínio antes de recriar as seeds."""
    print("Limpando dados existentes...")
    await Payment.find_all().delete()
    await Command.find_all().delete()
    await Document.find_all().delete()
    await Product.find_all().delete()
    await Table.find_all().delete()
    await Client.find_all().delete()
    print("Banco limpo.")


async def seed_clients(count: int = 120) -> list[Client]:
    """Cria clientes fictícios."""
    clients = []

    for index in range(count):
        client = Client(
            name=fake.name(),
            phone=fake.phone_number(),
            email=f"{fake.user_name()}_{index}@{fake.free_email_domain()}",
            tax_id=fake.cpf() if random.random() > 0.3 else None,
            created_at=utc_now() - timedelta(days=random.randint(10, 60)),
        )
        await client.insert()
        clients.append(client)

        if (index + 1) % 20 == 0:
            print(f"  {index + 1}/{count} clientes criados")

    return clients


async def seed_tables(count: int = 100) -> list[Table]:
    """Cria mesas no sistema."""
    tables = []
    locations = ["Salão Principal", "Varanda", "Mezanino", "Jardim", "Balcão", "Área VIP"]

    for number in range(1, count + 1):
        table = Table(
            number=number,
            name=f"Mesa {number}",
            seats=random.choice([2, 4, 6, 8, 10]),
            location=random.choice(locations),
            status=random.choice(list(TableStatus)),
        )
        await table.insert()
        tables.append(table)

        if number % 20 == 0:
            print(f"  {number}/{count} mesas criadas")

    return tables


def product_catalog() -> dict[CategoryEnum, list[tuple[str, str, float]]]:
    """Retorna o catálogo base usado para gerar produtos realistas por categoria."""
    return {
        CategoryEnum.BEBIDA: [
            ("Refrigerante Lata", "Refrigerante de 350ml.", 6.0),
            ("Suco Natural", "Suco natural preparado na hora.", 8.5),
            ("Água Mineral", "Água mineral em garrafa de 500ml.", 4.5),
            ("Chá Gelado", "Chá gelado com limão e hortelã.", 7.0),
            ("Café Espresso", "Café espresso com grãos selecionados.", 5.5),
            ("Milkshake", "Milkshake cremoso batido com sorvete.", 18.0),
            ("Vinho Taça", "Taça de vinho seco.", 19.5),
            ("Cerveja Long Neck", "Cerveja lager 330ml.", 11.9),
        ],
        CategoryEnum.PRATO_PRINCIPAL: [
            ("Filé Mignon", "Filé mignon grelhado com acompanhamento.", 68.0),
            ("Salmão Grelhado", "Salmão grelhado com legumes.", 74.0),
            ("Risoto de Cogumelos", "Risoto cremoso com cogumelos frescos.", 52.0),
            ("Lasanha Bolonhesa", "Lasanha com molho de carne e queijo.", 45.0),
            ("Picanha Grelhada", "Picanha grelhada com farofa e fritas.", 85.0),
            ("Strogonoff de Frango", "Strogonoff servido com arroz e batata palha.", 38.0),
        ],
        CategoryEnum.ENTRADA: [
            ("Bruschetta", "Pão italiano com tomate e manjericão.", 18.0),
            ("Bolinho de Bacalhau", "Bolinhos fritos de bacalhau.", 28.0),
            ("Batata Rústica", "Batatas rústicas com molho da casa.", 22.0),
            ("Pastel de Queijo", "Pastéis recheados com queijo.", 16.0),
            ("Dadinho de Tapioca", "Dadinhos de tapioca com melaço.", 24.0),
        ],
        CategoryEnum.SOBREMESA: [
            ("Pudim", "Pudim de leite condensado com caramelo.", 12.0),
            ("Petit Gateau", "Bolo quente de chocolate com sorvete.", 22.0),
            ("Brownie", "Brownie de chocolate com calda.", 16.5),
            ("Mousse", "Mousse cremosa de fruta.", 11.0),
            ("Torta", "Torta doce com massa crocante.", 14.0),
        ],
        CategoryEnum.LANCHE: [
            ("X-Burger", "Hambúrguer com queijo e molho da casa.", 24.0),
            ("Sanduíche de Frango", "Sanduíche com frango grelhado.", 22.0),
            ("Pastel de Carne", "Pastel recheado com carne temperada.", 14.0),
            ("Coxinha", "Coxinha de frango com massa crocante.", 9.0),
            ("Wrap Vegetariano", "Wrap com vegetais e homus.", 20.0),
        ],
        CategoryEnum.OUTRO: [
            ("Couvert", "Cesta de pães artesanais.", 12.0),
            ("Molho Extra", "Porção extra de molho da casa.", 4.0),
            ("Adicional", "Adicional escolhido pelo cliente.", 6.0),
        ],
    }


async def seed_products(count: int = 120) -> list[Product]:
    """Cria produtos fictícios agrupados por categoria."""
    products = []
    catalog = product_catalog()
    categories = list(CategoryEnum)

    for index in range(count):
        category = categories[index % len(categories)]
        base_name, description, base_price = random.choice(catalog[category])
        variation = fake.word().capitalize()
        price = round(max(2.0, base_price + random.uniform(-2.0, 8.0)), 2)
        product = Product(
            name=f"{base_name} {variation}",
            description=f"{description} {fake.sentence(nb_words=8)}",
            category=category,
            price=price,
            active=random.choice([True, True, True, False]),
        )
        await product.insert()
        products.append(product)

        if (index + 1) % 20 == 0:
            print(f"  {index + 1}/{count} produtos criados")

    return products


async def seed_commands(clients: list[Client], tables: list[Table], products: list[Product], count: int = 150) -> list[Command]:
    """Cria comandas associadas a clientes, mesas e itens embutidos."""
    commands = []

    for index in range(count):
        status = random.choice(list(CommandStatus))
        opened_at = fake.date_time_between(start_date="-60d", end_date="now")
        closed_at = None

        if status in [CommandStatus.FECHADA, CommandStatus.CANCELADA]:
            closed_at = opened_at + timedelta(minutes=random.randint(45, 240))

        items = []
        for _ in range(random.randint(1, 6)):
            product = random.choice(products)
            quantity = random.randint(1, 4)
            items.append(
                ItemCommand(
                    product=product,
                    quantity=quantity,
                    unit_price=product.price,
                    observation=fake.sentence(nb_words=6) if random.random() > 0.75 else None,
                )
            )

        command = Command(
            client=random.choice(clients),
            table=random.choice(tables),
            items=items,
            status=status,
            total_amount=round(sum(item.quantity * item.unit_price for item in items), 2),
            opened_at=opened_at,
            closed_at=closed_at,
        )
        await command.insert()
        commands.append(command)

        if (index + 1) % 20 == 0:
            print(f"  {index + 1}/{count} comandas criadas")

    return commands


async def seed_payments(commands: list[Command], minimum_count: int = 120) -> list[Payment]:
    """Cria pagamentos para comandas fechadas, canceladas e alguns casos pendentes."""
    payments = []

    for command in commands:
        if command.status == CommandStatus.FECHADA:
            payment = Payment(
                command=command,
                amount=command.total_amount,
                method=random.choice(list(PaymentMethod)),
                status=PaymentStatus.PAGO,
                paid_at=command.closed_at,
            )
            await payment.insert()
            payments.append(payment)
        elif command.status == CommandStatus.CANCELADA and random.random() > 0.8:
            payment = Payment(
                command=command,
                amount=command.total_amount,
                method=random.choice(list(PaymentMethod)),
                status=PaymentStatus.ESTORNADO,
                paid_at=command.opened_at + timedelta(minutes=10),
            )
            await payment.insert()
            payments.append(payment)

    while len(payments) < minimum_count:
        command = random.choice(commands)
        paid = random.random() > 0.4
        payment = Payment(
            command=command,
            amount=round(command.total_amount * random.choice([0.5, 1.0]), 2),
            method=random.choice(list(PaymentMethod)),
            status=PaymentStatus.PAGO if paid else PaymentStatus.PENDENTE,
            paid_at=command.opened_at + timedelta(minutes=random.randint(10, 180)) if paid else None,
        )
        await payment.insert()
        payments.append(payment)

    print(f"  {len(payments)} pagamentos processados")
    return payments


async def seed_documents(products: list[Product], count: int = 120) -> list[Document]:
    """Cria metadados de documentos associados aos produtos."""
    documents = []
    extensions = [".pdf", ".jpg", ".jpeg", ".png"]
    content_types = {
        ".pdf": "application/pdf",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
    }

    for index in range(count):
        extension = random.choice(extensions)
        product = products[index % len(products)]
        document = Document(
            product=product,
            original_filename=f"{fake.word()}-{product.name.lower().replace(' ', '-')}{extension}",
            content_type=content_types[extension],
            extension=extension,
            size_bytes=random.randint(15_000, 500_000),
            created_at=fake.date_time_between(start_date="-30d", end_date="now"),
        )
        await document.insert()
        documents.append(document)

        if (index + 1) % 20 == 0:
            print(f"  {index + 1}/{count} documentos criados")

    return documents


async def collection_counts() -> dict[str, int]:
    """Retorna o total atual de documentos por coleção."""
    return {
        "clientes": await Client.count(),
        "mesas": await Table.count(),
        "produtos": await Product.count(),
        "comandas": await Command.count(),
        "pagamentos": await Payment.count(),
        "documentos": await Document.count(),
    }


def should_clean(args: argparse.Namespace, has_data: bool) -> bool:
    """Define se a seed deve limpar o banco antes de popular."""
    if args.no_clean:
        return False

    if args.yes or not has_data:
        return True

    print("\nO banco já contém dados!")
    response = input("Deseja limpar todas as coleções e recriar as seeds? (s/n): ").strip().lower()
    return response == "s"


async def main() -> None:
    """Executa a carga completa de dados fictícios."""
    print("Iniciando verificação do banco de dados...")
    await init_mongo()

    has_data = await database_has_data()
    args = parse_args()
    clean = should_clean(args, has_data)

    if has_data and not clean and not args.no_clean:
        print("Operação cancelada.")
        return

    if clean:
        await clean_database()

    random.seed(args.seed)
    Faker.seed(args.seed)

    print("\n> Criando Clientes (mínimo 100)")
    clients = await seed_clients(count=120)

    print("\n> Criando Mesas (mínimo 100)")
    tables = await seed_tables(count=100)

    print("\n> Criando Produtos (mínimo 100)")
    products = await seed_products(count=120)

    print("\n> Criando Comandas (mínimo 100)")
    commands = await seed_commands(clients, tables, products, count=150)

    print("\n> Processando Pagamentos (mínimo 100)")
    await seed_payments(commands, minimum_count=120)

    print("\n> Gerando Documentos (mínimo 100)")
    await seed_documents(products, count=120)

    print("\nResumo final:")
    for name, total in (await collection_counts()).items():
        print(f"  {name}: {total}")

    print("\nBanco de dados MongoDB populado com sucesso!")


def parse_args() -> argparse.Namespace:
    """Lê os argumentos de linha de comando da seed."""
    parser = argparse.ArgumentParser(description="Popula o MongoDB com dados realistas para desenvolvimento.")
    parser.add_argument("--yes", action="store_true", help="Confirma a limpeza do banco sem perguntar.")
    parser.add_argument("--no-clean", action="store_true", help="Mantém os dados existentes e adiciona novos registros.")
    parser.add_argument("--seed", type=int, default=42, help="Semente usada para gerar dados reprodutíveis.")
    return parser.parse_args()


if __name__ == "__main__":
    asyncio.run(main())
