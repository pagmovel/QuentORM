"""
Comando para gerar templates de validadores.

Este módulo fornece comandos para criar novos validadores customizados
usando a estrutura padrão do QuentORM.
"""

import os
import click
from jinja2 import Template

@click.group()
def validator():
    """Comandos para gerenciar validadores."""
    pass

@validator.command()
@click.argument('nome')
@click.option('--diretorio', '-d', default='validators',
              help='Diretório onde o validador será criado')
@click.option('--mensagens/--sem-mensagens', default=True,
              help='Gerar arquivo de mensagens')
@click.option('--idioma', '-l', default='pt_br',
              help='Idioma das mensagens (pt_br, en, es, fr)')
def criar(nome, diretorio, mensagens, idioma):
    """
    Cria um novo validador customizado.
    
    Args:
        nome: Nome do validador (ex: Endereco)
        diretorio: Diretório onde o validador será criado
        mensagens: Se deve gerar arquivo de mensagens
        idioma: Idioma das mensagens
    """
    # Template do validador
    template_validador = Template("""\"\"\"
Validador customizado para {{ nome }}.

Este validador foi gerado automaticamente pelo comando quentorm validator criar.
\"\"\"

from typing import Dict, List
from quentorm.utils.validators import Validator, ValidationResult

class {{ nome }}Validator(Validator):
    \"\"\"Validador para {{ nome }}.\"\"\"
    
    def validate(self, valor: str) -> ValidationResult:
        \"\"\"
        Valida um {{ nome }}.
        
        Args:
            valor: Valor a ser validado
            
        Returns:
            ValidationResult com o resultado da validação
        \"\"\"
        errors: List[str] = []
        
        # Implemente suas regras de validação aqui
        # Exemplo:
        if not valor:
            errors.append(self.get_message('{{ nome_lower }}.required'))
            
        if errors:
            return ValidationResult(
                success=False,
                message=self.get_message('{{ nome_lower }}.invalid'),
                errors=errors
            )
            
        return ValidationResult(
            success=True,
            message=self.get_message('{{ nome_lower }}.valid')
        )
""")

    # Template de mensagens
    template_mensagens = Template("""{
    "{{ nome_lower }}": {
        "valid": "{{ nome }} válido",
        "invalid": "{{ nome }} inválido",
        "required": "{{ nome }} é obrigatório"
    }
}""")

    # Cria diretório se não existir
    if not os.path.exists(diretorio):
        os.makedirs(diretorio)
        
    # Gera arquivo do validador
    nome_arquivo = f"{nome.lower()}_validator.py"
    caminho_validador = os.path.join(diretorio, nome_arquivo)
    
    with open(caminho_validador, 'w', encoding='utf-8') as f:
        f.write(template_validador.render(
            nome=nome,
            nome_lower=nome.lower()
        ))
        
    click.echo(f"✓ Validador criado em {caminho_validador}")
    
    # Gera arquivo de mensagens se solicitado
    if mensagens:
        diretorio_mensagens = os.path.join(diretorio, 'messages')
        if not os.path.exists(diretorio_mensagens):
            os.makedirs(diretorio_mensagens)
            
        nome_arquivo = f"{idioma}.json"
        caminho_mensagens = os.path.join(diretorio_mensagens, nome_arquivo)
        
        with open(caminho_mensagens, 'w', encoding='utf-8') as f:
            f.write(template_mensagens.render(
                nome=nome,
                nome_lower=nome.lower()
            ))
            
        click.echo(f"✓ Mensagens criadas em {caminho_mensagens}")
    
    click.echo("\nPróximos passos:")
    click.echo(f"1. Implemente as regras de validação em {nome_arquivo}")
    click.echo("2. Adicione mensagens personalizadas no arquivo de mensagens")
    click.echo(f"3. Importe e use o {nome}Validator em seu código")

@validator.command()
@click.argument('nome')
@click.option('--diretorio', '-d', default='validators',
              help='Diretório onde o validador será criado')
def remover(nome, diretorio):
    """
    Remove um validador existente.
    
    Args:
        nome: Nome do validador a ser removido
        diretorio: Diretório onde o validador está
    """
    nome_arquivo = f"{nome.lower()}_validator.py"
    caminho_validador = os.path.join(diretorio, nome_arquivo)
    
    if os.path.exists(caminho_validador):
        os.remove(caminho_validador)
        click.echo(f"✓ Validador removido: {caminho_validador}")
    else:
        click.echo(f"Validador não encontrado: {caminho_validador}")
        
    # Remove mensagens
    diretorio_mensagens = os.path.join(diretorio, 'messages')
    for idioma in ['pt_br', 'en', 'es', 'fr']:
        caminho_mensagens = os.path.join(diretorio_mensagens, f"{idioma}.json")
        if os.path.exists(caminho_mensagens):
            os.remove(caminho_mensagens)
            click.echo(f"✓ Mensagens removidas: {caminho_mensagens}")

@validator.command()
@click.argument('nome')
@click.option('--diretorio', '-d', default='validators',
              help='Diretório onde o validador está')
def listar_mensagens(nome, diretorio):
    """
    Lista as mensagens disponíveis para um validador.
    
    Args:
        nome: Nome do validador
        diretorio: Diretório onde o validador está
    """
    diretorio_mensagens = os.path.join(diretorio, 'messages')
    
    for idioma in ['pt_br', 'en', 'es', 'fr']:
        caminho = os.path.join(diretorio_mensagens, f"{idioma}.json")
        if os.path.exists(caminho):
            click.echo(f"\nMensagens em {idioma}:")
            with open(caminho, 'r', encoding='utf-8') as f:
                click.echo(f.read()) 