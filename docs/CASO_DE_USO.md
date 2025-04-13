# Guias do QuentORM - CASO DE USO

## 1. Criando um Novo Projeto

### 1.1 Comando Básico

```bash
quentorm new nome_do_projeto
```

### 1.2 Processo Interativo

O CLI irá guiar você através de um processo interativo:

1. **Estrutura do Projeto**:
   ```
   Deseja criar a estrutura básica do projeto? [S/n]
   ```
   - Cria diretórios e arquivos necessários
   - Configura o ambiente básico
   - Gera arquivos __init__.py em cada diretório

2. **Ambiente Virtual**:
   ```
   Deseja criar um ambiente virtual? [S/n]
   ```
   - Cria o diretório `venv/` dentro do projeto
   - Configura o ambiente Python isolado

3. **Ativação do Ambiente**:
   ```
   Deseja ativar o ambiente virtual? [S/n]
   ```
   - Ativa o ambiente virtual automaticamente
   - Configura as variáveis de ambiente necessárias
   - Permite instalação de dependências

4. **Dependências**:
   ```
   Deseja instalar as dependências do projeto? [S/n]
   ```
   - Instala o QuentORM e suas dependências
   - Configura o ambiente para desenvolvimento

5. **Arquivos de Configuração**:
   ```
   Deseja criar os arquivos de configuração? [S/n]
   ```
   - Cria `.env.example` com configurações padrão
   - Gera `requirements.txt` com dependências
   - Cria `README.md` com instruções básicas

6. **Controle de Versão**:
   ```
   Deseja inicializar um repositório Git? [S/n]
   ```
   - Inicializa um repositório Git
   - Cria `.gitignore` com padrões Python
   - Faz commit inicial do projeto

### 1.3 Estrutura do Projeto

Após a criação, você terá a seguinte estrutura:

```
nome_do_projeto/
├── app/
│   ├── models/
│   │   └── __init__.py
│   ├── controllers/
│   │   └── __init__.py
│   └── views/
│       └── __init__.py
├── config/
│   └── __init__.py
├── database/
│   ├── migrations/
│   │   └── __init__.py
│   └── seeders/
│       └── __init__.py
├── tests/
│   └── __init__.py
├── venv/
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

## 2. Criando um Modelo

### 2.1 Comando Básico

```bash
quentorm make model Usuario
```

### 2.2 Opções Disponíveis

```bash
# Criar modelo com migração
quentorm make model Usuario --migration

# Criar modelo com seeder
quentorm make model Usuario --seeder

# Criar modelo com controller
quentorm make model Usuario --controller

# Criar modelo com todas as opções
quentorm make model Usuario --all
```

### 2.3 Exemplo: Criando um Modelo de Usuário

```bash
quentorm make model Usuario --migration
```

Isso criará:

1. **Modelo** (`app/models/usuario.py`):
```python
from quentorm import Model, Column

class Usuario(Model):
    __tablename__ = 'usuarios'
    
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
```

2. **Migração** (`database/migrations/YYYYMMDDHHMMSS_create_usuarios_table.py`):
```python
from quentorm import Migration

class CreateUsuariosTable(Migration):
    def up(self):
        self.create_table('usuarios', [
            'id INTEGER PRIMARY KEY AUTOINCREMENT',
            'created_at DATETIME',
            'updated_at DATETIME'
        ])

    def down(self):
        self.drop_table('usuarios')
```

## 3. Caso de Uso: Sistema Financeiro

# Tutorial: Criando seu Primeiro Sistema Financeiro com QuentORM

## Introdução

Olá! Se você está começando a aprender Python e quer criar um sistema financeiro, este tutorial é para você. Vamos criar um sistema completo para gerenciar:

- Contas bancárias
- Contas a pagar
- Contas a receber
- Clientes
- Fornecedores
- Lançamentos financeiros

### O que você vai aprender:

1. Como instalar e configurar o QuentORM
2. Como criar as tabelas do sistema financeiro
3. Como cadastrar contas, clientes e fornecedores
4. Como registrar pagamentos e recebimentos
5. Como gerar relatórios financeiros básicos

### Pré-requisitos:

- Python 3.8 ou superior instalado
- Editor de código (VS Code, PyCharm, etc.)
- Conhecimento básico de Python

## Passo 1: Instalando o QuentORM

Primeiro, vamos instalar o QuentORM. Abra o terminal (PowerShell no Windows) e digite:

```bash
pip install quentorm
```

Se aparecer algum erro, tente:

```bash
python -m pip install quentorm
```

## Passo 2: Criando o Projeto

Vamos criar uma pasta para nosso sistema financeiro:

```bash
# Criar pasta do projeto
mkdir sistema_financeiro
cd sistema_financeiro

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# No Windows:
venv\Scripts\activate
# No Linux/Mac:
source venv/bin/activate
```

## Passo 3: Configurando o Banco de Dados

Crie um arquivo chamado `config.py`:

```python
from quentorm import Database
import os
from dotenv import load_dotenv

