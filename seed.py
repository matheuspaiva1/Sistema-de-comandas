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
from app.services.storage_service import StorageService


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
    storage = StorageService()

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

    def generate_file_content(ext: str) -> bytes:
        if ext == ".pdf":
            return b"%PDF-1.4\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>\nendobj\n4 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n5 0 obj\n<< /Length 44 >>\nstream\nBT\n/F1 24 Tf\n100 700 Td\n(Documento de Teste) Tj\nET\nendstream\nendobj\nxref\n0 6\n0000000000 65535 f \n0000000009 00000 n \n0000000058 00000 n \n0000000115 00000 n \n0000000238 00000 n \n0000000306 00000 n \ntrailer\n<< /Size 6 /Root 1 0 R >>\nstartxref\n401\n%%EOF\n"
        elif ext == ".png":
            return b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82"
        elif ext == ".jpg":
            return b"\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00\xff\xdb\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t\x08\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f\x14\x1d\x1a\x1f\x1e\x1d\x1a\x1c\x1c $.\' ",#\x1c\x1c(7),01444\x1f\'9=82<.342\xff\xdb\x00C\x01\t\t\t\x0c\x0b\x0c\x18\r\r\x182!\x1c!22222222222222222222222222222222222222222222222222\xff\xc0\x00\x11\x08\x00\x01\x00\x01\x03\x01\"\x00\x02\x11\x01\x03\x11\x01\xff\xc4\x00\x1f\x00\x00\x01\x05\x01\x01\x01\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\xff\xc4\x00\xb5\x10\x00\x02\x01\x03\x03\x02\x04\x03\x05\x05\x04\x04\x00\x00\x01}\x01\x02\x03\x00\x04\x11\x05\x12!1A\x06\x13Qa\x07\"q\x142\x81\x91\xa1\x08#B\xb1\xc1\x15R\xd1\xf0$3br\x82\t\n\x16\x17\x18\x19\x1a%&'()*456789:CDEFGHIJSTUVWXYZcdefghijstuvwxyz\x83\x84\x85\x86\x87\x88\x89\x8a\x92\x93\x94\x95\x96\x97\x98\x99\x9a\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xff\xc4\x00\x1c\x01\x00\x02\x03\x01\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x02\x03\x04\x05\x06\x07\x08\xff\xc4\x00\xda\x11\x00\x02\x01\x02\x04\x04\x03\x04\x07\x05\x04\x04\x00\x01\x02w\x00\x01\x02\x03\x11\x04\x05!1\x06\x12AQ\x07aq\x13\"2\x81\x08\x14B\x91\xa1\xb1\xc1\t#3R\xf0\x15br\xd1\n\x16$4\xe1%\xf1\x17\x18\x19\x1a&'()*56789:CDEFGHIJSTUVWXYZcdefghijstuvwxyz\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x92\x93\x94\x95\x96\x97\x98\x99\x9a\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xff\xda\x00\x0c\x03\x01\x00\x02\x11\x03\x11\x00?\x00\xfd\xfc\xa8\xff\xd9"
        else:
            return f"Documento fictício com extensão {ext}.".encode("utf-8")

    for prod in products:
        ext = random.choice(extensions)
        slug_name = prod.name.lower().replace(" ", "_").replace("(", "").replace(")", "")
        file_content = generate_file_content(ext)
        document = Document(
            product=prod,
            original_filename=f"{slug_name}_foto{ext}",
            content_type=content_types[ext],
            extension=ext,
            size_bytes=len(file_content),
            created_at=datetime.utcnow() - timedelta(days=random.randint(1, 10)),
        )
        await document.insert()
        storage.upload(
            document_id=document.id,
            extension=document.extension,
            data=file_content,
            content_type=document.content_type,
        )
        documents.append(document)

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
