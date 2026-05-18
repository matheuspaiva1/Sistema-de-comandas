"""
Script orquestrador de carregamento de dados fictícios.
Popula o banco com mais de 100 registros por entidade, garantindo as restrições e relacionamentos.
"""

import asyncio
import sys
from pathlib import Path

from sqlalchemy import delete
from sqlmodel import select

app_path = Path(__file__).parent.parent
sys.path.insert(0, str(app_path))

from app.core.database import AsyncSessionLocal, init_db
from app.models.client import Client
from app.models.table import Table
from app.models.product import Product
from app.models.command import Command
from app.models.item_command import ItemCommand
from app.models.payment import Payment
from app.models.document import Document

from scripts.seeds.client_seed import seed_clients
from scripts.seeds.table_seed import seed_tables
from scripts.seeds.product_seed import seed_products
from scripts.seeds.command_seed import seed_commands
from scripts.seeds.item_command_seed import seed_item_commands
from scripts.seeds.payment_seed import seed_payments
from scripts.seeds.document_seed import seed_documents

async def main():
    print("Iniciando verificação do banco de dados...")
    
    await init_db()
    
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Product).limit(1))
        existing_products = result.scalars().all()
        
        if len(existing_products) > 0:
            print("\nO banco já contém dados!")
            response = input("Deseja limpar todas as tabelas e recriar as seeds? (s/n): ").lower()
            
            if response == "s":
                print("Limpando dados existentes...")
                await session.execute(delete(Document))
                await session.execute(delete(Payment))
                await session.execute(delete(ItemCommand))
                await session.execute(delete(Command))
                await session.execute(delete(Product))
                await session.execute(delete(Table))
                await session.execute(delete(Client))
                await session.commit()
                print("✓ Banco limpo.")
            else:
                print("Operação cancelada.")
                return
    
    async with AsyncSessionLocal() as session:
        print("\n> Criando Clientes (mínimo 100)")
        clients = await seed_clients(session, count=120)
        
        print("\n> Criando Mesas (mínimo 100)")
        tables = await seed_tables(session, count=100)
        
        print("\n> Criando Produtos (mínimo 100)")
        products = await seed_products(session, count=120)
        
    async with AsyncSessionLocal() as session:
        print("\n> Criando Comandas (mínimo 100)")
        commands = await seed_commands(session, clients, tables, count=150)
        
    async with AsyncSessionLocal() as session:
        print("\n> Criando Itens das Comandas")
        item_commands = await seed_item_commands(session, commands, products)
        
    async with AsyncSessionLocal() as session:
        print("\n> Processando Pagamentos")
        payments = await seed_payments(session, commands)
        
    async with AsyncSessionLocal() as session:
        print("\n> Gerando Documentos e Arquivos Locais")
        await seed_documents(session, products)
        
    async with AsyncSessionLocal() as session:
        total_clients = (await session.execute(select(Client))).scalars().all()
        total_tables = (await session.execute(select(Table))).scalars().all()
        total_products = (await session.execute(select(Product))).scalars().all()
        total_commands = (await session.execute(select(Command))).scalars().all()
        total_items = (await session.execute(select(ItemCommand))).scalars().all()
        total_payments = (await session.execute(select(Payment))).scalars().all()
        total_docs = (await session.execute(select(Document))).scalars().all()

if __name__ == "__main__":
    asyncio.run(main())