# Carrega as variáveis do .env
load_dotenv()

# Cria uma instância do banco de dados
db = Database()

# Configura a conexão
db.config({
    'default': {
        'driver': 'sqlite',
        'database': 'financeiro.db'
    }
})
```

Crie um arquivo `.env`:

```env
DB_CONNECTION=sqlite
DB_DATABASE=financeiro.db
```

## Passo 4: Criando as Tabelas do Sistema Financeiro

Vamos criar um arquivo `models.py` com todas as tabelas necessárias:

```python
from quentorm import Model
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, ForeignKey
from datetime import datetime

# Tabela de Clientes
class Cliente(Model):
    __table__ = 'tbl_cliente'
    
    id = Column(Integer, primary_key=True)
    nome = Column(String(100))
    cpf = Column(String(14), unique=True)
    email = Column(String(100))
    telefone = Column(String(20))
    ativo = Column(Boolean, default=True)
    data_criacao = Column(DateTime, default=datetime.now)

# Tabela de Fornecedores
class Fornecedor(Model):
    __table__ = 'tbl_fornecedor'
    
    id = Column(Integer, primary_key=True)
    nome = Column(String(100))
    cnpj = Column(String(18), unique=True)
    email = Column(String(100))
    telefone = Column(String(20))
    ativo = Column(Boolean, default=True)
    data_criacao = Column(DateTime, default=datetime.now)

# Tabela de Contas Bancárias
class ContaBancaria(Model):
    __table__ = 'tbl_conta_bancaria'
    
    id = Column(Integer, primary_key=True)
    banco = Column(String(100))
    agencia = Column(String(10))
    conta = Column(String(20))
    saldo = Column(Float, default=0.0)
    ativo = Column(Boolean, default=True)
    data_criacao = Column(DateTime, default=datetime.now)

# Tabela de Contas a Pagar
class ContaPagar(Model):
    __table__ = 'tbl_conta_pagar'
    
    id = Column(Integer, primary_key=True)
    fornecedor_id = Column(Integer, ForeignKey('tbl_fornecedor.id'))
    descricao = Column(String(200))
    valor = Column(Float)
    data_vencimento = Column(DateTime)
    data_pagamento = Column(DateTime, nullable=True)
    status = Column(String(20))  # pendente, pago, atrasado
    conta_bancaria_id = Column(Integer, ForeignKey('tbl_conta_bancaria.id'))
    data_criacao = Column(DateTime, default=datetime.now)

# Tabela de Contas a Receber
class ContaReceber(Model):
    __table__ = 'tbl_conta_receber'
    
    id = Column(Integer, primary_key=True)
    cliente_id = Column(Integer, ForeignKey('tbl_cliente.id'))
    descricao = Column(String(200))
    valor = Column(Float)
    data_vencimento = Column(DateTime)
    data_recebimento = Column(DateTime, nullable=True)
    status = Column(String(20))  # pendente, recebido, atrasado
    conta_bancaria_id = Column(Integer, ForeignKey('tbl_conta_bancaria.id'))
    data_criacao = Column(DateTime, default=datetime.now)
```

## Passo 5: Criando as Tabelas no Banco

Crie um arquivo `criar_tabelas.py`:

```python
from config import db
from models import Cliente, Fornecedor, ContaBancaria, ContaPagar, ContaReceber

# Criar as tabelas
Cliente.create_table()
Fornecedor.create_table()
ContaBancaria.create_table()
ContaPagar.create_table()
ContaReceber.create_table()

print("Tabelas do sistema financeiro criadas com sucesso!")
```

Execute o arquivo:

```bash
python criar_tabelas.py
```

## Passo 6: Cadastrando Dados Iniciais

Crie um arquivo `cadastrar_dados.py`:

```python
from models import Cliente, Fornecedor, ContaBancaria, ContaPagar, ContaReceber
from datetime import datetime, timedelta

# Cadastrar um cliente
cliente = Cliente.create(
    nome="Maria Santos",
    cpf="123.456.789-00",
    email="maria@exemplo.com",
    telefone="(11) 99999-9999"
)

# Cadastrar um fornecedor
fornecedor = Fornecedor.create(
    nome="Fornecedor XYZ",
    cnpj="12.345.678/0001-90",
    email="contato@fornecedor.com",
    telefone="(11) 88888-8888"
)

