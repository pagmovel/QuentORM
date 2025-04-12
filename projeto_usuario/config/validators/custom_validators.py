"""
Validações personalizadas do usuário para o QuentORM.

Este arquivo contém validações customizadas que podem ser reutilizadas
em diferentes partes do projeto. Estas validações estendem ou complementam
as validações padrão do framework.
"""

import re
from typing import Dict, List, Any, Optional
from quentorm.utils.validators import Validator, ValidationResult
from quentorm.validators.default_validators import (
    DefaultEmailValidator,
    DefaultCPFValidator,
    DefaultSenhaValidator
)
from datetime import datetime
from config.settings import Settings

class CustomEmailValidator(DefaultEmailValidator):
    """
    Validador customizado para endereços de e-mail.
    
    Estende o validador padrão com regras adicionais.
    """
    
    def validate(self, data: Dict[str, Any]) -> ValidationResult:
        """
        Valida um endereço de e-mail.
        
        Args:
            data: Dicionário contendo o campo 'email' a ser validado
            
        Returns:
            ValidationResult: Resultado da validação
        """
        # Primeiro executa a validação padrão
        result = super().validate(data)
        if not result.is_valid():
            return result
            
        # Adiciona validações customizadas
        email = data.get('email', '')
        
        # Verifica domínios bloqueados
        blocked_domains = ['spam.com', 'fake.com']
        domain = email.split('@')[1]
        if domain in blocked_domains:
            result.add_error('email', self.get_message('validations.email.invalid'))
            
        return result

class CustomCPFValidator(DefaultCPFValidator):
    """
    Validador customizado para números de CPF.
    
    Estende o validador padrão com regras adicionais.
    """
    
    def validate(self, data: Dict[str, Any]) -> ValidationResult:
        """
        Valida um número de CPF.
        
        Args:
            data: Dicionário contendo o campo 'cpf' a ser validado
            
        Returns:
            ValidationResult: Resultado da validação
        """
        # Primeiro executa a validação padrão
        result = super().validate(data)
        if not result.is_valid():
            return result
            
        # Adiciona validações customizadas
        cpf = data.get('cpf', '')
        cpf = ''.join(filter(str.isdigit, cpf))
        
        # Verifica CPFs bloqueados
        blocked_cpfs = ['11111111111', '22222222222']
        if cpf in blocked_cpfs:
            result.add_error('cpf', self.get_message('validations.cpf.invalid_digits'))
            
        return result

class CustomSenhaValidator(DefaultSenhaValidator):
    """
    Validador customizado para senhas.
    
    Estende o validador padrão com regras adicionais.
    """
    
    def validate(self, senha: str) -> ValidationResult:
        """
        Valida uma senha.
        
        Args:
            senha: Senha a ser validada
            
        Returns:
            ValidationResult: Resultado da validação
        """
        # Primeiro executa a validação padrão
        result = super().validate(senha)
        if not result.is_valid():
            return result
            
        # Adiciona validações customizadas
        errors: List[str] = []
        
        # Verifica senhas comuns
        common_passwords = ['123456', 'password', 'querty']
        if senha.lower() in common_passwords:
            errors.append(self.get_message('validations.password.invalid'))
            
        # Verifica sequências
        if re.search(r'(.)\1{3,}', senha):
            errors.append(self.get_message('validations.password.invalid'))
            
        if errors:
            return ValidationResult(
                success=False,
                message=self.get_message('validations.password.invalid'),
                errors=errors
            )
            
        return result 