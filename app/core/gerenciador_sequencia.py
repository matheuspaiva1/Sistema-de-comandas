import os
import fcntl
from pathlib import Path


class SequenceManager:
    """Gerencia um arquivo .seq contendo o valor numérico inteiro para IDs."""

    def __init__(self, sequence_name: str):
        self.seq_file = Path(f"./data/{sequence_name}.seq")
        # Garante que a pasta base exista
        self.seq_file.parent.mkdir(parents=True, exist_ok=True)

        # Se arquivo não existe, inicializa com 0
        if not self.seq_file.exists():
            with open(self.seq_file, "w") as f:
                f.write("0")

    def get_next_id(self) -> int:
        """Lê o valor atual, incrementa de 1, salva e retorna o novo valor,
        usando locks de sistema de arquivo para segurança entre múltiplas transações simultâneas."""
        fd = open(self.seq_file, "r+")
        try:
            # Trava exclusiva para leitura e escrita bloqueando concorrências
            fcntl.flock(fd, fcntl.LOCK_EX)
            content = fd.read().strip()
            # Pega o ID atual ou assume 0
            current_id = int(content) if content else 0
            # Regra: ao processar o 'get', ele garante o próximo ID.
            new_id = current_id + 1

            # Sobrescreve com sucesso
            fd.seek(0)
            fd.write(str(new_id))
            fd.truncate()

            return new_id
        finally:
            # Libera o lock
            fcntl.flock(fd, fcntl.LOCK_UN)
            fd.close()
