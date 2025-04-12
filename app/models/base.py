"""
Modelos base do sistema.

Este módulo contém os modelos base que podem ser importados
e estendidos em outros projetos.
"""

from pyquent import Model
from datetime import datetime

class BaseModel(Model):
    """Modelo base com campos comuns."""
    
    id = Column(Integer, primary_key=True)
    criado_em = Column(DateTime, default=datetime.now)
    atualizado_em = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    def to_dict(self):
        """Converte o modelo para dicionário."""
        return {
            'id': self.id,
            'criado_em': self.criado_em.isoformat(),
            'atualizado_em': self.atualizado_em.isoformat()
        }

class Cliente(BaseModel):
    """Modelo de cliente."""
    
    __table__ = 'clientes'
    
    nome = Column(String(255))
    cpf = Column(String(11))
    email = Column(String(255))
    telefone = Column(String(20))
    
    def to_dict(self):
        """Converte o modelo para dicionário."""
        dados = super().to_dict()
        dados.update({
            'nome': self.nome,
            'cpf': self.cpf,
            'email': self.email,
            'telefone': self.telefone
        })
        return dados

class ContaBancaria(BaseModel):
    """Modelo de conta bancária."""
    
    __table__ = 'contas_bancarias'
    
    agencia = Column(String(10))
    conta = Column(String(20))
    digito = Column(String(2))
    cliente_id = Column(Integer, ForeignKey('clientes.id'))
    
    def to_dict(self):
        """Converte o modelo para dicionário."""
        dados = super().to_dict()
        dados.update({
            'agencia': self.agencia,
            'conta': self.conta,
            'digito': self.digito,
            'cliente_id': self.cliente_id
        })
        return dados 