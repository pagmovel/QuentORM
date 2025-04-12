"""
Módulo para validações personalizadas que podem ser compartilhadas entre projetos.

Este arquivo contém validações comuns que podem ser reutilizadas em diferentes projetos.
Para usar estas validações em outro projeto, basta copiar este arquivo e suas dependências.

Exemplo de uso:
    from app.validators.custom_validators import TelefoneValidator, CEPValidator
    
    # Validar telefone
    validador = TelefoneValidator()
    resultado = validador.validate("(11) 99999-9999")
    
    # Validar CEP
    validador = CEPValidator()
    resultado = validador.validate("12345-678")
"""

from typing import Optional
import requests
from config.messages import messages
from pyquent.utils.validators import Validator, ValidationResult

class TelefoneValidator(Validator):
    """Validação de números de telefone."""
    
    def __init__(self):
        super().__init__()
        self.messages = messages.get('validations.telefone', {})
    
    def validate(self, telefone: str) -> ValidationResult:
        """
        Valida um número de telefone.
        
        Args:
            telefone (str): Número de telefone a ser validado
            
        Returns:
            ValidationResult: Resultado da validação
        """
        # Remove caracteres não numéricos
        numeros = ''.join(filter(str.isdigit, telefone))
        
        # Validação básica
        if len(numeros) < 10 or len(numeros) > 11:
            return ValidationResult(
                success=False,
                message=self.messages.get('invalid_length', 'Telefone inválido')
            )
        
        # Validação de DDD
        ddd = numeros[:2]
        if not ddd.isdigit() or int(ddd) < 11:
            return ValidationResult(
                success=False,
                message=self.messages.get('invalid_ddd', 'DDD inválido')
            )
        
        return ValidationResult(
            success=True,
            message=self.messages.get('success', 'Telefone válido')
        )

class CEPValidator(Validator):
    """Validação de CEP com verificação de existência."""
    
    def __init__(self, verificar_existencia: bool = True):
        super().__init__()
        self.verificar_existencia = verificar_existencia
        self.messages = messages.get('validations.cep', {})
    
    def validate(self, cep: str) -> ValidationResult:
        """Valida um CEP."""
        # Remove caracteres não numéricos
        numeros = ''.join(filter(str.isdigit, cep))
        
        # Validação básica
        if len(numeros) != 8:
            return ValidationResult(
                success=False,
                message=self.messages.get('invalid_length', 'CEP inválido')
            )
        
        # Verifica existência se configurado
        if self.verificar_existencia:
            try:
                response = requests.get(f'https://viacep.com.br/ws/{numeros}/json/')
                if response.json().get('erro'):
                    return ValidationResult(
                        success=False,
                        message=self.messages.get('not_found', 'CEP não encontrado')
                    )
            except:
                return ValidationResult(
                    success=False,
                    message=self.messages.get('api_error', 'Erro ao verificar CEP')
                )
        
        return ValidationResult(
            success=True,
            message=self.messages.get('success', 'CEP válido')
        )

class EmailValidator(Validator):
    """Validação de endereços de e-mail."""
    
    def __init__(self):
        super().__init__()
        self.messages = messages.get('validations.email', {})
    
    def validate(self, email: str) -> ValidationResult:
        """Valida um endereço de e-mail."""
        import re
        
        # Expressão regular para e-mail
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if not re.match(pattern, email):
            return ValidationResult(
                success=False,
                message=self.messages.get('invalid_format', 'E-mail inválido')
            )
        
        return ValidationResult(
            success=True,
            message=self.messages.get('success', 'E-mail válido')
        )

class SenhaValidator(Validator):
    """Validação de senhas."""
    
    def __init__(self, min_length: int = 8, require_special: bool = True):
        super().__init__()
        self.min_length = min_length
        self.require_special = require_special
        self.messages = messages.get('validations.senha', {})
    
    def validate(self, senha: str) -> ValidationResult:
        """Valida uma senha."""
        # Verifica comprimento mínimo
        if len(senha) < self.min_length:
            return ValidationResult(
                success=False,
                message=self.messages.get('invalid_length', 
                    f'Senha deve ter no mínimo {self.min_length} caracteres')
            )
        
        # Verifica caracteres especiais
        if self.require_special and not any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in senha):
            return ValidationResult(
                success=False,
                message=self.messages.get('no_special', 
                    'Senha deve conter pelo menos um caractere especial')
            )
        
        # Verifica números
        if not any(c.isdigit() for c in senha):
            return ValidationResult(
                success=False,
                message=self.messages.get('no_number', 
                    'Senha deve conter pelo menos um número')
            )
        
        # Verifica letras maiúsculas
        if not any(c.isupper() for c in senha):
            return ValidationResult(
                success=False,
                message=self.messages.get('no_upper', 
                    'Senha deve conter pelo menos uma letra maiúscula')
            )
        
        return ValidationResult(
            success=True,
            message=self.messages.get('success', 'Senha válida')
        ) 