import asyncio
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.core.database import AsyncSessionLocal
from app.models.client import Client
from app.models.product import Product

async def main():
    async with AsyncSessionLocal() as session:
        # create client
        client = Client(nome='Teste Item', telefone='11999999999', email='item@example.com')
        session.add(client)
        await session.commit()
        await session.refresh(client)
        # create product
        product = Product(nome='Produto Teste', descricao='desc', preco=100.0)
        session.add(product)
        await session.commit()
        await session.refresh(product)
        # create command
        from app.models.command import Command
        command = Command(client_id=client.id)
        session.add(command)
        await session.commit()
        await session.refresh(command)
        # create order
        from app.models.order import Order
        order = Order(command_id=command.id)
        session.add(order)
        await session.commit()
        await session.refresh(order)
        order_id = order.id
        product_id = product.id

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url='http://test') as http_client:
        response = await http_client.post('/itens-pedido/', json={'order_id': order_id, 'product_id': product_id, 'quantity': 2})
        print(response.status_code)
        print(response.text)

if __name__ == '__main__':
    asyncio.run(main())
