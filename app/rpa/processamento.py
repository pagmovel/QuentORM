"""
Exemplo de RPA usando modelos importados.

Este módulo demonstra como usar os modelos base
em um processo de automação.
"""

from app.models.base import Cliente, ContaBancaria
from pyquent.utils.validators import validar_cpf, validar_agencia, validar_conta
import pandas as pd
from datetime import datetime

class ProcessadorClientes:
    """Processa dados de clientes e contas bancárias."""
    
    def __init__(self, arquivo_clientes, arquivo_contas):
        self.arquivo_clientes = arquivo_clientes
        self.arquivo_contas = arquivo_contas
        
    def processar_clientes(self):
        """Processa dados de clientes."""
        df = pd.read_excel(self.arquivo_clientes)
        
        for _, linha in df.iterrows():
            # Validar CPF
            if not validar_cpf(linha['cpf']):
                print(f"CPF inválido: {linha['cpf']}")
                continue
                
            # Criar cliente
            cliente = Cliente.create(
                nome=linha['nome'],
                cpf=linha['cpf'],
                email=linha['email'],
                telefone=linha['telefone']
            )
            
            # Salvar no banco
            cliente.save()
            print(f"Cliente criado: {cliente.nome}")
            
    def processar_contas(self):
        """Processa dados de contas bancárias."""
        df = pd.read_excel(self.arquivo_contas)
        
        for _, linha in df.iterrows():
            # Validar dados bancários
            if not validar_agencia(linha['agencia']):
                print(f"Agência inválida: {linha['agencia']}")
                continue
                
            if not validar_conta(linha['conta']):
                print(f"Conta inválida: {linha['conta']}")
                continue
                
            # Buscar cliente
            cliente = Cliente.where('cpf', linha['cpf_cliente']).first()
            if not cliente:
                print(f"Cliente não encontrado: {linha['cpf_cliente']}")
                continue
                
            # Criar conta
            conta = ContaBancaria.create(
                agencia=linha['agencia'],
                conta=linha['conta'],
                digito=linha['digito'],
                cliente_id=cliente.id
            )
            
            # Salvar no banco
            conta.save()
            print(f"Conta criada para: {cliente.nome}")
            
    def executar(self):
        """Executa o processamento completo."""
        print("Iniciando processamento...")
        print(f"Data: {datetime.now()}")
        
        print("\nProcessando clientes...")
        self.processar_clientes()
        
        print("\nProcessando contas...")
        self.processar_contas()
        
        print("\nProcessamento concluído!") 