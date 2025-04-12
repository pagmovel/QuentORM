"""
Módulo de validações do QuentORM

Este módulo contém funções de validação para diferentes tipos de dados,
como documentos (CPF, CNPJ) e dados bancários (agência, conta, dígito).

Cada função de validação:
1. Recebe um valor para validar
2. Retorna um objeto ValidationResult com:
   - success: bool (True se válido, False se inválido)
   - message: str (mensagem de sucesso ou erro)
   - errors: list (lista de erros específicos)

Exemplo de uso:
    from quentorm.utils.validators import validar_cpf
    
    resultado = validar_cpf('123.456.789-09')
    if resultado.success:
        print(resultado.message)  # "CPF válido"
    else:
        print(resultado.errors)   # Lista de erros
"""

import re
import json
import os
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class ValidationResult:
    """Resultado de uma validação"""
    success: bool
    message: str
    errors: List[str]

class Validator:
    """Classe base para validações"""
    
    def __init__(self, lang: str = 'pt_br'):
        """Inicializa o validador com o idioma especificado"""
        self.lang = lang
        self.messages = self._load_messages()
    
    def _load_messages(self) -> dict:
        """Carrega as mensagens do arquivo JSON"""
        messages_path = os.path.join(
            os.path.dirname(__file__),
            'messages',
            f'{self.lang}.json'
        )
        with open(messages_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _get_message(self, path: str) -> str:
        """Obtém uma mensagem do arquivo de configuração"""
        parts = path.split('.')
        current = self.messages
        for part in parts:
            current = current.get(part, {})
        return current if isinstance(current, str) else ""

class DocumentValidator(Validator):
    """Validador de documentos (CPF, CNPJ)"""
    
    def validar_cpf(self, cpf: str) -> ValidationResult:
        """Valida um número de CPF"""
        errors = []
        
        # Remove caracteres não numéricos
        cpf = re.sub(r'[^0-9]', '', cpf)
        
        # Verifica se tem 11 dígitos
        if len(cpf) != 11:
            errors.append(self._get_message('validations.cpf.invalid_length'))
            return ValidationResult(False, "", errors)
        
        # Verifica se todos os dígitos são iguais
        if cpf == cpf[0] * 11:
            errors.append(self._get_message('validations.cpf.all_same_digits'))
            return ValidationResult(False, "", errors)
        
        # Calcula primeiro dígito verificador
        soma = 0
        for i in range(9):
            soma += int(cpf[i]) * (10 - i)
        resto = 11 - (soma % 11)
        if resto > 9:
            resto = 0
        if resto != int(cpf[9]):
            errors.append(self._get_message('validations.cpf.invalid_check_digit'))
            return ValidationResult(False, "", errors)
        
        # Calcula segundo dígito verificador
        soma = 0
        for i in range(10):
            soma += int(cpf[i]) * (11 - i)
        resto = 11 - (soma % 11)
        if resto > 9:
            resto = 0
        if resto != int(cpf[10]):
            errors.append(self._get_message('validations.cpf.invalid_check_digit'))
            return ValidationResult(False, "", errors)
        
        return ValidationResult(True, self._get_message('validations.cpf.success'), [])
    
    def validar_cnpj(self, cnpj: str) -> ValidationResult:
        """Valida um número de CNPJ"""
        errors = []
        
        # Remove caracteres não numéricos
        cnpj = re.sub(r'[^0-9]', '', cnpj)
        
        # Verifica se tem 14 dígitos
        if len(cnpj) != 14:
            errors.append(self._get_message('validations.cnpj.invalid_length'))
            return ValidationResult(False, "", errors)
        
        # Verifica se todos os dígitos são iguais
        if cnpj == cnpj[0] * 14:
            errors.append(self._get_message('validations.cnpj.all_same_digits'))
            return ValidationResult(False, "", errors)
        
        # Calcula primeiro dígito verificador
        soma = 0
        peso = 5
        for i in range(12):
            soma += int(cnpj[i]) * peso
            peso = 9 if peso == 2 else peso - 1
        resto = 11 - (soma % 11)
        if resto > 9:
            resto = 0
        if resto != int(cnpj[12]):
            errors.append(self._get_message('validations.cnpj.invalid_check_digit'))
            return ValidationResult(False, "", errors)
        
        # Calcula segundo dígito verificador
        soma = 0
        peso = 6
        for i in range(13):
            soma += int(cnpj[i]) * peso
            peso = 9 if peso == 2 else peso - 1
        resto = 11 - (soma % 11)
        if resto > 9:
            resto = 0
        if resto != int(cnpj[13]):
            errors.append(self._get_message('validations.cnpj.invalid_check_digit'))
            return ValidationResult(False, "", errors)
        
        return ValidationResult(True, self._get_message('validations.cnpj.success'), [])
    
    def validar_cpf_cnpj(self, documento: str) -> ValidationResult:
        """Valida automaticamente um CPF ou CNPJ"""
        # Remove caracteres não numéricos
        documento = re.sub(r'[^0-9]', '', documento)
        
        # Verifica se é CPF (11 dígitos) ou CNPJ (14 dígitos)
        if len(documento) == 11:
            return self.validar_cpf(documento)
        elif len(documento) == 14:
            return self.validar_cnpj(documento)
        else:
            return ValidationResult(
                False,
                "",
                [self._get_message('validations.document.invalid_length')]
            )

class BankValidator(Validator):
    """Validador de dados bancários"""
    
    def validar_agencia(self, agencia: str) -> ValidationResult:
        """Valida um número de agência bancária"""
        errors = []
        
        # Remove caracteres não numéricos
        agencia = re.sub(r'[^0-9]', '', agencia)
        
        # Verifica se tem entre 4 e 10 dígitos
        if len(agencia) < 4 or len(agencia) > 10:
            errors.append(self._get_message('validations.bank.agency.invalid_length'))
            return ValidationResult(False, "", errors)
        
        return ValidationResult(True, self._get_message('validations.bank.agency.success'), [])
    
    def validar_conta(self, conta: str) -> ValidationResult:
        """Valida um número de conta bancária"""
        errors = []
        
        # Remove caracteres não numéricos e hífen
        conta = re.sub(r'[^0-9-]', '', conta)
        
        # Verifica se tem entre 5 e 20 dígitos (excluindo hífen)
        if len(conta.replace('-', '')) < 5 or len(conta.replace('-', '')) > 20:
            errors.append(self._get_message('validations.bank.account.invalid_length'))
            return ValidationResult(False, "", errors)
        
        return ValidationResult(True, self._get_message('validations.bank.account.success'), [])
    
    def validar_digito(self, digito: Optional[str]) -> ValidationResult:
        """Valida um dígito verificador de conta bancária"""
        if not digito:
            return ValidationResult(True, self._get_message('validations.bank.digit.success'), [])
        
        # Remove caracteres não numéricos
        digito = re.sub(r'[^0-9]', '', digito)
        
        # Verifica se tem no máximo 2 dígitos
        if len(digito) > 2:
            return ValidationResult(
                False,
                "",
                [self._get_message('validations.bank.digit.invalid_length')]
            )
        
        return ValidationResult(True, self._get_message('validations.bank.digit.success'), [])

# Instâncias globais para uso direto
document_validator = DocumentValidator()
bank_validator = BankValidator()

# Funções de conveniência
def validar_cpf(cpf: str) -> ValidationResult:
    """Valida um CPF"""
    return document_validator.validar_cpf(cpf)

def validar_cnpj(cnpj: str) -> ValidationResult:
    """Valida um CNPJ"""
    return document_validator.validar_cnpj(cnpj)

def validar_cpf_cnpj(documento: str) -> ValidationResult:
    """Valida automaticamente um CPF ou CNPJ"""
    return document_validator.validar_cpf_cnpj(documento)

def validar_agencia(agencia: str) -> ValidationResult:
    """Valida um número de agência bancária"""
    return bank_validator.validar_agencia(agencia)

def validar_conta(conta: str) -> ValidationResult:
    """Valida um número de conta bancária"""
    return bank_validator.validar_conta(conta)

def validar_digito(digito: Optional[str]) -> ValidationResult:
    """Valida um dígito verificador de conta bancária"""
    return bank_validator.validar_digito(digito) 