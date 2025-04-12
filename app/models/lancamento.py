from pyquent import Model, Column, relationship, validates
from datetime import datetime

class Lancamento(Model):
    __tablename__ = 'tbl_lancamentos'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    tipo = Column(String(20), nullable=False)
    descricao = Column(String(200), nullable=False)
    valor = Column(Numeric(10,2), nullable=False)
    data = Column(Date, nullable=False)
    conta_bancaria_id = Column(Integer, ForeignKey('tbl_contas_bancarias.id'))
    cartao_id = Column(Integer, ForeignKey('tbl_cartoes.id'))
    conta_pagar_id = Column(Integer, ForeignKey('tbl_contas_pagar.id'))
    conta_receber_id = Column(Integer, ForeignKey('tbl_contas_receber.id'))
    
    user = relationship('User', back_populates='lancamentos')
    conta_bancaria = relationship('ContaBancaria', back_populates='lancamentos')
    cartao = relationship('Cartao', back_populates='lancamentos')
    conta_pagar = relationship('ContaPagar', back_populates='lancamentos')
    conta_receber = relationship('ContaReceber', back_populates='lancamentos')
    
    @validates('valor')
    def validar_valor(self, key, value):
        """Valida o valor do lançamento"""
        if value <= 0:
            raise ValueError('O valor deve ser maior que zero')
        return value
    
    @validates('data')
    def validar_data(self, key, value):
        """Valida a data do lançamento"""
        if value > datetime.now().date():
            raise ValueError('A data do lançamento não pode ser futura')
        return value
    
    @validates('tipo')
    def validar_tipo(self, key, value):
        """Valida o tipo do lançamento"""
        tipos_validos = ['entrada', 'saida']
        if value not in tipos_validos:
            raise ValueError(f'Tipo inválido. Use um dos seguintes: {", ".join(tipos_validos)}')
        return value 