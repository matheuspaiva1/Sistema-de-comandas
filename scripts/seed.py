"""
Compatibilidade de seed MongoDB para o projeto.

Este arquivo delega para o seed principal do projeto, que já usa
Motor + Beanie e funciona com a configuração de MongoDB.
"""

import argparse
import asyncio
from pathlib import Path
import sys

app_path = Path(__file__).parent.parent
sys.path.insert(0, str(app_path))

from seed import main as project_seed_main


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Popula o banco MongoDB do projeto com dados de exemplo."
    )
    parser.add_argument(
        "--no-clean",
        action="store_true",
        help="Mantém os dados existentes e apenas adiciona novos registros.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    asyncio.run(project_seed_main(clean=not args.no_clean))
