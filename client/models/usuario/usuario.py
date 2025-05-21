from datetime import datetime
from typing import Any, Dict

class Usuario:
    """
    Representa um usuário do sistema.

    Atributos:
        id (int): Identificador único do usuário.
        nome (str): Primeiro nome do usuário.
        sobrenome (str): Sobrenome do usuário.
        username (str): Nome de usuário (login).
        email (str): Endereço de e-mail do usuário.
        nome_diretorio (str): Nome do diretório associado ao usuário.
        data_criacao (datetime): Data e hora de criação do usuário.
    """

    def __init__(
        self,
        id: int,
        nome: str,
        sobrenome: str,
        username: str,
        email: str,
        nome_diretorio: str,
        data_criacao: datetime
    ):
        self.id = id
        self.nome = nome
        self.sobrenome = sobrenome
        self.username = username
        self.email = email
        self.nome_diretorio = nome_diretorio
        self.data_criacao = data_criacao

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Usuario":
        """
        Cria uma instância de Usuario a partir de um dicionário.

        Args:
            data (dict): Dicionário com os dados do usuário.

        Returns:
            Usuario: Instância criada.
        """
        return cls(
            id=int(data.get("id", 0)),
            nome=str(data.get("nome", "")),
            sobrenome=str(data.get("sobrenome", "")),
            username=str(data.get("username", "")),
            email=str(data.get("email", "")),
            nome_diretorio=str(data.get("nome_diretorio", "")),
            data_criacao=cls._parse_datetime(data.get("data_criacao"))
        )

    @staticmethod
    def _parse_datetime(value: Any) -> datetime:
        """
        Converte uma string em datetime.

        Args:
            value (str): String com data e hora no formato "YYYY-MM-DD HH:MM:SS".

        Returns:
            datetime: Objeto datetime correspondente.
        """
        if isinstance(value, datetime):
            return value
        try:
            return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
        except (ValueError, TypeError):
            return datetime.min  # ou lançar uma exceção, se preferir

    def __str__(self) -> str:
        return f"{self.nome} {self.sobrenome} (@{self.username})"

    def __repr__(self) -> str:
        return (
            f"Usuario(id={self.id}, nome='{self.nome}', sobrenome='{self.sobrenome}', "
            f"username='{self.username}', email='{self.email}', "
            f"nome_diretorio='{self.nome_diretorio}', data_criacao='{self.data_criacao}')"
        )

