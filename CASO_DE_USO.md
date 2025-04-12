# Guias do PyQuent - CASO DE USO

## 1. Criando um Novo Projeto

### 1.1 Comando Básico

```bash
pyquent new nome_do_projeto
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
   - Instala o PyQuent e suas dependências
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
pyquent make:model NomeDoModelo
```

### 2.2 Opções Disponíveis

```bash
# Criar modelo com migração
pyquent make:model NomeDoModelo --migration

# Criar modelo com seeder
pyquent make:model NomeDoModelo --seeder

# Criar modelo com controller
pyquent make:model NomeDoModelo --controller

# Criar modelo com todas as opções
pyquent make:model NomeDoModelo --all
```

### 2.3 Exemplo: Criando um Modelo de Usuário

```bash
pyquent make:model User --migration
```

Isso criará:

1. **Modelo** (`app/models/user.py`):
```python
from pyquent import Model, Column

class User(Model):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
```

2. **Migração** (`database/migrations/YYYYMMDDHHMMSS_create_users_table.py`):
```python
from pyquent import Migration

class CreateUsersTable(Migration):
    def up(self):
        self.create_table('users', [
            'id INTEGER PRIMARY KEY AUTOINCREMENT',
            'created_at DATETIME',
            'updated_at DATETIME'
        ])

    def down(self):
        self.drop_table('users')
```

## 3. Caso de Uso: Sistema Financeiro

# Sistema Financeiro com PyQuent

Este é um guia passo a passo para criar um sistema financeiro completo usando o PyQuent ORM.

## 1. Configuração Inicial do Projeto

### 1.1 Criando o Projeto

Primeiro, vamos criar um novo projeto usando o CLI do PyQuent:

```bash
pyquent new sistema_financeiro
```

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
   - Instala o PyQuent e suas dependências
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

### 1.2 Estrutura do Projeto

Após a criação, você terá a seguinte estrutura:

```
sistema_financeiro/
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

### 1.3 Configuração do Ambiente

1. Entre no diretório do projeto:
```bash
cd sistema_financeiro
```

2. Se o ambiente virtual não foi ativado automaticamente, ative-o:
```bash
# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

3. Configure o arquivo `.env`:
```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas configurações:
```
DB_CONNECTION=sqlite
DB_DATABASE=database.sqlite
```

4. Verifique se tudo está configurado corretamente:
```bash
# Verificar versão do PyQuent
pyquent --version

# Verificar status do ambiente
pyquent env:status
```

## 2. Modelagem do Sistema

### 2.1 Criando os Modelos

Vamos criar os modelos necessários para o sistema:

#### 2.1.1 Usuário (app/models/user.py)
```python
from pyquent import Model, Column, relationship

class User(Model):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    
    lancamentos = relationship('Lancamento', back_populates='user')
```

#### 2.1.2 Cliente (app/models/cliente.py)
```python
from pyquent import Model, Column, relationship

class Cliente(Model):
    __tablename__ = 'tbl_clientes'
    
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    cpf_cnpj = Column(String(20), unique=True, nullable=False)
    email = Column(String(100))
    telefone = Column(String(20))
    
    contas_receber = relationship('ContaReceber', back_populates='cliente')
    
    def validar_cpf_cnpj(self):
        # Implementar validação de CPF/CNPJ
        pass
```

[Continua com outros modelos...]

## 3. Migrações e Seeders

### 3.1 Criando as Migrações

```bash
pyquent make:migration create_users_table
pyquent make:migration create_clientes_table
pyquent make:migration create_fornecedores_table
pyquent make:migration create_bancos_table
pyquent make:migration create_contas_bancarias_table
pyquent make:migration create_cartoes_table
pyquent make:migration create_contas_pagar_table
pyquent make:migration create_contas_receber_table
pyquent make:migration create_lancamentos_table
```

### 3.2 Executando as Migrações

```bash
pyquent migrate
```

### 3.3 Criando Seeders

```bash
pyquent make:seeder UsersSeeder
pyquent make:seeder ClientesSeeder
pyquent make:seeder FornecedoresSeeder
```

### 3.4 Executando os Seeders

```bash
pyquent db:seed
```

## 4. Exemplos de Uso

### 4.1 Cadastrando um Cliente

```python
from app.models import Cliente

cliente = Cliente()
cliente.nome = "João Silva"
cliente.cpf_cnpj = "123.456.789-00"
cliente.email = "joao@email.com"
cliente.telefone = "(11) 99999-9999"
cliente.save()
```

### 4.2 Registrando uma Conta a Receber

```python
from app.models import ContaReceber
from datetime import datetime

conta = ContaReceber()
conta.cliente_id = 1
conta.descricao = "Venda #123"
conta.valor = 1500.00
conta.data_vencimento = datetime(2024, 12, 31)
conta.save()
```

### 4.3 Consultando Contas em Atraso

```python
from app.models import ContaPagar
from datetime import datetime

contas_atrasadas = ContaPagar.where('data_vencimento', '<', datetime.now())\
                            .whereNull('data_pagamento')\
                            .get()
```

## 5. Relatórios

### 5.1 Fluxo de Caixa

```python
from app.models import Lancamento
from datetime import datetime, timedelta

inicio = datetime.now()
fim = inicio + timedelta(days=30)

receitas = Lancamento.whereBetween('data', [inicio, fim])\
                    .where('tipo', 'receita')\
                    .sum('valor')

despesas = Lancamento.whereBetween('data', [inicio, fim])\
                    .where('tipo', 'despesa')\
                    .sum('valor')

saldo = receitas - despesas
```

### 5.2 Contas a Pagar por Fornecedor

```python
from app.models import ContaPagar, Fornecedor

