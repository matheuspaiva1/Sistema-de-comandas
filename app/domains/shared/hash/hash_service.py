import hashlib

def gerar_hash(valor: str, algoritmo: str) -> str:
    algoritmos = {
        "md5": hashlib.md5,
        "sha1": hashlib.sha1,
        "sha-1": hashlib.sha1,
        "sha256": hashlib.sha256,
        "sha-256": hashlib.sha256,
    }

    algoritmo = algoritmo.lower()

    if algoritmo not in algoritmos:
        raise ValueError("Algoritmo inválido")

    return algoritmos[algoritmo](valor.encode("utf-8")).hexdigest()