"""
Classe base para todos os modelos do sistema.
Define comportamentos e atributos comuns.
"""

from quentorm import Model

class BaseModel(Model):
    """
    Classe base para todos os modelos do sistema.
    Herda de Model do QuentORM e adiciona funcionalidades comuns.
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    @classmethod
    def get_table_name(cls):
        """Retorna o nome da tabela no banco de dados."""
        return cls.__name__.lower() + 's' 