fornecedor = Fornecedor.find(1)
total_devido = fornecedor.contas_pagar\
                        .whereNull('data_pagamento')\
                        .sum('valor')
```

## 6. Boas Práticas

1. **Validações**: Sempre valide os dados antes de salvar
2. **Transações**: Use transações para operações que envolvem múltiplas tabelas
3. **Eventos**: Use eventos para ações após salvar/atualizar registros
4. **Logs**: Mantenha logs de todas as operações financeiras
5. **Backup**: Configure backups automáticos do banco de dados

## 7. Próximos Passos

1. Implementar autenticação e autorização
2. Adicionar validações personalizadas
3. Criar interface web ou API
4. Implementar relatórios avançados
5. Configurar backups automáticos
6. Adicionar testes automatizados

## Validações no Sistema Financeiro

### Validação de Documentos

#### Clientes
```python
from pyquent.utils.validators import validar_cpf_cnpj

class Cliente(Model):
    @validates('cpf_cnpj')
    def validar_documento(self, key, value):
        if not validar_cpf_cnpj(value):
            raise ValueError('CPF/CNPJ inválido')
        return value

# Exemplo de uso
try:
    cliente = Cliente.create(
        nome='João Silva',
        cpf_cnpj='123.456.789-09'
    )
except ValueError as e:
    print(f'Erro ao criar cliente: {e}')
```

#### Fornecedores
```python
class Fornecedor(Model):
    @validates('cpf_cnpj')
    def validar_documento(self, key, value):
        if not validar_cpf_cnpj(value):
            raise ValueError('CPF/CNPJ inválido')
        return value

# Exemplo de uso
try:
    fornecedor = Fornecedor.create(
        nome='Empresa XYZ',
        cpf_cnpj='12.345.678/0001-95'
    )
except ValueError as e:
    print(f'Erro ao criar fornecedor: {e}')
```

### Validação de Dados Bancários

#### Contas Bancárias
```python
from pyquent.utils.validators import (
    validar_agencia,
    validar_conta,
    validar_digito
)

class ContaBancaria(Model):
    @validates('agencia')
    def validar_agencia(self, key, value):
        if not validar_agencia(value):
            raise ValueError('Agência inválida')
        return value

    @validates('conta')
    def validar_conta(self, key, value):
        if not validar_conta(value):
            raise ValueError('Conta inválida')
        return value

    @validates('digito')
    def validar_digito(self, key, value):
        if not validar_digito(value):
            raise ValueError('Dígito verificador inválido')
        return value

# Exemplo de uso
try:
    conta = ContaBancaria.create(
        banco_id=1,
        agencia='1234',
        conta='12345-6',
        digito='7'
    )
except ValueError as e:
    print(f'Erro ao criar conta: {e}')
```

### Validação de Transações

#### Lançamentos
```python
class Lancamento(Model):
    @validates('valor')
    def validar_valor(self, key, value):
        if value <= 0:
            raise ValueError('O valor deve ser maior que zero')
        return value

    @validates('data')
    def validar_data(self, key, value):
        if value > datetime.now():
            raise ValueError('A data não pode ser futura')
        return value

    @validates('tipo')
    def validar_tipo(self, key, value):
        if value not in ['entrada', 'saida']:
            raise ValueError('Tipo inválido. Use "entrada" ou "saida"')
        return value

# Exemplo de uso
try:
    lancamento = Lancamento.create(
        user_id=1,
        tipo='entrada',
        descricao='Salário',
        valor=5000.00,
        data=datetime.now()
    )
except ValueError as e:
    print(f'Erro ao criar lançamento: {e}')
```

### Boas Práticas de Validação

1. **Validação em Massa**:
   ```python
   # Validar múltiplos documentos
   documentos = ['123.456.789-09', '12.345.678/0001-95']
   for doc in documentos:
       if validar_cpf_cnpj(doc):
           print(f'{doc} é válido')
   ```

2. **Validação com Mensagens Personalizadas**:
   ```python
   @validates('cpf_cnpj')
   def validar_documento(self, key, value):
       if not validar_cpf_cnpj(value):
           raise ValueError(f'O documento {value} é inválido para {self.nome}')
       return value
   ```

3. **Validação Condicional**:
   ```python
   @validates('cpf_cnpj')
   def validar_documento(self, key, value):
       if self.tipo == 'PF' and not validar_cpf(value):
           raise ValueError('CPF inválido para pessoa física')
       elif self.tipo == 'PJ' and not validar_cnpj(value):
           raise ValueError('CNPJ inválido para pessoa jurídica')
       return value
   ```

4. **Validação com Observadores**:
   ```python
   @observes('before_save')
   def validar_antes_de_salvar(self):
       if not validar_cpf_cnpj(self.cpf_cnpj):
           raise ValueError('Documento inválido')
   ```

from app.models.base import Cliente, ContaBancaria
from app.rpa.processamento import ProcessadorClientes

# Criar processador
processador = ProcessadorClientes(
    arquivo_clientes='clientes.xlsx',
    arquivo_contas='contas.xlsx'
)

# Executar processamento
processador.executar()

from app.models.base import Cliente, ContaBancaria
from app.api.routes import app

# Iniciar servidor
if __name__ == '__main__':
    app.run(debug=True)

from app.models.base import Cliente

class ClienteEspecial(Cliente):
    """Cliente com funcionalidades adicionais."""
    
    def validar_limite_credito(self):
        """Valida limite de crédito do cliente."""
        # Implemente sua lógica aqui
        pass
        
    def calcular_score(self):
        """Calcula score do cliente."""
        # Implemente sua lógica aqui
        pass 