# Cadastrar uma conta bancária
conta = ContaBancaria.create(
    banco="Banco do Brasil",
    agencia="1234",
    conta="56789-0",
    saldo=10000.00
)

# Cadastrar uma conta a pagar
conta_pagar = ContaPagar.create(
    fornecedor_id=fornecedor.id,
    descricao="Aluguel",
    valor=1500.00,
    data_vencimento=datetime.now() + timedelta(days=30),
    status="pendente",
    conta_bancaria_id=conta.id
)

# Cadastrar uma conta a receber
conta_receber = ContaReceber.create(
    cliente_id=cliente.id,
    descricao="Venda de produto",
    valor=500.00,
    data_vencimento=datetime.now() + timedelta(days=15),
    status="pendente",
    conta_bancaria_id=conta.id
)

print("Dados financeiros cadastrados com sucesso!")
```

Execute o arquivo:

```bash
python cadastrar_dados.py
```

## Passo 7: Consultando Dados Financeiros

Crie um arquivo `consultar_dados.py`:

```python
from models import Cliente, Fornecedor, ContaBancaria, ContaPagar, ContaReceber
from datetime import datetime

# Buscar saldo total das contas
contas = ContaBancaria.all()
saldo_total = sum(conta.saldo for conta in contas)
print(f"\nSaldo Total: R$ {saldo_total:.2f}")

# Buscar contas a pagar do mês
hoje = datetime.now()
contas_pagar = ContaPagar.where('data_vencimento', '>=', hoje).get()
print("\nContas a Pagar:")
for conta in contas_pagar:
    print(f"- {conta.descricao}: R$ {conta.valor:.2f} (Vencimento: {conta.data_vencimento.strftime('%d/%m/%Y')})")

# Buscar contas a receber do mês
contas_receber = ContaReceber.where('data_vencimento', '>=', hoje).get()
print("\nContas a Receber:")
for conta in contas_receber:
    print(f"- {conta.descricao}: R$ {conta.valor:.2f} (Vencimento: {conta.data_vencimento.strftime('%d/%m/%Y')})")
```

Execute o arquivo:

```bash
python consultar_dados.py
```

## Passo 8: Atualizando Dados Financeiros

Crie um arquivo `atualizar_dados.py`:

```python
from models import ContaPagar, ContaReceber, ContaBancaria
from datetime import datetime

# Registrar pagamento de uma conta
conta_pagar = ContaPagar.where('status', 'pendente').first()
if conta_pagar:
    conta_pagar.status = "pago"
    conta_pagar.data_pagamento = datetime.now()
    conta_pagar.save()
    
    # Atualizar saldo da conta
    conta = ContaBancaria.find(conta_pagar.conta_bancaria_id)
    conta.saldo -= conta_pagar.valor
    conta.save()
    print("Pagamento registrado com sucesso!")

# Registrar recebimento de uma conta
conta_receber = ContaReceber.where('status', 'pendente').first()
if conta_receber:
    conta_receber.status = "recebido"
    conta_receber.data_recebimento = datetime.now()
    conta_receber.save()
    
    # Atualizar saldo da conta
    conta = ContaBancaria.find(conta_receber.conta_bancaria_id)
    conta.saldo += conta_receber.valor
    conta.save()
    print("Recebimento registrado com sucesso!")
```

Execute o arquivo:

```bash
python atualizar_dados.py
```

## Próximos Passos

Agora que você aprendeu o básico do sistema financeiro, pode:

1. Adicionar mais funcionalidades:
   - Relatórios de fluxo de caixa
   - Controle de cartões de crédito
   - Categorização de despesas
   - Previsão de fluxo de caixa

2. Melhorar o sistema:
   - Adicionar validações de dados
   - Criar uma interface web
   - Implementar autenticação
   - Gerar relatórios em PDF

## Dicas para Iniciantes

1. **Organize suas finanças**: Use o sistema para controlar suas próprias contas
2. **Teste bastante**: Faça simulações antes de usar em produção
3. **Documente**: Anote todas as alterações importantes
4. **Backup**: Faça backup regular do banco de dados
5. **Pratique**: Crie novos relatórios e funcionalidades

## Conclusão

Parabéns! Você criou seu primeiro sistema financeiro usando o QuentORM. Agora você pode:

- Controlar suas contas bancárias
- Gerenciar contas a pagar e receber
- Acompanhar clientes e fornecedores
- Gerar relatórios básicos

Lembre-se:
- Sempre valide os dados antes de salvar
- Faça backup regular do banco de dados
- Teste todas as funcionalidades
- Peça ajuda quando precisar 