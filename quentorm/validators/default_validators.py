"""
Validações padrão do QuentORM.

Este arquivo contém as validações padrão do framework
que podem ser estendidas pelo usuário.
"""

import re
from typing import Dict, List, Any, Optional
from quentorm.utils.validators import Validator, ValidationResult
from datetime import datetime
from quentorm.config import settings

class DefaultEmailValidator(Validator):
    """
    Validador padrão para endereços de e-mail.
    
    Implementa regras de validação para endereços de e-mail
    seguindo o padrão RFC 5322.
    """
    
    def __init__(self):
        """Inicializa o validador com o idioma configurado."""
        super().__init__()
        self.locale = settings.APP_LOCALE
    
    def validate(self, data: Dict[str, Any]) -> ValidationResult:
        """
        Valida um endereço de e-mail.
        
        Args:
            data: Dicionário contendo o campo 'email' a ser validado
            
        Returns:
            ValidationResult: Resultado da validação
        """
        result = ValidationResult()
        
        email = data.get('email', '')
        if not email:
            result.add_error('email', self.get_message('validations.email.invalid'))
            return result
            
        # Verifica formato básico
        if '@' not in email or '.' not in email:
            result.add_error('email', self.get_message('validations.email.invalid'))
            return result
            
        # Verifica domínio
        domain = email.split('@')[1]
        if len(domain.split('.')) < 2:
            result.add_error('email', self.get_message('validations.email.invalid'))
            
        return result

class DefaultCPFValidator(Validator):
    """
    Validador padrão para números de CPF.
    
    Implementa o algoritmo de validação de CPF conforme
    as regras da Receita Federal.
    """
    
    def __init__(self):
        """Inicializa o validador com o idioma configurado."""
        super().__init__()
        self.locale = settings.APP_LOCALE
    
    def validate(self, data: Dict[str, Any]) -> ValidationResult:
        """
        Valida um número de CPF.
        
        Args:
            data: Dicionário contendo o campo 'cpf' a ser validado
            
        Returns:
            ValidationResult: Resultado da validação
        """
        result = ValidationResult()
        
        cpf = data.get('cpf', '')
        if not cpf:
            result.add_error('cpf', self.get_message('validations.cpf.invalid_length'))
            return result
            
        # Remove caracteres não numéricos
        cpf = ''.join(filter(str.isdigit, cpf))
        
        # Verifica tamanho
        if len(cpf) != 11:
            result.add_error('cpf', self.get_message('validations.cpf.invalid_length'))
            return result
            
        # Verifica dígitos repetidos
        if cpf == cpf[0] * 11:
            result.add_error('cpf', self.get_message('validations.cpf.invalid_digits'))
            return result
            
        # Calcula primeiro dígito verificador
        soma = 0
        for i in range(9):
            soma += int(cpf[i]) * (10 - i)
        resto = 11 - (soma % 11)
        if resto > 9:
            resto = 0
        if resto != int(cpf[9]):
            result.add_error('cpf', self.get_message('validations.cpf.invalid_check_digits'))
            return result
            
        # Calcula segundo dígito verificador
        soma = 0
        for i in range(10):
            soma += int(cpf[i]) * (11 - i)
        resto = 11 - (soma % 11)
        if resto > 9:
            resto = 0
        if resto != int(cpf[10]):
            result.add_error('cpf', self.get_message('validations.cpf.invalid_check_digits'))
            
        return result

class DefaultSenhaValidator(Validator):
    """Validador padrão para senhas."""
    
    def __init__(self):
        """Inicializa o validador com o idioma configurado."""
        super().__init__()
        self.locale = settings.APP_LOCALE
    
    def validate(self, senha: str) -> ValidationResult:
        """
        Valida uma senha.
        
        Regras:
        - Mínimo 8 caracteres
        - Pelo menos uma letra maiúscula
        - Pelo menos uma letra minúscula
        - Pelo menos um número
        - Pelo menos um caractere especial
        
        Args:
            senha: Senha a ser validada
            
        Returns:
            ValidationResult com o resultado da validação
        """
        errors: List[str] = []
        
        # Verifica comprimento mínimo
        if len(senha) < 8:
            errors.append(self.get_message('validations.password.length'))
            
        # Verifica letra maiúscula
        if not re.search(r'[A-Z]', senha):
            errors.append(self.get_message('validations.password.uppercase'))
            
        # Verifica letra minúscula
        if not re.search(r'[a-z]', senha):
            errors.append(self.get_message('validations.password.lowercase'))
            
        # Verifica número
        if not re.search(r'[0-9]', senha):
            errors.append(self.get_message('validations.password.number'))
            
        # Verifica caractere especial
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', senha):
            errors.append(self.get_message('validations.password.special'))
            
        if errors:
            return ValidationResult(
                success=False,
                message=self.get_message('validations.password.invalid'),
                errors=errors
            )
            
        return ValidationResult(
            success=True,
            message=self.get_message('validations.password.valid')
        ) 