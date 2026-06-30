from typing import Annotated
from pydantic import BeforeValidator

# Converte ObjectId do MongoDB para str automaticamente na serialização
PyObjectId = Annotated[str, BeforeValidator(str)]
