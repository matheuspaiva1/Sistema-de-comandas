import argparse
import asyncio
from datetime import datetime, timedelta
import random
from faker import Faker
import motor.motor_asyncio
import beanie

from app.core.config import settings
from app.models import Client, Table, Product, Payment, Command, Document
from app.models.table import TableStatus
from app.models.product import CategoryEnum
from app.models.command import CommandStatus
from app.models.payment import PaymentMethod, PaymentStatus
from app.models.item_command import ItemCommand


async def clean_database():
    """Limpa todas as coleções do banco de dados antes de iniciar o seed."""
    print("Limpando coleções existentes...")
    await Payment.find_all().delete()
    await Command.find_all().delete()
    await Document.find_all().delete()
    await Product.find_all().delete()
    await Table.find_all().delete()
    await Client.find_all().delete()
    print("Limpeza concluída.")


async def main(clean: bool = True):
    print(f"Conectando ao MongoDB em {settings.mongo_url}...")
    client_db = motor.motor_asyncio.AsyncIOMotorClient(settings.mongo_url)
    db = client_db[settings.database_name]
    await beanie.init_beanie(
        database=db,
        document_models=[Client, Table, Product, Payment, Command, Document],
    )

    if clean:
        await clean_database()

    fake = Faker("pt_BR")
    random.seed(42)
    Faker.seed(42)

    print("Gerando 120 Clientes...")
    clients = []
    for _ in range(120):
        try:
            tax_id = fake.cpf()
        except AttributeError:
            tax_id = f"{random.randint(100, 999)}.{random.randint(100, 999)}.{random.randint(100, 999)}-{random.randint(10, 99)}"

        name = fake.name()
        email_prefix = name.lower().replace(" ", "")
        email = f"{email_prefix}_{random.randint(1000, 9999)}@{fake.free_email_domain()}"

        client_doc = Client(
            name=name,
            phone=fake.phone_number(),
            email=email,
            tax_id=tax_id,
            created_at=datetime.utcnow() - timedelta(days=random.randint(10, 60)),
        )
        await client_doc.insert()
        clients.append(client_doc)

    print("Gerando 100 Mesas...")
    tables = []
    locations = ["Salão Principal", "Varanda", "Terraço", "Mezanino", "Área VIP"]
    for i in range(1, 101):
        status = TableStatus.LIVRE if random.random() > 0.3 else TableStatus.OCUPADA
        table_doc = Table(
            number=i,
            name=f"Mesa {i}",
            seats=random.choice([2, 4, 6, 8]),
            location=random.choice(locations),
            status=status,
        )
        await table_doc.insert()
        tables.append(table_doc)

    print("Gerando 105 Produtos...")
    products_pool = {
        CategoryEnum.BEBIDA: [
            ("Suco Natural de Laranja", "Suco de laranja espremido na hora, 300ml.", 8.50),
            ("Suco de Limão Rústico", "Suco refrescante de limão taiti, 300ml.", 7.90),
            ("Refrigerante Lata", "Refrigerante de 350ml (Coca-Cola, Guaraná).", 6.00),
            ("Água Mineral Sem Gás", "Água mineral natural, garrafa 500ml.", 4.50),
            ("Água Mineral Com Gás", "Água mineral gaseificada, garrafa 500ml.", 5.00),
            ("Cerveja Heineken Long Neck", "Cerveja premium lager 330ml.", 11.90),
            ("Cerveja Artesanal IPA", "Cerveja local IPA forte e lupulada, 500ml.", 22.00),
            ("Caipirinha Clássica", "Caipirinha de cachaça premium, limão e açúcar.", 18.00),
            ("Chopp Caneca", "Chopp gelado direto da torneira, 450ml.", 10.00),
            ("Vinho Tinto Taça", "Taça de vinho tinto seco cabernet sauvignon.", 19.50),
        ],
        CategoryEnum.PRATO_PRINCIPAL: [
            ("Filé Mignon ao Molho Madeira", "Filé mignon grelhado com molho madeira, arroz e purê.", 68.00),
            ("Salmão Grelhado com Alcaparras", "Filé de salmão grelhado, legumes ao vapor e arroz.", 74.00),
            ("Risoto de Cogumelos Shimeji", "Risoto cremoso de arroz arbóreo com cogumelos frescos.", 52.00),
            ("Lasanha Bolonhesa", "Lasanha clássica com massa artesanal, molho de carne e queijo.", 45.00),
            ("Nhoque Rústico ao Sugo", "Nhoque de batata artesanal com molho de tomates frescos.", 39.00),
            ("Picanha Grelhada na Chapa", "Tiras de picanha grelhada com farofa, vinagrete e fritas.", 85.00),
            ("Strogonoff de Frango", "Clássico strogonoff com arroz branco e batata palha.", 38.00),
            ("Parmegiana de Carne", "Filé bovino empanado com molho de tomate e muçarela gratinada.", 59.00),
        ],
        CategoryEnum.ENTRADA: [
            ("Bruschetta de Tomate e Manjericão", "Pão italiano tostado com tomates picados, alho e azeite.", 18.00),
            ("Bolinho de Bacalhau (6 unidades)", "Bolinhos fritos de bacalhau desfiado e batata.", 28.00),
            ("Batata Rústica Especial", "Batatas fritas rústicas com alecrim e maionese da casa.", 22.00),
            ("Pastel de Queijo (4 unidades)", "Pastéis fritos recheados com queijo muçarela derretido.", 16.00),
            ("Provolone à Milanesa", "Cubos de queijo provolone empanados e fritos.", 25.00),
            ("Dadinho de Tapioca", "Dadinhos fritos de tapioca com queijo coalho e melaço.", 24.00),
        ],
        CategoryEnum.SOBREMESA: [
            ("Pudim de Leite Condensado", "Pudim cremoso clássico com calda de caramelo caseira.", 12.00),
            ("Petit Gâteau com Sorvete", "Bolo quente de chocolate com recheio cremoso e sorvete.", 22.00),
            ("Brownie de Chocolate com Nozes", "Brownie denso servido quente com calda de chocolate.", 16.50),
            ("Mousse de Maracujá Cremosa", "Mousse refrescante feita com polpa natural de maracujá.", 11.00),
            ("Torta de Limão Rústica", "Torta com base de biscoito, creme de limão e merengue tostado.", 14.00),
        ],
        CategoryEnum.LANCHE: [
            ("Hambúrguer Gourmet Especial", "Pão brioche, blend bovino 150g, queijo cheddar e bacon.", 32.00),
            ("Cheeseburger Clássico", "Pão brioche, blend bovino 120g e queijo prato derretido.", 24.00),
            ("Misto Quente Especial", "Pão de forma tostado com presunto royale e queijo muçarela.", 14.00),
            ("Sanduíche de Frango Grelhado", "Pão baguete, filé de frango, alface, tomate e maionese verde.", 22.00),
            ("Wrap de Vegetais e Húmus", "Tortilha recheada com abobrinha grelhada, tomate, rúcula e húmus.", 20.00),
        ],
        CategoryEnum.OUTRO: [
            ("Cafezinho Espresso", "Café espresso forte feito com grãos selecionados.", 5.50),
            ("Chá Gelado com Limão", "Chá preto gelado batido com suco de limão e hortelã.", 7.00),
            ("Cesta de Pães do Couvert", "Pães artesanais variados servidos com manteiga de ervas.", 12.00),
        ]
    }

    products = []
    count_prod = 0
    while count_prod < 105:
        for category, items_list in products_pool.items():
            if count_prod >= 105:
                break
            base_item = random.choice(items_list)
            variation = "" if count_prod < len(items_list) * 6 else f" (Variação {count_prod})"
            
            prod_name = f"{base_item[0]}{variation}"
            prod_desc = f"{base_item[1]} {fake.sentence()}"
            prod_price = float(base_item[2] + random.randint(-2, 5))
            if prod_price < 2.0:
                prod_price = 2.0
                
            product_doc = Product(
                name=prod_name,
                description=prod_desc,
                category=category,
                price=prod_price,
                active=random.random() > 0.05,
            )
            await product_doc.insert()
            products.append(product_doc)
            count_prod += 1

    print("Gerando 105 Documentos (metadados de fotos de produtos)...")
    documents = []
    extensions = [".jpg", ".png", ".pdf"]
    content_types = {
        ".jpg": "image/jpeg",
        ".png": "image/png",
        ".pdf": "application/pdf"
    }
    for prod in products:
        ext = random.choice(extensions)
        slug_name = prod.name.lower().replace(" ", "_").replace("(", "").replace(")", "")
        doc = Document(
            product=prod,
            original_filename=f"{slug_name}_foto{ext}",
            content_type=content_types[ext],
            extension=ext,
            size_bytes=random.randint(15000, 500000),
            created_at=datetime.utcnow() - timedelta(days=random.randint(1, 10)),
        )
        await doc.insert()
        documents.append(doc)

    print("Gerando 150 Comandas...")
    commands = []

    for _ in range(150):
        client = random.choice(clients)
        table = random.choice(tables) if random.random() > 0.2 else None
        
        status = random.choice([CommandStatus.ABERTA, CommandStatus.FECHADA, CommandStatus.CANCELADA])
        opened_at = datetime.utcnow() - timedelta(
            days=random.randint(0, 30),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )
        
        closed_at = None
        if status in [CommandStatus.FECHADA, CommandStatus.CANCELADA]:
            closed_at = opened_at + timedelta(
                hours=random.randint(1, 4),
                minutes=random.randint(0, 59)
            )

        items_count = random.randint(1, 6)
        items = []
        for _ in range(items_count):
            prod = random.choice(products)
            qty = random.randint(1, 4)
            items.append(
                ItemCommand(
                    product=prod,
                    quantity=qty,
                    unit_price=prod.price,
                    observation=fake.sentence() if random.random() > 0.7 else None
                )
            )
            
        total_amount = sum(item.quantity * item.unit_price for item in items)
        
        command_doc = Command(
            client=client,
            table=table,
            items=items,
            status=status,
            total_amount=total_amount,
            opened_at=opened_at,
            closed_at=closed_at,
        )
        await command_doc.insert()
        commands.append(command_doc)

    print("Gerando 120 Pagamentos...")
    payments_count = 0

    closed_commands = [c for c in commands if c.status == CommandStatus.FECHADA]
    for cmd in closed_commands:
        method = random.choice([PaymentMethod.CARTAO, PaymentMethod.PIX, PaymentMethod.DINHEIRO])
        paid_at = cmd.closed_at or (cmd.opened_at + timedelta(hours=2))
        
        payment_doc = Payment(
            command=cmd,
            amount=cmd.total_amount,
            method=method,
            status=PaymentStatus.PAGO,
            paid_at=paid_at,
        )
        await payment_doc.insert()
        payments_count += 1

    all_commands = commands.copy()
    while payments_count < 120:
        cmd = random.choice(all_commands)
        if cmd.status == CommandStatus.CANCELADA:
            status = PaymentStatus.ESTORNADO
            amount = cmd.total_amount
            paid_at = cmd.closed_at
        elif cmd.status == CommandStatus.ABERTA:
            status = random.choice([PaymentStatus.PENDENTE, PaymentStatus.PAGO])
            amount = cmd.total_amount * random.choice([0.5, 1.0])
            paid_at = cmd.opened_at + timedelta(minutes=30) if status == PaymentStatus.PAGO else None
        else:
            status = PaymentStatus.PAGO
            amount = cmd.total_amount * 0.5
            paid_at = cmd.closed_at

        method = random.choice([PaymentMethod.CARTAO, PaymentMethod.PIX, PaymentMethod.DINHEIRO])
        
        payment_doc = Payment(
            command=cmd,
            amount=amount,
            method=method,
            status=status,
            paid_at=paid_at,
        )
        await payment_doc.insert()
        payments_count += 1

    print(f"Banco de dados MongoDB populado com sucesso!")
    print(f"Total de Clientes inseridos: {len(clients)}")
    print(f"Total de Mesas inseridas: {len(tables)}")
    print(f"Total de Produtos inseridos: {len(products)}")
    print(f"Total de Documentos (metadados) inseridos: {len(documents)}")
    print(f"Total de Comandas inseridas: {len(commands)}")
    print(f"Total de Pagamentos inseridos: {payments_count}")


def parse_args():
    parser = argparse.ArgumentParser(description="Popula o MongoDB com dados realistas para desenvolvimento.")
    parser.add_argument(
        "--no-clean",
        action="store_true",
        help="Mantém os dados existentes e apenas adiciona novos registros.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    asyncio.run(main(clean=not args.no_clean))
