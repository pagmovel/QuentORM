# Manual do QuentORM - ORM para Python

## Índice

1. [Introdução](#introdução)
2. [Instalação](#instalação)
3. [Configuração](#configuração)
4. [Conceitos Básicos](#conceitos-básicos)
5. [Modelos](#modelos)
6. [Operações CRUD](#operações-crud)
7. [Consultas](#consultas)
8. [Relacionamentos](#relacionamentos)
9. [Operações em Lote](#operações-em-lote)
10. [Transações](#transações)
11. [Escopos](#escopos)
12. [Eventos](#eventos)
13. [Observadores](#observadores)
14. [Validações](#validações)
15. [Soft Deletes](#soft-deletes)
16. [Cache](#cache)
17. [Boas Práticas](#boas-práticas)
18. [Performance](#performance)
19. [Solução de Problemas](#solução-de-problemas)
20. [Migrações](#migrações)
21. [Seeding](#seeding)
22. [Monitoramento](#monitoramento)
23. [CLI](#cli)

## Introdução

### O que é um ORM?

Imagine que você está aprendendo a programar em Python e precisa trabalhar com um banco de dados. Tradicionalmente, você precisaria escrever comandos SQL como:

```sql
SELECT * FROM users WHERE age > 18;
```

Com um ORM (Object-Relational Mapping), você pode fazer a mesma coisa de forma mais simples:

```python
users = User.where('age', '>', 18).get()
```

O ORM traduz seus comandos em Python para SQL automaticamente. É como ter um tradutor que converte sua linguagem Python para a linguagem do banco de dados.

### Por que usar o QuentORM?

1. **Facilidade de Uso**: Sintaxe intuitiva e similar ao português
2. **Produtividade**: Menos código para escrever e manter
3. **Segurança**: Proteção automática contra erros comuns
4. **Flexibilidade**: Suporte a diferentes bancos de dados
5. **Aprendizado**: Ótimo para quem está começando com Python

### Pré-requisitos

Antes de começar, você precisa ter:

1. **Python instalado**: [Como instalar Python](https://www.python.org/downloads/)
2. **pip**: Gerenciador de pacotes do Python (vem com o Python)
3. **Banco de dados**: MySQL, PostgreSQL ou SQLite
4. **Editor de código**: VS Code, PyCharm ou outro de sua preferência

## Instalação

### Passo 1: Instalar o Python

Se você ainda não tem o Python instalado:

1. Acesse [python.org](https://www.python.org/downloads/)
2. Baixe a versão mais recente
3. Execute o instalador
4. Marque a opção "Add Python to PATH"
5. Clique em "Install Now"

### Passo 2: Verificar a instalação

Abra o terminal (PowerShell no Windows) e digite:

```bash
python --version
```

Se aparecer algo como "Python 3.8.0", está tudo certo!

### Passo 3: Instalar o QuentORM

No terminal, digite:

```bash
pip install quentorm
```

Se você for usar MySQL, também instale:

```bash
pip install quentorm[mysql]
```

Para PostgreSQL:

```bash
pip install quentorm[postgres]
```

Para SQLite:

```bash
pip install quentorm[sqlite]
```

### Passo 4: Verificar a instalação

Crie um arquivo `teste.py`:

```python
import quentorm

print("QuentORM instalado com sucesso!")
print(f"Versão: {quentorm.__version__}")
```

Execute:

```bash
python teste.py
```

Se não aparecer nenhum erro, está tudo pronto!

## Instalação e Configuração Inicial

### 1. Criando um Novo Projeto

O QuentORM oferece um comando CLI para criar novos projetos. Você pode criar projetos completos ou apenas com a estrutura de banco de dados.

## Projeto Completo

Para criar um novo projeto com todas as funcionalidades:

```bash
quentorm new MeuProjeto
```

Isto criará:
1. Estrutura de diretórios completa
2. Arquivos de configuração
3. Ambiente virtual (opcional)
4. Estrutura MVC completa

## Projeto Apenas com Banco de Dados

Para criar um projeto focado apenas em banco de dados, sem interfaces:

```bash
quentorm new MeuProjeto --only-db
```

Isto criará:
1. Estrutura básica de diretórios
   - app/models
   - app/database/migrations
   - app/database/seeders
   - app/utils
   - app/config
   - tests
2. Arquivos de configuração básicos
3. Ambiente virtual (opcional)

### Quando Usar --only-db

Use a opção `--only-db` quando:
1. Desenvolver uma API pura
2. Criar uma biblioteca de acesso a dados
3. Trabalhar apenas com banco de dados
4. Não precisar de interfaces web

### Opções Disponíveis

- `--only-db`: Criar apenas estrutura de banco de dados
- `--venv/--no-venv`: Criar ou não ambiente virtual (padrão: --venv)

### Exemplos

```bash
# Projeto completo com ambiente virtual
quentorm new MeuProjeto

# Projeto apenas DB com ambiente virtual
quentorm new MeuProjeto --only-db

# Projeto apenas DB sem ambiente virtual
quentorm new MeuProjeto --only-db --no-venv
```

### Estrutura Gerada

Com `--only-db`:
```
MeuProjeto/
├── app/
│   ├── models/        # Modelos do banco de dados
│   ├── database/      # Migrações e seeders
│   ├── config/        # Configurações
│   └── utils/         # Utilitários
├── tests/            # Testes
├── .env             # Variáveis de ambiente
└── requirements.txt  # Dependências
```

Sem `--only-db`:
```
MeuProjeto/
├── app/
│   ├── models/        # Modelos do banco de dados
│   ├── database/      # Migrações e seeders
│   ├── config/        # Configurações
│   ├── utils/         # Utilitários
│   ├── views/         # Views da aplicação
│   ├── templates/     # Templates HTML
│   └── static/        # Arquivos estáticos
├── tests/            # Testes
├── .env             # Variáveis de ambiente
└── requirements.txt  # Dependências
```

## Configuração Básica

### O que são arquivos de configuração?

Quando você usa o QuentORM, precisa dizer a ele:
1. Qual banco de dados usar
2. Onde está o banco de dados
3. Como se conectar a ele

Isso é feito através de dois arquivos:
- `.env`: Guarda informações sensíveis (senhas, etc.)
- `config.py`: Configura como o QuentORM deve funcionar

### Criando o arquivo .env

1. Crie um arquivo chamado `.env` na pasta do seu projeto
2. Adicione as configurações:

```env
# Configurações do banco de dados
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=meu_banco
DB_USERNAME=root
DB_PASSWORD=minha_senha
```

### Criando o arquivo config.py

1. Crie um arquivo chamado `config.py` na mesma pasta
2. Adicione o código:

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
        'driver': os.getenv('DB_CONNECTION', 'mysql'),
        'host': os.getenv('DB_HOST', '127.0.0.1'),
        'port': int(os.getenv('DB_PORT', 3306)),
        'database': os.getenv('DB_DATABASE', 'quentorm'),
        'username': os.getenv('DB_USERNAME', 'root'),
        'password': os.getenv('DB_PASSWORD', ''),
    }
})
```

### Testando a conexão

Crie um arquivo `teste_conexao.py`:

```python
from config import db

try:
    # Tenta executar uma consulta simples
    db.execute('SELECT 1')
    print("Conexão com o banco de dados estabelecida com sucesso!")
except Exception as e:
    print(f"Erro ao conectar: {e}")
```

Execute:

```bash
python teste_conexao.py
```

## Arquivos de Configuração

### config.py vs config/database.py

O QuentORM utiliza dois arquivos de configuração principais:

1. **config.py** (Configurações Globais)
   ```python
   from quentorm import Database
   from datetime import timedelta
   import os
   from dotenv import load_dotenv

   load_dotenv()

   db = Database()

   # Configurações de Banco de Dados
   db.config({
       'default': {
           'driver': os.getenv('DB_CONNECTION', 'mysql'),
           'host': os.getenv('DB_HOST', '127.0.0.1'),
           'port': int(os.getenv('DB_PORT', 3306)),
           'database': os.getenv('DB_DATABASE', 'quentorm'),
           'username': os.getenv('DB_USERNAME', 'root'),
           'password': os.getenv('DB_PASSWORD', ''),
           'charset': os.getenv('DB_CHARSET', 'utf8mb4'),
           'collation': os.getenv('DB_COLLATION', 'utf8mb4_unicode_ci'),
           'prefix': os.getenv('DB_PREFIX', ''),
           'strict': os.getenv('DB_STRICT', 'true').lower() == 'true',
           'engine': os.getenv('DB_ENGINE', 'InnoDB'),
           'options': {
               'pool_size': 5,
               'max_overflow': 10,
               'pool_timeout': 30,
               'pool_recycle': 3600,
               'pool_pre_ping': True
           }
       }
   })

   # Configurações de Cache
   cache_config = {
       'default': {
           'driver': os.getenv('CACHE_DRIVER', 'file'),
           'host': os.getenv('CACHE_HOST', '127.0.0.1'),
           'port': int(os.getenv('CACHE_PORT', 6379)),
           'prefix': os.getenv('CACHE_PREFIX', 'quentorm_'),
           'ttl': timedelta(days=1)
       }
   }

   # Configurações de Logging
   logging_config = {
       'enabled': os.getenv('LOG_QUERIES', 'false').lower() == 'true',
       'slow_query_threshold': 1.0,  # segundos
       'log_file': 'logs/queries.log',
       'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
   }
   ```

2. **config/database.py** (Configurações Específicas do Banco)
   ```python
   from quentorm import Database
   from datetime import timedelta

   db = Database()

   # Configurações de Conexão
   connection_config = {
       'default': {
           'driver': 'mysql',
           'host': '127.0.0.1',
           'port': 3306,
           'database': 'quentorm',
           'username': 'root',
           'password': '',
           'charset': 'utf8mb4',
           'collation': 'utf8mb4_unicode_ci',
           'prefix': '',
           'strict': True,
           'engine': 'InnoDB'
       }
   }

   # Configurações de Pool
   pool_config = {
       'pool_size': 5,
       'max_overflow': 10,
       'pool_timeout': 30,
       'pool_recycle': 3600,
       'pool_pre_ping': True
   }

   # Configurações de Schema
   schema_config = {
       'default_schema': 'public',
       'search_path': ['public', 'auth'],
       'create_schema': True
   }

   # Aplicar configurações
   db.config(connection_config)
   db.set_pool_options(pool_config)
   db.set_schema_options(schema_config)
   ```

### Quando Usar Cada Um

1. **Use config.py quando**:
   - Configurar o projeto pela primeira vez
   - Definir configurações globais
   - Gerenciar múltiplas configurações (banco, cache, logging)
   - Usar variáveis de ambiente

2. **Use config/database.py quando**:
   - Trabalhar apenas com configurações de banco
   - Precisar de configurações específicas do banco
   - Gerenciar múltiplas conexões
   - Configurar schemas e pools

### Boas Práticas

1. **Organização**:
   - Mantenha `config.py` para configurações globais
   - Use `config/database.py` para configurações específicas do banco
   - Documente alterações em ambos os arquivos

2. **Segurança**:
   - Nunca versione `config.py` com senhas
   - Use variáveis de ambiente em `config.py`
   - Mantenha `config/database.py` versionado

3. **Manutenção**:
   - Atualize ambos os arquivos quando necessário
   - Mantenha consistência entre os arquivos
   - Documente alterações importantes

4. **Desenvolvimento**:
   - Use `config.py` em desenvolvimento
   - Use `config/database.py` em produção
   - Mantenha ambientes separados

## Criando seu Primeiro Modelo

### O que é um Modelo?

Um modelo é como uma "representação" de uma tabela do banco de dados. Por exemplo, se você tem uma tabela `users`, você cria um modelo `User`.

### Criando o Modelo User

1. Crie uma pasta `models` no seu projeto
2. Crie um arquivo `user.py` dentro dela:

```python
from quentorm import Model
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

class User(Model):
    # Nome da tabela no banco de dados
    __table__ = 'users'
    
    # Colunas da tabela
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    email = Column(String(255))
    created_at = Column(DateTime, default=datetime.now)
    
    def __repr__(self):
        return f"<User {self.name}>"
```

### Explicando o código

1. `from quentorm import Model`: Importa a classe base para modelos
2. `__table__ = 'users'`: Define o nome da tabela no banco
3. `id = Column(Integer, primary_key=True)`: Cria uma coluna de ID
4. `name = Column(String(255))`: Cria uma coluna para o nome
5. `created_at`: Registra quando o usuário foi criado

### Criando a tabela no banco

Crie um arquivo `criar_tabela.py`:

```python
from config import db
from models.user import User

# Cria a tabela se não existir
User.create_table()

print("Tabela 'users' criada com sucesso!")
```

Execute:

```bash
python criar_tabela.py
```

## Operações Básicas com o Modelo

### Inserindo Dados

```python
from models.user import User

# Criar um usuário
user = User.create(
    name="João Silva",
    email="joao@exemplo.com"
)

print(f"Usuário criado: {user.name}")
```

### Buscando Dados

```python
from models.user import User

# Buscar todos os usuários
users = User.all()
for user in users:
    print(user.name)

# Buscar um usuário específico
joao = User.where('name', 'João Silva').first()
print(f"Email do João: {joao.email}")

# Buscar usuários com condições
adultos = User.where('age', '>', 18).get()
for adulto in adultos:
    print(adulto.name)
```

### Atualizando Dados

```python
from models.user import User

# Atualizar um usuário
joao = User.where('name', 'João Silva').first()
joao.email = "novo_email@exemplo.com"
joao.save()

# Atualizar em massa
User.where('age', '<', 18).update(status='menor')
```

### Excluindo Dados

```python
from models.user import User

# Excluir um usuário
joao = User.where('name', 'João Silva').first()
joao.delete()

# Excluir em massa
User.where('status', 'inativo').delete()
```

## Próximos Passos

Agora que você já sabe o básico, pode explorar:

1. [Relacionamentos entre Modelos](#relacionamentos)
2. [Validações de Dados](#validações)
3. [Eventos e Observadores](#eventos)
4. [Consultas Avançadas](#consultas-avançadas)

## Relacionamentos entre Modelos

### O que são Relacionamentos?

Imagine que você tem uma rede social. Os usuários podem ter posts, e cada post pertence a um usuário. Isso é um relacionamento! No QuentORM, você pode definir esses relacionamentos de forma simples.

### Tipos de Relacionamentos

1. **Um para Um**: Um usuário tem um perfil
2. **Um para Muitos**: Um usuário tem vários posts
3. **Muitos para Muitos**: Usuários seguem outros usuários

### Criando Modelos Relacionados

Primeiro, vamos criar o modelo `Post`:

```python
from quentorm import Model
from sqlalchemy import Column, Integer, String, ForeignKey
from datetime import datetime

class Post(Model):
    __table__ = 'posts'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    content = Column(String(1000))
    user_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.now)
    
    def __repr__(self):
        return f"<Post {self.title}>"
```

### Definindo Relacionamentos

Agora, vamos atualizar o modelo `User` para incluir os relacionamentos:

```python
class User(Model):
    __table__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    email = Column(String(255))
    created_at = Column(DateTime, default=datetime.now)
    
    # Relacionamento um para muitos
    posts = relationship('Post', backref='user')
    
    def __repr__(self):
        return f"<User {self.name}>"
```

### Usando Relacionamentos

```python
# Criar um usuário com posts
user = User.create(
    name="Maria Silva",
    email="maria@exemplo.com"
)

# Criar posts para o usuário
post1 = Post.create(
    title="Meu primeiro post",
    content="Olá, mundo!",
    user_id=user.id
)

post2 = Post.create(
    title="Segundo post",
    content="Aprendendo Python!",
    user_id=user.id
)

# Buscar posts de um usuário
posts = user.posts
for post in posts:
    print(f"Post: {post.title}")

# Buscar usuário de um post
post = Post.first()
print(f"Post escrito por: {post.user.name}")
```

## Validações

O QuentORM oferece um sistema robusto de validação de dados, com suporte a múltiplos tipos de validação e internacionalização de mensagens.

### Tipos de Validação

- **Documentos**: CPF, CNPJ e validação automática
- **Dados Bancários**: Agência, conta e dígito verificador
- **Dados Pessoais**: Email, telefone e CEP

### Exemplo Rápido

```python
from quentorm import Model, Field

class Cliente(Model):
    nome = Field(str)
    cpf = Field(str, validators=['cpf'])
    email = Field(str, validators=['email'])

# Criando um cliente
cliente = Cliente(
    nome="João Silva",
    cpf="12345678901",
    email="joao@exemplo.com"
)

# Salvando o cliente (as validações são executadas automaticamente)
try:
    cliente.save()
except ValidationError as e:
    print(e.message)
```

### Boas Práticas

1. Valide os dados assim que eles entram no sistema
2. Use mensagens de erro descritivas
3. Capture e trate exceções de validação
4. Implemente validação em camadas
5. Teste casos válidos e inválidos

Para mais detalhes sobre validações, consulte a [documentação completa](docs/VALIDACOES.md).

## Eventos e Observadores

### O que são Eventos?

Eventos são ações que acontecem em momentos específicos, como:
- Antes de salvar um usuário
- Depois de criar um post
- Antes de excluir um comentário

### Criando um Observador

```python
from quentorm import Observer

class UserObserver(Observer):
    def saving(self, user):
        print(f"Salvando usuário: {user.name}")
    
    def saved(self, user):
        print(f"Usuário salvo: {user.name}")
    
    def deleting(self, user):
        print(f"Excluindo usuário: {user.name}")
    
    def deleted(self, user):
        print(f"Usuário excluído: {user.name}")
```

### Registrando o Observador

```python
# Registrar observador para todos os usuários
User.observe(UserObserver())

# Criar usuário (disparará eventos)
user = User.create(
    name="João",
    email="joao@exemplo.com"
)

# Excluir usuário (disparará eventos)
user.delete()
```

## Consultas Avançadas

### O que são Consultas Avançadas?

São consultas que vão além do básico, como:
- Agrupar resultados
- Ordenar de forma específica
- Limitar o número de resultados
- Fazer consultas complexas

### Exemplos de Consultas Avançadas

```python
# Ordenar usuários por nome
users = User.order_by('name').get()

# Ordenar por nome decrescente
users = User.order_by('name', 'desc').get()

# Limitar número de resultados
users = User.limit(5).get()

# Pular resultados (paginação)
users = User.offset(10).limit(5).get()

# Agrupar posts por usuário
posts = Post.group_by('user_id').get()

# Contar posts por usuário (forma simplificada)
counts = Post.countBy('user_id')
# Retorna: [{'user_id': 1, 'total': 5}, {'user_id': 2, 'total': 3}]

# Buscar usuários em uma faixa etária
users = User.between('age', 18, 30).get()

# Buscar posts de um período
posts = Post.between('created_at', '2023-01-01', '2023-12-31').get()

# Buscar usuários ativos
active_users = User.isTrue('is_active').get()

# Buscar usuários inativos
inactive_users = User.isFalse('is_active').get()

# Consulta com subconsulta
users = User.where_in('id', 
    Post.select('user_id').where('created_at', '>', '2023-01-01')
).get()
```

### Query Builder - Métodos Disponíveis

O Query Builder do QuentORM oferece uma variedade de métodos para construir consultas SQL de forma intuitiva. Vamos explorar cada um deles:

### Métodos de Seleção

1. **select()**
   ```python
   # Selecionar colunas específicas
   users = User.select('id', 'name', 'email').get()
   
   # Selecionar com alias
   users = User.select('name as nome', 'email as email').get()
   ```

2. **distinct()**
   ```python
   # Selecionar valores únicos
   emails = User.select('email').distinct().get()
   ```

3. **from_()**
   ```python
   # Especificar tabela
   users = User.from_('users').get()
   ```

### Métodos de Filtro

1. **where()**
   ```python
   # Condição simples
   users = User.where('age', '>', 18).get()
   
   # Múltiplas condições
   users = User.where('age', '>', 18).where('status', 'active').get()
   ```

2. **orWhere()**
   ```python
   # Condição OR
   users = User.where('age', '>', 18).orWhere('status', 'active').get()
   ```

3. **whereIn()**
   ```python
   # Verificar se valor está em lista
   users = User.whereIn('id', [1, 2, 3]).get()
   ```

4. **whereNotIn()**
   ```python
   # Verificar se valor não está em lista
   users = User.whereNotIn('id', [1, 2, 3]).get()
   ```

5. **whereNull()**
   ```python
   # Verificar se campo é NULL
   users = User.whereNull('deleted_at').get()
   ```

6. **whereNotNull()**
   ```python
   # Verificar se campo não é NULL
   users = User.whereNotNull('email').get()
   ```

7. **whereBetween()**
   ```python
   # Verificar se valor está entre dois valores
   users = User.whereBetween('age', [18, 30]).get()
   ```

8. **whereNotBetween()**
   ```python
   # Verificar se valor não está entre dois valores
   users = User.whereNotBetween('age', [18, 30]).get()
   ```

9. **between()**
   ```python
   # Forma mais intuitiva de verificar intervalo
   users = User.between('age', 18, 30).get()
   
   # Com alias para maior clareza
   users = User.between('age', min=18, max=30).get()
   
   # Com datas
   posts = Post.between('created_at', '2023-01-01', '2023-12-31').get()
   
   # Com valores decimais
   products = Product.between('price', 10.50, 99.99).get()
   ```

10. **isTrue()**
    ```python
    # Verificar se valor é TRUE
    users = User.isTrue('is_active').get()
    
    # Com alias
    users = User.isTrue('is_active', alias='ativo').get()
    
    # Com condições adicionais
    users = User.isTrue('is_admin').where('age', '>', 18).get()
    ```

11. **isFalse()**
    ```python
    # Verificar se valor é FALSE
    users = User.isFalse('is_active').get()
    
    # Com alias
    users = User.isFalse('is_active', alias='inativo').get()
    
    # Com condições adicionais
    users = User.isFalse('is_admin').where('age', '>', 18).get()
    ```

12. **whereEmptyOrNull()**
    ```python
    # Verificar se campo está vazio ou é NULL
    users = User.whereEmptyOrNull('bio').get()
    
    # Com múltiplos campos
    users = User.whereEmptyOrNull(['bio', 'website']).get()
    
    # Com condições adicionais
    users = User.whereEmptyOrNull('bio').where('age', '>', 18).get()
    
    # Verificar campos de diferentes tipos
    # String vazia
    users = User.whereEmptyOrNull('name').get()
    
    # Lista vazia
    users = User.whereEmptyOrNull('tags').get()
    
    # JSON vazio
    users = User.whereEmptyOrNull('preferences').get()
    
    # Com alias para maior clareza
    users = User.whereEmptyOrNull('bio', alias='sem_biografia').get()
    
    # Com operador OR
    users = User.whereEmptyOrNull('bio').orWhereEmptyOrNull('website').get()
    
    # Com subconsulta
    users = User.whereEmptyOrNull('bio').whereIn('id', 
        Post.select('user_id').where('created_at', '>', '2023-01-01')
    ).get()
    ```

### Métodos de Ordenação

1. **orderBy()**
   ```python
   # Ordenar por uma coluna
   users = User.orderBy('name').get()
   
   # Ordenar descendente
   users = User.orderBy('name', 'desc').get()
   ```

2. **latest()**
   ```python
   # Ordenar por data mais recente
   posts = Post.latest('created_at').get()
   ```

3. **oldest()**
   ```python
   # Ordenar por data mais antiga
   posts = Post.oldest('created_at').get()
   ```

### Métodos de Agrupamento

1. **groupBy()**
   ```python
   # Agrupar por coluna
   posts = Post.groupBy('user_id').get()
   ```

2. **having()**
   ```python
   # Filtrar grupos
   users = User.groupBy('status').having('count', '>', 5).get()
   ```

### Métodos de Limitação

1. **limit()**
   ```python
   # Limitar número de resultados
   users = User.limit(10).get()
   ```

2. **offset()**
   ```python
   # Pular resultados (paginação)
   users = User.offset(10).limit(5).get()
   ```

3. **take()**
   ```python
   # Limitar número de resultados (alternativa)
   users = User.take(5).get()
   ```

4. **skip()**
   ```python
   # Pular resultados (alternativa)
   users = User.skip(10).take(5).get()
   ```

### Métodos de Agregação

1. **count()**
   ```python
   # Contar registros
   total = User.count()
   
   # Contar com condições
   total = User.where('age', '>', 18).count()
   ```

2. **countBy()**
   ```python
   # Contar agrupando por coluna
   counts = Post.countBy('user_id')
   # Retorna: [{'user_id': 1, 'total': 5}, {'user_id': 2, 'total': 3}]
   
   # Contar com alias personalizado
   counts = Post.countBy('user_id', alias='quantidade')
   # Retorna: [{'user_id': 1, 'quantidade': 5}, {'user_id': 2, 'quantidade': 3}]
   
   # Contar com condições
   counts = Post.where('status', 'published').countBy('user_id')
   ```

3. **sum()**
   ```python
   # Somar valores
   total = Order.sum('amount')
   ```

4. **avg()**
   ```python
   # Calcular média
   media = Order.avg('amount')
   ```

5. **min()**
   ```python
   # Encontrar valor mínimo
   menor = User.min('age')
   ```

6. **max()**
   ```python
   # Encontrar valor máximo
   maior = User.max('age')
   ```

### Métodos de Relacionamento

1. **with_()**
   ```python
   # Carregar relacionamentos
   users = User.with_('posts').get()
   ```

2. **join()**
   ```python
   # Inner join
   users = User.join('posts', 'users.id', '=', 'posts.user_id').get()
   ```

3. **leftJoin()**
   ```python
   # Left join
   users = User.leftJoin('posts', 'users.id', '=', 'posts.user_id').get()
   ```

4. **rightJoin()**
   ```python
   # Right join
   users = User.rightJoin('posts', 'users.id', '=', 'posts.user_id').get()
   ```

### Métodos de União

1. **union()**
   ```python
   # Unir consultas
   query1 = User.where('age', '>', 18)
   query2 = User.where('status', 'active')
   users = query1.union(query2).get()
   ```

2. **unionAll()**
   ```python
   # Unir consultas (incluindo duplicatas)
   users = query1.unionAll(query2).get()
   ```

### Métodos de Subconsulta

1. **whereIn() com subconsulta**
   ```python
   # Usar subconsulta
   users = User.whereIn('id', 
       Post.select('user_id').where('created_at', '>', '2023-01-01')
   ).get()
   ```

2. **exists()**
   ```python
   # Verificar existência
   users = User.whereExists(
       Post.where('user_id', '=', 'users.id')
   ).get()
   ```

### Métodos de Cache

1. **cache()**
   ```python
   # Cache por tempo
   users = User.cache(60).get()  # 60 segundos
   ```

2. **cacheTags()**
   ```python
   # Cache com tags
   users = User.cacheTags(['users', 'active']).get()
   ```

### Métodos de Debug

1. **toSql()**
   ```python
   # Ver SQL gerado
   sql = User.where('age', '>', 18).toSql()
   print(sql)
   ```

2. **explain()**
   ```python
   # Explicar consulta
   explanation = User.where('age', '>', 18).explain()
   print(explanation)
   ```

### Dicas de Uso

1. **Encadeamento de Métodos**
   ```python
   users = User.where('age', '>', 18)\
              .where('status', 'active')\
              .orderBy('name')\
              .limit(10)\
              .get()
   ```

2. **Reutilização de Consultas**
   ```python
   base_query = User.where('status', 'active')
   
   # Usar em diferentes contextos
   active_users = base_query.get()
   active_adults = base_query.where('age', '>', 18).get()
   ```

3. **Performance**
   ```python
   # Evitar N+1 queries
   users = User.with_('posts').get()  # Bom
   for user in users:
       print(user.posts)  # Já carregado
   
   # vs
   users = User.get()  # Ruim
   for user in users:
       print(user.posts)  # Nova query para cada usuário
   ```

## Próximos Passos

Agora que você já conhece os conceitos básicos e avançados do QuentORM, pode:

1. **Explorar mais recursos**:
   - Transações
   - Escopos
   - Mutadores
   - Acessores

2. **Praticar com projetos reais**:
   - Criar uma API
   - Desenvolver um blog
   - Construir um sistema de usuários

3. **Aprofundar conhecimentos**:
   - Ler a documentação do SQLAlchemy
   - Estudar padrões de banco de dados
   - Aprender sobre otimização

Lembre-se: A prática é essencial para dominar o QuentORM. Tente criar seus próprios projetos e experimentar diferentes recursos!

### Métodos de Atualização

1. **updateOrCreate()**
    ```python
    # Atualizar ou criar um único registro
    user = User.updateOrCreate(
        {'email': 'joao@exemplo.com'},  # Condição de busca
        {'name': 'João Silva', 'age': 25}  # Dados para atualizar/criar
    )
    
    # Atualizar ou criar em lote
    users = User.updateOrCreate(
        [
            {
                'condition': {'email': 'joao@exemplo.com'},
                'data': {'name': 'João Silva', 'age': 25}
            },
            {
                'condition': {'email': 'maria@exemplo.com'},
                'data': {'name': 'Maria Silva', 'age': 30}
            }
        ]
    )
    
    # Com validações
    try:
        user = User.updateOrCreate(
            {'email': 'joao@exemplo.com'},
            {'name': 'João Silva', 'age': -5}  # Falhará se age < 0
        )
    except ValueError as e:
        print(f"Erro: {e}")
    
    # Com relacionamentos
    user = User.updateOrCreate(
        {'email': 'joao@exemplo.com'},
        {
            'name': 'João Silva',
            'posts': [
                {'title': 'Primeiro post', 'content': 'Olá mundo!'},
                {'title': 'Segundo post', 'content': 'Aprendendo Python!'}
            ]
        }
    )
    
    # Com timestamps
    user = User.updateOrCreate(
        {'email': 'joao@exemplo.com'},
        {
            'name': 'João Silva',
            'updated_at': datetime.now()
        }
    )
    
    # Com campos calculados
    user = User.updateOrCreate(
        {'email': 'joao@exemplo.com'},
        {
            'name': 'João Silva',
            'full_name': lambda: f"{user.name} {user.last_name}"
        }
    )
    
    # Com transações
    with db.transaction():
        user = User.updateOrCreate(
            {'email': 'joao@exemplo.com'},
            {'name': 'João Silva'}
        )
        user.posts.create({'title': 'Novo post'})
    
    # Com eventos
    class UserObserver(Observer):
        def updating(self, user):
            print(f"Atualizando usuário: {user.name}")
        
        def creating(self, user):
            print(f"Criando usuário: {user.name}")
    
    User.observe(UserObserver())
    user = User.updateOrCreate(
        {'email': 'joao@exemplo.com'},
        {'name': 'João Silva'}
    )
    ```

# Gerando Validadores via CLI

O QuentORM oferece um comando CLI para gerar templates de validadores customizados. Este comando facilita a criação de novos validadores seguindo as melhores práticas do framework.

## Criar um Novo Validador

Para criar um novo validador, use o comando:

```bash
quentorm validator criar NomeDoValidador
```

Por exemplo, para criar um validador de endereço:

```bash
quentorm validator criar Endereco
```

Isto irá criar:
1. Um arquivo `endereco_validator.py` com a estrutura básica do validador
2. Um arquivo de mensagens em português (pt_br.json) com mensagens padrão

### Opções Disponíveis

- `--diretorio, -d`: Define o diretório onde o validador será criado (padrão: validators)
- `--mensagens/--sem-mensagens`: Define se deve gerar arquivo de mensagens (padrão: --mensagens)
- `--idioma, -l`: Define o idioma das mensagens (padrão: pt_br)

Exemplo com opções:

```bash
quentorm validator criar Endereco --diretorio app/validators --idioma en
```

## Remover um Validador

Para remover um validador existente:

```bash
quentorm validator remover NomeDoValidador
```

Isto irá remover o arquivo do validador e seus arquivos de mensagens.

## Listar Mensagens

Para listar as mensagens disponíveis para um validador:

```bash
quentorm validator listar-mensagens NomeDoValidador
```

## Estrutura Gerada

O comando gera a seguinte estrutura:

```
validators/
  ├── endereco_validator.py
  └── messages/
      ├── pt_br.json
      ├── en.json
      ├── es.json
      └── fr.json
```

### Exemplo de Validador Gerado

```python
from typing import Dict, List
from quentorm.utils.validators import Validator, ValidationResult

class EnderecoValidator(Validator):
    """Validador para Endereco."""
    
    def validate(self, valor: str) -> ValidationResult:
        """
        Valida um Endereco.
        
        Args:
            valor: Valor a ser validado
            
        Returns:
            ValidationResult com o resultado da validação
        """
        errors: List[str] = []
        
        # Implemente suas regras de validação aqui
        if not valor:
            errors.append(self.get_message('endereco.required'))
            
        if errors:
            return ValidationResult(
                success=False,
                message=self.get_message('endereco.invalid'),
                errors=errors
            )
            
        return ValidationResult(
            success=True,
            message=self.get_message('endereco.valid')
        )
```

### Exemplo de Mensagens Geradas

```json
{
    "endereco": {
        "valid": "Endereço válido",
        "invalid": "Endereço inválido",
        "required": "Endereço é obrigatório"
    }
}
```

## Próximos Passos

Após gerar um validador:

1. Implemente as regras de validação específicas no método `validate`
2. Adicione mensagens personalizadas nos arquivos de mensagens
3. Importe e use o validador em seu código:

```python
from validators import EnderecoValidator

validador = EnderecoValidator()
resultado = validador.validate("Rua Exemplo, 123")

if resultado.success:
    print(resultado.message)  # "Endereço válido"
else:
    print(resultado.errors)  # Lista de erros encontrados
```

## Soft Deletes

O QuentORM oferece suporte a soft deletes, permitindo que você marque registros como excluídos sem realmente excluí-los do banco de dados.

### Como Usar

Para usar soft deletes, basta chamar o método `delete()` no modelo, que o QuentORM irá marcar o registro como excluído logicamente.

```python
from models.user import User

# Excluir um usuário
joao = User.where('name', 'João Silva').first()
joao.delete()

# Excluir em massa
User.where('status', 'inativo').delete()
```

### Boas Práticas

1. Use soft deletes com moderação
2. Mantenha um campo para registrar o motivo da exclusão
3. Implemente regras de recuperação de dados excluídos
4. Teste casos de exclusão e recuperação

Para mais detalhes sobre soft deletes, consulte a [documentação completa](docs/SOFT_DELETES.md).