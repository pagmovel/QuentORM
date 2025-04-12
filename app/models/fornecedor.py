from pyquent import Model, Column, relationship, validates
from pyquent.utils.validators import validar_cpf_cnpj
import re

class Fornecedor(Model):
    __tablename__ = 'tbl_fornecedores'
    
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    cpf_cnpj = Column(String(20), unique=True, nullable=False)
    email = Column(String(100))
    telefone = Column(String(20))
    
    contas_pagar = relationship('ContaPagar', back_populates='fornecedor')
    
    @validates('cpf_cnpj')
    def validar_cpf_cnpj(self, key, value):
        """Valida o CPF ou CNPJ do fornecedor"""
        if not validar_cpf_cnpj(value):
            raise ValueError('CPF/CNPJ inválido')
        return value
    
    @validates('email')
    def validar_email(self, key, value):
        """Valida o email do fornecedor"""
        if value and not re.match(r'[^@]+@[^@]+\.[^@]+', value):
            raise ValueError('Email inválido')
        return value
    
    @validates('telefone')
    def validar_telefone(self, key, value):
        """Valida o telefone do fornecedor"""
        if value and not re.match(r'^\(\d{2}\) \d{5}-\d{4}$', value):
            raise ValueError('Telefone inválido. Use o formato (99) 99999-9999')
        return value 