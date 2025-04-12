"""
Comando para criar novos projetos QuentORM.

Este módulo fornece comandos para criar novos projetos QuentORM,
com opção de criar apenas a estrutura de banco de dados.
"""

import os
import click
from jinja2 import Template
import shutil

@click.command()
@click.argument('nome')
@click.option('--only-db', is_flag=True, default=False,
              help='Criar apenas estrutura de banco de dados, sem interfaces')
@click.option('--venv/--no-venv', default=True,
              help='Criar ambiente virtual')
def new(nome, only_db, venv):
    """
    Cria um novo projeto QuentORM.
    
    Args:
        nome: Nome do projeto
        only_db: Se deve criar apenas estrutura de banco
        venv: Se deve criar ambiente virtual
    """
    # Cria diretório do projeto
    if not os.path.exists(nome):
        os.makedirs(nome)
        
    # Estrutura básica (sempre criada)
    diretorios_base = [
        'app/models',
        'app/database/migrations',
        'app/database/seeders',
        'app/utils',
        'app/config',
        'tests'
    ]
    
    # Estrutura de views (criada apenas se não for only_db)
    diretorios_view = [
        'app/views',
        'app/templates',
        'app/static/css',
        'app/static/js',
        'app/static/img'
    ]
    
    # Cria estrutura base
    for dir in diretorios_base:
        os.makedirs(os.path.join(nome, dir), exist_ok=True)
        
    # Cria estrutura de views se necessário
    if not only_db:
        for dir in diretorios_view:
            os.makedirs(os.path.join(nome, dir), exist_ok=True)
    
    # Template do arquivo .env
    env_template = Template("""# Configurações do Banco de Dados
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE={{ nome }}
DB_USERNAME=root
DB_PASSWORD=

# Configurações da Aplicação
APP_NAME={{ nome }}
APP_ENV=development
APP_DEBUG=true
{% if not only_db %}
# Configurações do Servidor Web
APP_HOST=127.0.0.1
APP_PORT=5000
{% endif %}""")
    
    # Template do README
    readme_template = Template("""# {{ nome }}

## Sobre o Projeto

Este projeto foi gerado com QuentORM.

## Configuração

1. Clone o repositório
2. Crie um ambiente virtual (opcional):
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\\Scripts\\activate   # Windows
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure o arquivo .env
5. Execute as migrações:
   ```bash
   quentorm migrate
   ```
{% if not only_db %}
6. Inicie o servidor:
   ```bash
   quentorm serve
   ```
{% endif %}

## Estrutura do Projeto

```
{{ nome }}/
├── app/
│   ├── models/        # Modelos do banco de dados
│   ├── database/      # Migrações e seeders
│   ├── config/        # Configurações
│   ├── utils/         # Utilitários{% if not only_db %}
│   ├── views/         # Views da aplicação
│   ├── templates/     # Templates HTML
│   └── static/        # Arquivos estáticos{% endif %}
├── tests/            # Testes
├── .env             # Variáveis de ambiente
└── requirements.txt  # Dependências
```

## Comandos Disponíveis

```bash
# Migrações
quentorm migrate           # Executar migrações
quentorm migrate:rollback  # Reverter migrações
quentorm migrate:fresh     # Recriar banco de dados

# Seeders
quentorm db:seed          # Popular banco de dados{% if not only_db %}

# Servidor
quentorm serve            # Iniciar servidor de desenvolvimento{% endif %}
```""")
    
    # Template do requirements.txt
    requirements_template = Template("""# Dependências do QuentORM
quentorm>=1.0.0
python-dotenv>=0.19.0
SQLAlchemy>=1.4.0
alembic>=1.7.0{% if not only_db %}

# Dependências Web
flask>=2.0.0
flask-sqlalchemy>=2.5.0
flask-migrate>=3.1.0{% endif %}

# Dependências de Desenvolvimento
pytest>=6.0.0
pytest-cov>=2.0.0""")
    
    # Gera arquivo .env
    with open(os.path.join(nome, '.env'), 'w', encoding='utf-8') as f:
        f.write(env_template.render(
            nome=nome,
            only_db=only_db
        ))
    
    # Gera README.md
    with open(os.path.join(nome, 'README.md'), 'w', encoding='utf-8') as f:
        f.write(readme_template.render(
            nome=nome,
            only_db=only_db
        ))
    
    # Gera requirements.txt
    with open(os.path.join(nome, 'requirements.txt'), 'w', encoding='utf-8') as f:
        f.write(requirements_template.render(
            only_db=only_db
        ))
    
    # Cria ambiente virtual se solicitado
    if venv:
        click.echo(f"\nCriando ambiente virtual...")
        os.system(f"python -m venv {os.path.join(nome, 'venv')}")
    
    # Mensagem de sucesso
    click.echo(f"\n✓ Projeto {nome} criado com sucesso!")
    if only_db:
        click.echo("  Modo: Apenas banco de dados (sem interfaces)")
    
    # Próximos passos
    click.echo("\nPróximos passos:")
    if venv:
        click.echo("1. Ative o ambiente virtual:")
        if os.name == 'nt':  # Windows
            click.echo(f"   {nome}\\venv\\Scripts\\activate")
        else:  # Linux/Mac
            click.echo(f"   source {nome}/venv/bin/activate")
    click.echo(f"2. Entre no diretório do projeto: cd {nome}")
    click.echo("3. Instale as dependências: pip install -r requirements.txt")
    click.echo("4. Configure o arquivo .env")
    click.echo("5. Execute as migrações: quentorm migrate")
    if not only_db:
        click.echo("6. Inicie o servidor: quentorm serve") 