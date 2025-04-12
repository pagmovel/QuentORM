"""
Comandos para criar arquivos do projeto
"""

import os
import click
from datetime import datetime
from pathlib import Path

@click.group('make')
def make_command():
    """Comandos para criar arquivos do projeto"""
    pass

@make_command.command('model')
@click.argument('name')
@click.option('--migration', is_flag=True, help='Criar migração para o modelo')
@click.option('--seeder', is_flag=True, help='Criar seeder para o modelo')
@click.option('--controller', is_flag=True, help='Criar controller para o modelo')
@click.option('--all', is_flag=True, help='Criar todos os arquivos relacionados')
def make_model(name, migration, seeder, controller, all):
    """Cria um novo modelo e arquivos relacionados"""
    
    # Criar modelo
    create_model(name)
    click.echo(f"✓ Modelo {name} criado com sucesso!")
    
    # Criar migração se solicitado
    if migration or all:
        create_migration(name)
        click.echo(f"✓ Migração para {name} criada com sucesso!")
    
    # Criar seeder se solicitado
    if seeder or all:
        create_seeder(name)
        click.echo(f"✓ Seeder para {name} criado com sucesso!")
    
    # Criar controller se solicitado
    if controller or all:
        create_controller(name)
        click.echo(f"✓ Controller para {name} criado com sucesso!")

def create_model(name):
    """Cria o arquivo do modelo"""
    model_path = os.path.join('app', 'models', f"{name.lower()}.py")
    
    # Criar diretório se não existir
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    
    # Criar arquivo do modelo
    with open(model_path, 'w') as f:
        f.write(f"""from quentorm import Model, Column
from datetime import datetime

class {name}(Model):
    __tablename__ = '{name.lower()}s'
    
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
""")

def create_migration(name):
    """Cria o arquivo de migração"""
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    migration_path = os.path.join('database', 'migrations', f"{timestamp}_create_{name.lower()}s_table.py")
    
    # Criar diretório se não existir
    os.makedirs(os.path.dirname(migration_path), exist_ok=True)
    
    # Criar arquivo de migração
    with open(migration_path, 'w') as f:
        f.write(f"""from quentorm import Migration

class Create{name}sTable(Migration):
    def up(self):
        self.create_table('{name.lower()}s', [
            'id INTEGER PRIMARY KEY AUTOINCREMENT',
            'created_at DATETIME',
            'updated_at DATETIME'
        ])

    def down(self):
        self.drop_table('{name.lower()}s')
""")

def create_seeder(name):
    """Cria o arquivo de seeder"""
    seeder_path = os.path.join('database', 'seeders', f"{name}Seeder.py")
    
    # Criar diretório se não existir
    os.makedirs(os.path.dirname(seeder_path), exist_ok=True)
    
    # Criar arquivo de seeder
    with open(seeder_path, 'w') as f:
        f.write(f"""from quentorm import Seeder
from app.models.{name.lower()} import {name}

class {name}Seeder(Seeder):
    def run(self):
        # Adicione seus dados de seed aqui
        pass
""")

def create_controller(name):
    """Cria o arquivo do controller"""
    controller_path = os.path.join('app', 'controllers', f"{name.lower()}_controller.py")
    
    # Criar diretório se não existir
    os.makedirs(os.path.dirname(controller_path), exist_ok=True)
    
    # Criar arquivo do controller
    with open(controller_path, 'w') as f:
        f.write(f"""from app.models.{name.lower()} import {name}

class {name}Controller:
    def index(self):
        return {name}.all()
    
    def show(self, id):
        return {name}.find(id)
    
    def store(self, data):
        return {name}.create(data)
    
    def update(self, id, data):
        model = {name}.find(id)
        model.update(data)
        return model
    
    def destroy(self, id):
        model = {name}.find(id)
        model.delete()
        return True
""") 