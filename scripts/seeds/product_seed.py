import random
from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.product import Product, CategoryEnum

fake = Faker("pt_BR")

async def seed_products(session: AsyncSession, count: int = 120) -> list[Product]:
    """Cria produtos fictícios agrupados por categoria."""
    produtos = []
    categorias = list(CategoryEnum)
    
    for i in range(count):
        categoria = categorias[i % len(categorias)]
        
        if categoria == CategoryEnum.BEBIDA:
            preco = round(fake.pydecimal(left_digits=3, right_digits=2, positive=True, min_value=3, max_value=30), 2)
            nome_base = ["Refrigerante", "Suco", "Água", "Chá gelado", "Café", "Milkshake", "Smoothie", "Bebida energética", "Vinho", "Cerveja"]
            nome = f"{random.choice(nome_base)} {fake.word().capitalize()}"
            
        elif categoria == CategoryEnum.PRATO_PRINCIPAL:
            preco = round(fake.pydecimal(left_digits=3, right_digits=2, positive=True, min_value=25, max_value=150), 2)
            nome_base = ["Prato de", "Filé", "Peito de", "Arroz com", "Macarrão à", "Risoto de"]
            ingrediente = ["Frango", "Carne", "Peixe", "Camarão", "Cogumelo", "Brócolis"]
            nome = f"{random.choice(nome_base)} {random.choice(ingrediente)}"
            
        elif categoria == CategoryEnum.ENTRADA:
            preco = round(fake.pydecimal(left_digits=3, right_digits=2, positive=True, min_value=15, max_value=50), 2)
            nome_base = ["Entrada de", "Tábua de", "Pão", "Patê de", "Salada de"]
            ingrediente = ["Queijo", "Presunto", "Vegetais", "Tomate", "Alface", "Frutos do mar"]
            nome = f"{random.choice(nome_base)} {random.choice(ingrediente)}"
            
        elif categoria == CategoryEnum.SOBREMESA:
            preco = round(fake.pydecimal(left_digits=3, right_digits=2, positive=True, min_value=10, max_value=40), 2)
            nome_base = ["Bolo de", "Mousse de", "Torta de", "Pudim de", "Sorvete de", "Doce de"]
            sabor = ["Chocolate", "Morango", "Maracujá", "Limão", "Coco", "Pistache"]
            nome = f"{random.choice(nome_base)} {random.choice(sabor)}"
            
        else: 
            preco = round(fake.pydecimal(left_digits=3, right_digits=2, positive=True, min_value=8, max_value=35), 2)
            nome_base = ["X-Burger", "Sanduíche de", "Pastel de", "Coxinha de", "Croquete de"]
            ingrediente = ["Queijo", "Frango", "Carne", "Calabresa", "Palmito"]
            nome = f"{random.choice(nome_base)} {random.choice(ingrediente)}"
        
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
