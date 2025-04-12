from pyquent import Model, Column, relationship, validates
from datetime import datetime

class ContaReceber(Model):
    __tablename__ = 'tbl_contas_receber'
    
    id = Column(Integer, primary_key=True)
    cliente_id = Column(Integer, ForeignKey('tbl_clientes.id'), nullable=False)
    descricao = Column(String(200), nullable=False)
    valor = Column(Numeric(10,2), nullable=False)
    data_vencimento = Column(Date, nullable=False)
    data_recebimento = Column(Date)
    status = Column(String(20), default='pendente')
    
    cliente = relationship('Cliente', back_populates='contas_receber')
    
    @validates('valor')
    def validar_valor(self, key, value):
        """Valida o valor da conta"""
        if value <= 0:
            raise ValueError('O valor deve ser maior que zero')
        return value
    
    @validates('data_vencimento')
    def validar_data_vencimento(self, key, value):
        """Valida a data de vencimento"""
        if value < datetime.now().date():
            raise ValueError('A data de vencimento não pode ser anterior à data atual')
        return value
    
    @validates('data_recebimento')
    def validar_data_recebimento(self, key, value):
        """Valida a data de recebimento"""
        if value and value > datetime.now().date():
            raise ValueError('A data de recebimento não pode ser futura')
        return value
    
    @validates('status')
    def validar_status(self, key, value):
        """Valida o status da conta"""
        status_validos = ['pendente', 'recebido', 'cancelado']
        if value not in status_validos:
            raise ValueError(f'Status inválido. Use um dos seguintes: {", ".join(status_validos)}')
        return value 