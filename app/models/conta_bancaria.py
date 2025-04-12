from pyquent import Model, Column, relationship, validates
from pyquent.utils.validators import validar_agencia, validar_conta, validar_digito

class ContaBancaria(Model):
    __tablename__ = 'tbl_contas_bancarias'
    
    id = Column(Integer, primary_key=True)
    banco_id = Column(Integer, ForeignKey('tbl_bancos.id'), nullable=False)
    agencia = Column(String(10), nullable=False)
    conta = Column(String(20), nullable=False)
    digito = Column(String(2))
    saldo = Column(Numeric(10,2), default=0)
    
    banco = relationship('Banco', back_populates='contas_bancarias')
    lancamentos = relationship('Lancamento', back_populates='conta_bancaria')
    
    @validates('agencia')
    def validar_agencia(self, key, value):
        """Valida o número da agência"""
        if not validar_agencia(value):
            raise ValueError('Agência inválida. Deve ter entre 4 e 10 dígitos')
        return value
    
    @validates('conta')
    def validar_conta(self, key, value):
        """Valida o número da conta"""
        if not validar_conta(value):
            raise ValueError('Conta inválida. Deve ter entre 5 e 20 dígitos')
        return value
    
    @validates('digito')
    def validar_digito(self, key, value):
        """Valida o dígito verificador"""
        if not validar_digito(value):
            raise ValueError('Dígito verificador inválido. Deve ter no máximo 2 dígitos')
        return value 