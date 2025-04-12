"""
Validações personalizadas reutilizáveis.

Este arquivo contém validações que podem ser reutilizadas em diferentes projetos.
As validações aqui implementadas são genéricas e não específicas ao PyQuent.

Exemplo de uso:
    from config.validators import TelefoneValidator
    
    # Validar telefone
    validador = TelefoneValidator()
    resultado = validador.validate("(11) 99999-9999")
"""

import re
from typing import Dict, List
from pyquent.utils.validators import Validator, ValidationResult

class TelefoneValidator(Validator):
    """Validador para números de telefone."""
    
    def validate(self, telefone: str) -> ValidationResult:
        """
        Valida um número de telefone.
        
        Args:
            telefone: Número de telefone a ser validado
            
        Returns:
            ValidationResult com o resultado da validação
        """
        # Remove caracteres não numéricos
        numeros = re.sub(r'\D', '', telefone)
        
        # Valida formato
        if not re.match(r'^[0-9]{10,11}$', numeros):
            return ValidationResult(
                success=False,
                message=self.get_message('phone.invalid'),
                errors=[self.get_message('phone.invalid')]
            )
            
        return ValidationResult(
            success=True,
            message=self.get_message('phone.valid')
        )

class CEPValidator(Validator):
    """Validador para CEPs brasileiros."""
    
    def validate(self, cep: str) -> ValidationResult:
        """
        Valida um CEP brasileiro.
        
        Args:
            cep: CEP a ser validado
            
        Returns:
            ValidationResult com o resultado da validação
        """
        # Remove caracteres não numéricos
        numeros = re.sub(r'\D', '', cep)
        
        # Valida formato
        if not re.match(r'^[0-9]{8}$', numeros):
            return ValidationResult(
                success=False,
                message=self.get_message('cep.invalid'),
                errors=[self.get_message('cep.invalid')]
            )
            
        return ValidationResult(
            success=True,
            message=self.get_message('cep.valid')
        )

class EmailValidator(Validator):
    """Validador para endereços de e-mail."""
    
    def validate(self, email: str) -> ValidationResult:
        """
        Valida um endereço de e-mail.
        
        Args:
            email: E-mail a ser validado
            
        Returns:
            ValidationResult com o resultado da validação
        """
        # Expressão regular para validar e-mail
        padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if not re.match(padrao, email):
            return ValidationResult(
                success=False,
                message=self.get_message('email.invalid'),
                errors=[self.get_message('email.invalid')]
            )
            
        return ValidationResult(
            success=True,
            message=self.get_message('email.valid')
        )

class SenhaValidator(Validator):
    """Validador para senhas."""
    
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
            errors.append(self.get_message('password.length'))
            
        # Verifica letra maiúscula
        if not re.search(r'[A-Z]', senha):
            errors.append(self.get_message('password.uppercase'))
            
        # Verifica letra minúscula
        if not re.search(r'[a-z]', senha):
            errors.append(self.get_message('password.lowercase'))
            
        # Verifica número
        if not re.search(r'[0-9]', senha):
            errors.append(self.get_message('password.number'))
            
        # Verifica caractere especial
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', senha):
            errors.append(self.get_message('password.special'))
            
        if errors:
            return ValidationResult(
                success=False,
                message=self.get_message('password.invalid'),
                errors=errors
            )
            
        return ValidationResult(
            success=True,
            message=self.get_message('password.valid')
        ) 