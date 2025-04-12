"""
Validações específicas para modelos do QuentORM.

Este arquivo contém validações customizadas para os modelos
do sistema financeiro.
"""

from typing import Dict, Any, Optional
from datetime import datetime

from quentorm.utils.validators import Validator, ValidationResult
from config.validators.custom_validators import (
    CustomEmailValidator,
    CustomCPFValidator,
    CustomSenhaValidator
)
from config.settings import Settings

class UsuarioValidator(Validator):
    """
    Validador para o modelo de Usuário.
    
    Implementa regras de validação específicas para usuários
    do sistema financeiro.
    """
    
    def __init__(self):
        """Inicializa o validador com o idioma configurado."""
        super().__init__()
        self.locale = Settings.APP_LOCALE
    
    def validate(self, data: Dict[str, Any]) -> ValidationResult:
        """
        Valida os dados de um usuário.
        
        Args:
            data: Dicionário contendo os campos do usuário
            
        Returns:
            ValidationResult: Resultado da validação
        """
        result = ValidationResult()
        
        # Valida nome
        nome = data.get('nome', '')
        if not nome:
            result.add_error('nome', self.get_message('errors.invalid_name'))
        elif len(nome) < 3:
            result.add_error('nome', self.get_message('errors.invalid_name'))
            
        # Valida e-mail
        email_result = CustomEmailValidator().validate({'email': data.get('email', '')})
        if not email_result.is_valid():
            result.add_error('email', self.get_message('validations.email.invalid'))
            
        # Valida senha
        senha = data.get('senha', '')
        if not senha:
            result.add_error('senha', self.get_message('validations.password.invalid'))
        else:
            senha_result = CustomSenhaValidator().validate(senha)
            if not senha_result.is_valid():
                result.add_error('senha', senha_result.get_errors()[0])
            
        return result

class ClienteValidator(Validator):
    """
    Validador para o modelo de Cliente.
    
    Implementa regras de validação específicas para clientes
    do sistema financeiro.
    """
    
    def __init__(self):
        """Inicializa o validador com o idioma configurado."""
        super().__init__()
        self.locale = Settings.APP_LOCALE
    
    def validate(self, data: Dict[str, Any]) -> ValidationResult:
        """
        Valida os dados de um cliente.
        
        Args:
            data: Dicionário contendo os campos do cliente
            
        Returns:
            ValidationResult: Resultado da validação
        """
        result = ValidationResult()
        
        # Valida nome
        nome = data.get('nome', '')
        if not nome:
            result.add_error('nome', self.get_message('errors.invalid_name'))
        elif len(nome) < 3:
            result.add_error('nome', self.get_message('errors.invalid_name'))
            
        # Valida CPF
        cpf_result = CustomCPFValidator().validate({'cpf': data.get('cpf', '')})
        if not cpf_result.is_valid():
            result.add_error('cpf', cpf_result.get_errors()[0])
            
        # Valida e-mail
        email = data.get('email', '')
        if email:  # E-mail é opcional
            email_result = CustomEmailValidator().validate({'email': email})
            if not email_result.is_valid():
                result.add_error('email', email_result.get_errors()[0])
                
        return result 