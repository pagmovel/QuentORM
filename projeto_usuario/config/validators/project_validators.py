"""
Validações específicas do projeto QuentORM.

Este arquivo contém validações que são específicas para o projeto QuentORM
e não devem ser reutilizadas em outros projetos.

Exemplo de uso:
    from config.validators import ContaBancariaValidator
    
    # Validar conta bancária
    validador = ContaBancariaValidator()
    resultado = validador.validate({"banco": "Banco do Brasil", "agencia": "1234", "conta": "56789-0"})
"""

from datetime import datetime
from typing import Optional, Dict, Any

from quentorm.utils.validators import Validator, ValidationResult

class ContaBancariaValidator(Validator):
    """
    Validador para contas bancárias do QuentORM.
    
    Este validador implementa regras específicas para contas bancárias
    do sistema financeiro.
    """
    
    def validate(self, data: Dict[str, Any]) -> ValidationResult:
        """
        Valida os dados de uma conta bancária.
        
        Args:
            data: Dicionário com os dados da conta bancária
            
        Returns:
            ValidationResult: Resultado da validação
        """
        result = ValidationResult()
        
        # Valida o banco
        if not data.get('banco'):
            result.add_error('banco', 'O banco é obrigatório')
            
        # Valida a agência
        if not data.get('agencia'):
            result.add_error('agencia', 'A agência é obrigatória')
        elif len(data['agencia']) != 4:
            result.add_error('agencia', 'A agência deve ter 4 dígitos')
            
        # Valida a conta
        if not data.get('conta'):
            result.add_error('conta', 'A conta é obrigatória')
        elif len(data['conta']) < 5:
            result.add_error('conta', 'A conta deve ter pelo menos 5 dígitos')
            
        # Valida o saldo inicial
        if 'saldo' in data and data['saldo'] < 0:
            result.add_error('saldo', 'O saldo não pode ser negativo')
            
        return result

class LancamentoValidator(Validator):
    """
    Validador para lançamentos financeiros do QuentORM.
    
    Este validador implementa regras específicas para lançamentos
    financeiros do sistema.
    """
    
    def validate(self, data: Dict[str, Any]) -> ValidationResult:
        """
        Valida os dados de um lançamento financeiro.
        
        Args:
            data: Dicionário com os dados do lançamento
            
        Returns:
            ValidationResult: Resultado da validação
        """
        result = ValidationResult()
        
        # Valida a descrição
        if not data.get('descricao'):
            result.add_error('descricao', 'A descrição é obrigatória')
        elif len(data['descricao']) < 3:
            result.add_error('descricao', 'A descrição deve ter pelo menos 3 caracteres')
            
        # Valida o valor
        if 'valor' not in data:
            result.add_error('valor', 'O valor é obrigatório')
        elif data['valor'] <= 0:
            result.add_error('valor', 'O valor deve ser maior que zero')
            
        # Valida a data
        if not data.get('data'):
            result.add_error('data', 'A data é obrigatória')
        else:
            try:
                data_obj = datetime.strptime(data['data'], '%Y-%m-%d')
                if data_obj > datetime.now():
                    result.add_error('data', 'A data não pode ser futura')
            except ValueError:
                result.add_error('data', 'Data inválida')
                
        return result 