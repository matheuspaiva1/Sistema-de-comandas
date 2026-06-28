"""
Script compatível com o comando antigo de seed.
Executa o orquestrador MongoDB definido na raiz do projeto.
"""

import asyncio
import importlib.util
from pathlib import Path
import sys


project_root = Path(__file__).resolve().parent.parent
seed_path = project_root / "seed.py"
sys.path.insert(0, str(project_root))

spec = importlib.util.spec_from_file_location("mongo_seed", seed_path)
mongo_seed = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mongo_seed)


if __name__ == "__main__":
    asyncio.run(mongo_seed.main())
