from typing import Optional

from sqlmodel import Field, Relationship, SQLModel


class ItemCommand(SQLModel, table=True):
    """Representa um item de produto associado a uma comanda, com quantidade e preço unitário."""

    __tablename__ = "item_commands"

    id: Optional[int] = Field(default=None, primary_key=True)
    command_id: int = Field(foreign_key="commands.id", index=True)
    product_id: int = Field(foreign_key="products.id", index=True)
    quantity: int = Field(gt=0)
    unit_price: float = Field(gt=0)

    command: "Command" = Relationship(back_populates="items")
    product: "Product" = Relationship(back_populates="item_commands")
