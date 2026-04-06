from fastapi import APIRouter, HTTPException
from typing import Literal
from app.domains.shared.hash.hash_service import gerar_hash

router = APIRouter(prefix="/hash", tags=["Hash"])

@router.get(
    "",
    summary="Gerar hash",
    description="""
Request:
- Query param `valor`: texto a ser processado.
- Query param `algoritmo`: `md5`, `sha1`, `sha-1`, `sha256` ou `sha-256`.

Response:
- Retorna algoritmo normalizado, valor original e hash gerado.
- Retorna 400 quando o algoritmo é inválido.
""",
    response_description="Hash calculado com sucesso",
)
def compute_hash(
    valor: str,
    algoritmo: Literal["md5", "sha1", "sha-1", "sha256", "sha-256"]
):
    try:
        resultado = gerar_hash(valor, algoritmo)
        return {
            "algoritmo": algoritmo.lower(),
            "valor": valor,
            "hash": resultado
        }
    except ValueError:
        raise HTTPException(status_code=400, detail="Algoritmo inválido")