"""
Script de carregamento de dados realistas usando Faker com localização pt_BR.

Popula o banco com 100+ produtos, documentos associados a alguns produtos, e dados consistentes e significativos.

Uso:
    python scripts/seed.py

O script lê a DATABASE_URL do arquivo .env e popula automaticamente.
"""

import asyncio
import random
import sys
from pathlib import Path

from faker import Faker
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

app_path = Path(__file__).parent.parent
sys.path.insert(0, str(app_path))

from app.core.config import settings
from app.models.product import Product, CategoryEnum
from app.models.document import Document
from app.core.database import AsyncSessionLocal

fake = Faker("pt_BR")

async def seed_products(session: AsyncSession, count: int = 120) -> list[Product]:
    """
    Cria produtos com categorias variadas.
    
    Args:
        session: Sessão assíncrona do banco
        count: Quantidade de produtos a criar
        
    Returns:
        Lista de produtos criados
    """
    
    produtos = []
    categorias = list(CategoryEnum)
    
    for i in range(count):
        categoria = categorias[i % len(categorias)]
        
        if categoria == CategoryEnum.BEBIDA:
            preco = round(fake.pydecimal(left_digits=3, right_digits=2, positive=True, min_value=3, max_value=30), 2)
        elif categoria == CategoryEnum.PRATO_PRINCIPAL:
            preco = round(fake.pydecimal(left_digits=3, right_digits=2, positive=True, min_value=25, max_value=150), 2)
        elif categoria == CategoryEnum.ENTRADA:
            preco = round(fake.pydecimal(left_digits=3, right_digits=2, positive=True, min_value=15, max_value=50), 2)
        elif categoria == CategoryEnum.SOBREMESA:
            preco = round(fake.pydecimal(left_digits=3, right_digits=2, positive=True, min_value=10, max_value=40), 2)
        else: 
            preco = round(fake.pydecimal(left_digits=3, right_digits=2, positive=True, min_value=8, max_value=35), 2)
        
        if categoria == CategoryEnum.BEBIDA:
            nome_base = [
                "Refrigerante", "Suco", "Água", "Chá gelado", "Café", 
                "Milkshake", "Smoothie", "Bebida energética", "Vinho", "Cerveja"
            ]
            sabor = fake.word()
            nome = f"{random.choice(nome_base)} {sabor.capitalize()}"
        elif categoria == CategoryEnum.PRATO_PRINCIPAL:
            nome_base = [
                "Prato de", "Filé", "Peito de", "Arroz com", "Macarrão à", "Risoto de"
            ]
            ingrediente = ["Frango", "Carne", "Peixe", "Camarão", "Cogumelo", "Brócolis"]
            nome = f"{random.choice(nome_base)} {random.choice(ingrediente)}"
        elif categoria == CategoryEnum.ENTRADA:
            nome_base = [
                "Entrada de", "Tábua de", "Pão", "Patê de", "Salada de"
            ]
            ingrediente = ["Queijo", "Presunto", "Vegetais", "Tomate", "Alface", "Frutos do mar"]
            nome = f"{random.choice(nome_base)} {random.choice(ingrediente)}"
        elif categoria == CategoryEnum.SOBREMESA:
            nome_base = [
                "Bolo de", "Mousse de", "Torta de", "Pudim de", "Sorvete de", "Doce de"
            ]
            sabor_sobremesa = ["Chocolate", "Morango", "Maracujá", "Limão", "Coco", "Pistache"]
            nome = f"{random.choice(nome_base)} {random.choice(sabor_sobremesa)}"
        else:
            nome_base = [
                "X-Burger", "Sanduíche de", "Pastel de", "Coxinha de", "Croquete de"
            ]
            ingrediente_lanche = ["Queijo", "Frango", "Carne", "Calabresa", "Palmito"]
            nome = f"{random.choice(nome_base)} {random.choice(ingrediente_lanche)}"
        
        produto = Product(
            name=nome,
            description=fake.sentence(nb_words=8),
            category=categoria,
            price=float(preco),
            active=random.choice([True, True, True, False]) 
        )
        
        session.add(produto)
        produtos.append(produto)
        
        if (i + 1) % 20 == 0:
            print(f"  ✓ {i + 1}/{count} produtos criados")
    
    await session.commit()
    
    for p in produtos:
        await session.refresh(p)
    
    return produtos


