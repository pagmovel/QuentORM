"""
Validações específicas do projeto PyQuent.

Este arquivo contém validações que são específicas para o projeto PyQuent
e não devem ser compartilhadas com outros projetos.

Exemplo de uso:
    from config.validators import ContaBancariaValidator
    
    # Validar conta bancária
    validador = ContaBancariaValidator()
    resultado = validador.validate("1234", "56789-0")
"""

from typing import Dict, List
from pyquent.utils.validators import Validator, ValidationResult
from quentorm.utils.validators import validate_project_name

class ContaBancariaValidator(Validator):
    """Validador para contas bancárias do PyQuent."""
    
    def validate(self, agencia: str, conta: str, digito: str = None) -> ValidationResult:
        """
        Valida os dados de uma conta bancária.
        
        Args:
            agencia: Número da agência
            conta: Número da conta
            digito: Dígito verificador (opcional)
            
        Returns:
            ValidationResult com o resultado da validação
        """
        errors: List[str] = []
        
        # Valida agência
        if not agencia or not agencia.isdigit():
            errors.append(self.get_message('bank.agency.invalid'))
            
        # Valida conta
        if not conta or not conta.replace('-', '').isdigit():
            errors.append(self.get_message('bank.account.invalid'))
            
        # Valida dígito se fornecido
        if digito and not digito.isdigit():
            errors.append(self.get_message('bank.digit.invalid'))
            
        if errors:
            return ValidationResult(
                success=False,
                message=self.get_message('bank.validation.failed'),
                errors=errors
            )
            
        return ValidationResult(
            success=True,
            message=self.get_message('bank.validation.success')
        )

class LancamentoValidator(Validator):
    """Validador para lançamentos financeiros do PyQuent."""
    
    def validate(self, valor: float, data: str, tipo: str) -> ValidationResult:
        """
        Valida os dados de um lançamento financeiro.
        
        Args:
            valor: Valor do lançamento
            data: Data do lançamento
            tipo: Tipo do lançamento ('entrada' ou 'saida')
            
        Returns:
            ValidationResult com o resultado da validação
        """
        errors: List[str] = []
        
        # Valida valor
        if not valor or valor <= 0:
            errors.append(self.get_message('transaction.value.invalid'))
            
        # Valida data
        if not data:
            errors.append(self.get_message('transaction.date.required'))
            
        # Valida tipo
        if tipo not in ['entrada', 'saida']:
            errors.append(self.get_message('transaction.type.invalid'))
            
        if errors:
            return ValidationResult(
                success=False,
                message=self.get_message('transaction.validation.failed'),
                errors=errors
            )
            
        return ValidationResult(
            success=True,
            message=self.get_message('transaction.validation.success')
        )

def validate_project_name(name: str) -> bool:
    """Valida o nome do projeto QuentORM"""
    if not name:
        return False
    if name.lower() == 'quentorm':
        return False
    return True 