async def seed_documents(session: AsyncSession, produtos: list[Product], count_per_product: int = 1) -> None:
    """
    Cria documentos associados aos produtos.
    
    Args:
        session: Sessão assíncrona do banco
        produtos: Lista de produtos
        count_per_product: Quantidade de documentos por produto (aleatória)
    """
    
    upload_dir = Path(settings.upload_dir)
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    extensoes_permitidas = [".pdf", ".jpg", ".jpeg", ".png"]
    total_docs_created = 0
    
    for produto in produtos:
        if random.random() > 0.6: 
            continue
        
        num_docs = random.randint(1, 3)
        
        for _ in range(num_docs):
            extensao = random.choice(extensoes_permitidas)
            
            doc_types = [
                f"Foto-do-produto-{fake.word()}{extensao}",
                f"Cardápio-{fake.word()}{extensao}",
                f"Receita-{fake.word()}{extensao}",
                f"Certificado-{fake.word()}{extensao}",
                f"Manual-{fake.word()}{extensao}",
            ]
            
            filename = random.choice(doc_types)
            
            if extensao == ".pdf":
                file_content = b"%PDF-1.4\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>\nendobj\n4 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n5 0 obj\n<< /Length 44 >>\nstream\nBT\n/F1 24 Tf\n100 700 Td\n(Documento de Teste) Tj\nET\nendstream\nendobj\nxref\n0 6\n0000000000 65535 f \n0000000009 00000 n \n0000000058 00000 n \n0000000115 00000 n \n0000000238 00000 n \n0000000306 00000 n \ntrailer\n<< /Size 6 /Root 1 0 R >>\nstartxref\n401\n%%EOF\n"
            elif extensao == ".png":
                file_content = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82'
            elif extensao == ".jpg":
                file_content = b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00\xff\xdb\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t\x08\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f\x14\x1d\x1a\x1f\x1e\x1d\x1a\x1c\x1c $.\' ",#\x1c\x1c(7),01444\x1f\'9=82<.342\xff\xdb\x00C\x01\t\t\t\x0c\x0b\x0c\x18\r\r\x182!\x1c!22222222222222222222222222222222222222222222222222\xff\xc0\x00\x11\x08\x00\x01\x00\x01\x03\x01"\x00\x02\x11\x01\x03\x11\x01\xff\xc4\x00\x1f\x00\x00\x01\x05\x01\x01\x01\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\xff\xc4\x00\xb5\x10\x00\x02\x01\x03\x03\x02\x04\x03\x05\x05\x04\x04\x00\x00\x01}\x01\x02\x03\x00\x04\x11\x05\x12!1A\x06\x13Qa\x07"q\x142\x81\x91\xa1\x08#B\xb1\xc1\x15R\xd1\xf0$3br\x82\t\n\x16\x17\x18\x19\x1a%&\'()*456789:CDEFGHIJSTUVWXYZcdefghijstuvwxyz\x83\x84\x85\x86\x87\x88\x89\x8a\x92\x93\x94\x95\x96\x97\x98\x99\x9a\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xff\xc4\x00\x1c\x01\x00\x02\x03\x01\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x02\x03\x04\x05\x06\x07\x08\xff\xc4\x00\xda\x11\x00\x02\x01\x02\x04\x04\x03\x04\x07\x05\x04\x04\x00\x01\x02w\x00\x01\x02\x03\x11\x04\x05!1\x06\x12AQ\x07aq\x13"2\x81\x08\x14B\x91\xa1\xb1\xc1\t#3R\xf0\x15br\xd1\n\x16$4\xe1%\xf1\x17\x18\x19\x1a&\'()*56789:CDEFGHIJSTUVWXYZcdefghijstuvwxyz\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x92\x93\x94\x95\x96\x97\x98\x99\x9a\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xff\xda\x00\x0c\x03\x01\x00\x02\x11\x03\x11\x00?\x00\xfd\xfc\xa8\xff\xd9'
            else:
                file_content = f"Este é um documento de mock gerado pelo seed e salvo ficticiamente com a extensão {extensao}.".encode("utf-8")
            
            mime_types = {
                ".pdf": "application/pdf",
                ".jpg": "image/jpeg",
                ".jpeg": "image/jpeg",
                ".png": "image/png",
            }
            
            document = Document(
                product_id=produto.id,
                original_filename=filename,
                content_type=mime_types.get(extensao, "application/octet-stream"),
                extension=extensao,
                size_bytes=len(file_content),
                created_at=fake.date_time_between(start_date="-30d")
            )
            
            session.add(document)
            total_docs_created += 1
            
            file_path = upload_dir / f"{document.id}{extensao}"
            file_path.write_bytes(file_content)
    
    await session.commit()

async def main():
    """Função principal para seed."""
    
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Product))
        existing_products = result.scalars().all()
        
        if len(existing_products) > 0:
            print(f"\nBanco já contém {len(existing_products)} produtos!")
            response = input("Deseja limpar e recriar? (s/n): ").lower()
            
            if response == "s":
                print("Limpando dados existentes...")
                
                await session.execute(delete(Document))
                await session.execute(delete(Product))
                
                await session.commit()
                print("Dados existentes removidos")
            else:
                print("Operação cancelada")
                return
    
    async with AsyncSessionLocal() as session:
        produtos = await seed_products(session, count=120)
    
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Product))
        produtos = result.scalars().all()
        
        await seed_documents(session, produtos, count_per_product=1)
    
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Product))
        total_products = len(result.scalars().all())

        result = await session.execute(select(Document))
        total_documents = len(result.scalars().all())

    print("\nSeed concluído com sucesso!")
    print(f"  Produtos:   {total_products}")
    print(f"  Documentos: {total_documents}")

if __name__ == "__main__":
    asyncio.run(main())
