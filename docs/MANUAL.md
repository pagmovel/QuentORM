# 📚 QuentORM: O Guia Completo

## 📋 Índice

1. [Introdução](#1️⃣-introdução)
2. [Instalação](#2️⃣-instalação)
3. [Configuração do Ambiente](#3️⃣-configuração-do-ambiente)
4. [Modelos e Migrações](#4️⃣-modelos-e-migrações)
5. [Relacionamentos](#5️⃣-relacionamentos)
6. [Consultas e Filtros](#6️⃣-consultas-e-filtros)
7. [Validações](#7️⃣-validações)
8. [Eventos](#8️⃣-eventos)
9. [CLI e Comandos](#9️⃣-cli-e-comandos)
10. [Boas Práticas](#1️⃣0️⃣-boas-práticas)
11. [Exemplos Práticos](#1️⃣1️⃣-exemplos-práticos)
12. [Solução de Problemas](#1️⃣2️⃣-solução-de-problemas)
13. [Cache](#1️⃣3️⃣-cache)
14. [Logging](#1️⃣4️⃣-logging) 

## 1️⃣ Introdução

### O que é o QuentORM?

QuentORM é um ORM (Object-Relational Mapping) moderno e poderoso para Python, projetado para tornar o desenvolvimento de aplicações com banco de dados mais simples, rápido e agradável.

### Principais Características

- 🚀 **Interface Intuitiva**: API fluente e fácil de usar
- 🔄 **Multi-conexões**: Suporte a múltiplos bancos de dados
- 🛡️ **Validações**: Sistema robusto de validação de dados
- 🔌 **Eventos**: Sistema de eventos para hooks e callbacks
- 🛠️ **CLI**: Interface de linha de comando completa
- 📦 **Modular**: Estrutura organizada e extensível

## 2️⃣ Instalação

### Requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Virtualenv (recomendado)

### Comandos de Instalação

```bash
# Instalação via pip (recomendado)
pip install quentorm

# Instalação em modo desenvolvimento
pip install -e .

# Instalação da versão mais recente
pip install git+https://github.com/pagmovel/QuentORM.git
```

## 3️⃣ Configuração do Ambiente

### Arquivo .env

```ini
# Configurações da Aplicação
APP_ENV=development
APP_DEBUG=true
APP_NAME=MeuProjeto

# Conexão Principal (PostgreSQL)
DB_CONNECTION=pgsql
DB_HOST=localhost
DB_PORT=5432
DB_DATABASE=meu_banco
DB_USERNAME=postgres
DB_PASSWORD=senha123
```

### Configuração do Projeto

```python
from quentorm import Config

config = Config()

config.database = {
    'default': {
        'driver': 'pgsql',
    'host': 'localhost',
        'port': 5432,
    'database': 'meu_banco',
        'username': 'postgres',
        'password': 'senha123'
    }
}
```

## 4️⃣ Modelos e Migrações

### Definindo um Modelo

```python
from quentorm import BaseModel, Column, types

class User(BaseModel):
    __tablename__ = 'users'
    
    id = Column(types.Integer, primary_key=True)
    name = Column(types.String(100), nullable=False)
    email = Column(types.String(100), unique=True)
    active = Column(types.Boolean, default=True)
    created_at = Column(types.DateTime, server_default=types.func.now())
```

### Criando uma Migração

```python
from quentorm import Migration

class CreateUsersTable(Migration):
    def up(self):
        self.create_table('users', [
            Column('id', Integer, primary_key=True),
            Column('name', String(100), nullable=False),
            Column('email', String(100), unique=True),
            Column('active', Boolean, default=True),
            Column('created_at', DateTime, default=datetime.utcnow)
        ])

    def down(self):
        self.drop_table('users')
```

## 5️⃣ Relacionamentos

### Um para Um

```python
from quentorm import BaseModel, Column, types, relationship

class User(BaseModel):
    __tablename__ = 'users'
    
    id = Column(types.Integer, primary_key=True)
    name = Column(types.String(100))
    
    # Relacionamento um-para-um
    profile = relationship('Profile', back_populates='user', uselist=False)

class Profile(BaseModel):
    __tablename__ = 'profiles'
    
    id = Column(types.Integer, primary_key=True)
    user_id = Column(types.Integer, ForeignKey('users.id'))
    bio = Column(types.Text)
    
    user = relationship('User', back_populates='profile')
```

### Um para Muitos

```python
class Post(BaseModel):
    __tablename__ = 'posts'
    
    id = Column(types.Integer, primary_key=True)
    title = Column(types.String(200))
    content = Column(types.Text)
    user_id = Column(types.Integer, ForeignKey('users.id'))
    
    user = relationship('User', back_populates='posts')

class User(BaseModel):
    __tablename__ = 'users'
    
    id = Column(types.Integer, primary_key=True)
    name = Column(types.String(100))
    
    posts = relationship('Post', back_populates='user')
```

### Muitos para Muitos

```python
post_tags = Table('post_tags', BaseModel.metadata,
    Column('post_id', types.Integer, ForeignKey('posts.id')),
    Column('tag_id', types.Integer, ForeignKey('tags.id'))
)

class Post(BaseModel):
    __tablename__ = 'posts'
    
    id = Column(types.Integer, primary_key=True)
    title = Column(types.String(200))
    
    tags = relationship('Tag', secondary=post_tags, back_populates='posts')

class Tag(BaseModel):
    __tablename__ = 'tags'
    
    id = Column(types.Integer, primary_key=True)
    name = Column(types.String(50))
    
    posts = relationship('Post', secondary=post_tags, back_populates='tags')
```

## 6️⃣ Consultas e Filtros

### Consultas Básicas

```python
# Buscar todos os registros
users = User.all()

# Buscar por ID
user = User.find(1)

# Buscar primeiro registro
user = User.first()

# Buscar último registro
user = User.last()

# Contar registros
count = User.count()
```

### Filtros

```python
# Filtro simples
users = User.where('active', True).get()

# Filtro com operador
users = User.where('age', '>', 18).get()

# Múltiplos filtros (AND)
users = User.where('active', True).where('age', '>', 18).get()

# Filtro OR
users = User.where('name', 'John').or_where('name', 'Jane').get()

# Filtro IN
users = User.where_in('id', [1, 2, 3]).get()

# Filtro LIKE
users = User.where_like('name', '%John%').get()
```

### Ordenação e Paginação

```python
# Ordenação simples
users = User.order_by('name').get()

# Ordenação múltipla
users = User.order_by('age', 'desc').order_by('name').get()

# Limite e offset
users = User.limit(10).offset(20).get()

# Paginação
users, total = User.paginate(page=2, per_page=10)
```

### Relacionamentos

```python
# Carregar relacionamentos
users = User.with_('posts').get()

# Carregar múltiplos relacionamentos
users = User.with_('posts', 'profile').get()

# Filtrar por relacionamento
users = User.where_has('posts', lambda q: q.where('active', True)).get()

# Contar relacionamentos
users = User.with_count('posts').get()
```

## 7️⃣ Validações

### Validações Básicas

```python
from quentorm import BaseModel, Column, validates

class User(BaseModel):
    __tablename__ = 'users'
    
    id = Column(types.Integer, primary_key=True)
    name = Column(types.String(100))
    email = Column(types.String(255))
    age = Column(types.Integer)
    
    @validates('name')
    def validate_name(self, key, value):
        if len(value) < 3:
            raise ValueError('Nome deve ter pelo menos 3 caracteres')
        return value
    
    @validates('email')
    def validate_email(self, key, value):
        if not '@' in value:
            raise ValueError('Email inválido')
        return value
    
    @validates('age')
    def validate_age(self, key, value):
        if value < 0 or value > 120:
            raise ValueError('Idade inválida')
        return value
```

### Validadores Personalizados

```python
from quentorm.validators import Validator

class CPFValidator(Validator):
    def validate(self, value):
        if not self.is_valid_cpf(value):
            raise ValueError('CPF inválido')
        return value
    
    def is_valid_cpf(self, cpf):
        # Lógica de validação de CPF
        return True

class User(BaseModel):
    __tablename__ = 'users'
    
    cpf = Column(types.String(11))
    
    __validators__ = {
        'cpf': CPFValidator()
    }
```

### Validação em Lote

```python
def import_users(users_data):
    valid_users = []
    errors = []
    
    for data in users_data:
        try:
            user = User(**data)
            if user.is_valid():
                valid_users.append(user)
            else:
                errors.append(user.errors)
        except ValueError as e:
            errors.append(str(e))
    
    return valid_users, errors
```

## 8️⃣ Eventos

### Eventos de Ciclo de Vida

```python
from quentorm import BaseModel, event

class User(BaseModel):
    __tablename__ = 'users'
    
    @event('before_create')
    def before_create(self):
        self.password = hash_password(self.password)
    
    @event('after_create')
    def after_create(self):
        send_welcome_email(self.email)
    
    @event('before_update')
    def before_update(self):
        self.updated_at = datetime.now()
    
    @event('after_delete')
    def after_delete(self):
        cleanup_user_data(self.id)
```

### Eventos Assíncronos

```python
from quentorm import BaseModel, async_event

class Post(BaseModel):
    __tablename__ = 'posts'
    
    @async_event('after_create')
    async def index_content(self):
        await search_service.index(self)
    
    @async_event('after_update')
    async def update_cache(self):
        await cache_service.invalidate(self)
```

### Eventos Personalizados

```python
from quentorm import BaseModel, event

class Order(BaseModel):
    __tablename__ = 'orders'
    
    @event('after_payment')
    def after_payment(self):
        self.status = 'paid'
        self.send_confirmation()
    
    @event('after_shipment')
    def after_shipment(self):
        self.status = 'shipped'
        self.send_tracking()
```

## 9️⃣ CLI e Comandos

O QuentORM fornece uma interface de linha de comando (CLI) completa para gerenciar seu projeto. Esta seção detalha todos os comandos disponíveis e suas opções.

### Comandos Disponíveis

#### 1. Migrações

```bash
# Criar uma nova migração
quentorm make:migration <nome_da_migracao>

# Executar migrações pendentes
quentorm migrate

# Reverter a última migração
quentorm migrate:rollback

# Reverter todas as migrações
quentorm migrate:reset

# Recriar o banco de dados (reset + migrate)
quentorm migrate:refresh

# Listar todas as migrações
quentorm migrate:status
```

Opções para migrações:
- `--path`: Especificar o diretório das migrações
- `--pretend`: Mostrar o SQL sem executar
- `--step`: Número de migrações para reverter
- `--force`: Forçar execução em produção

#### 2. Modelos

```bash
# Criar um novo modelo
quentorm make:model <nome_do_modelo>

# Criar um modelo com migração
quentorm make:model <nome_do_modelo> --migration

# Criar um modelo com validações
quentorm make:model <nome_do_modelo> --validators

# Criar um modelo com relacionamentos
quentorm make:model <nome_do_modelo> --relationships
```

Opções para modelos:
- `--table`: Nome da tabela (se diferente do modelo)
- `--fillable`: Campos preenchíveis
- `--hidden`: Campos ocultos
- `--timestamps`: Adicionar timestamps
- `--soft-deletes`: Adicionar soft deletes

#### 3. Validações

```bash
# Criar um novo validador
quentorm make:validator <nome_do_validador>

# Criar regras de validação
quentorm make:rule <nome_da_regra>
```

Opções para validações:
- `--force`: Sobrescrever arquivo existente
- `--path`: Diretório de destino

#### 4. Eventos

```bash
# Criar um novo evento
quentorm make:event <nome_do_evento>

# Criar um listener
quentorm make:listener <nome_do_listener>
```

Opções para eventos:
- `--event`: Nome do evento associado
- `--queued`: Criar como evento em fila

#### 5. Projeto

```bash
# Criar um novo projeto
quentorm new <nome_do_projeto>

# Instalar dependências
quentorm install

# Atualizar dependências
quentorm update

# Limpar cache
quentorm cache:clear
```

Opções para projeto:
- `--dev`: Instalar dependências de desenvolvimento
- `--no-interaction`: Não perguntar confirmações
- `--prefer-source`: Preferir instalação do código-fonte

### Exemplos de Uso

#### Criando um Projeto

```bash
# Criar um novo projeto
quentorm new meu-projeto

# Navegar para o diretório
cd meu-projeto

# Instalar dependências
quentorm install
```

#### Gerenciando Migrações

```bash
# Criar uma migração para a tabela de usuários
quentorm make:migration create_users_table

# Executar migrações
quentorm migrate

# Verificar status
quentorm migrate:status
```

#### Criando Modelos

```bash
# Criar um modelo de usuário com migração
quentorm make:model User --migration --fillable="name,email,password"

# Criar um modelo de post com relacionamentos
quentorm make:model Post --relationships="belongsTo:User,hasMany:Comment"
```

#### Gerenciando Validações

```bash
# Criar um validador de email
quentorm make:validator EmailValidator

# Criar uma regra de validação
quentorm make:rule RequiredRule
```

### Dicas e Boas Práticas

1. **Nomenclatura**: Use nomes descritivos para migrações e modelos
2. **Ordem**: Execute migrações em ordem cronológica
3. **Backup**: Faça backup antes de executar migrações em produção
4. **Ambiente**: Use diferentes configurações para desenvolvimento e produção
5. **Versionamento**: Mantenha o controle de versão das migrações

### Solução de Problemas

Se encontrar problemas com os comandos CLI:

1. Verifique se o QuentORM está instalado corretamente
2. Confirme se está no diretório correto do projeto
3. Verifique as permissões de arquivo
4. Consulte os logs de erro
5. Tente executar com a opção `--verbose` para mais detalhes

## 1️⃣0️⃣ Boas Práticas

### Organização do Projeto

1. **Estrutura de Diretórios**: Mantenha a estrutura de diretórios organizada, com subdiretórios para modelos, controladores, visualizações, configurações, etc.
2. **Nomenclatura**: Use nomes descritivos para arquivos e classes, facilitando a navegação e compreensão do código.
3. **Documentação**: Adicione comentários de documentação para classes e métodos, explicando o propósito e o comportamento.

### Código Limpo

1. **Modularidade**: Divida o código em módulos pequenos e focados, evitando código duplicado e aumentando a reutilização.
2. **Consistência**: Siga um padrão de codificação consistente, facilitando a manutenção e a colaboração.
3. **Legibilidade**: Use nomes descritivos para variáveis, métodos e classes, tornando o código mais legível e fácil de entender.

### Segurança

1. **Autenticação e Autorização**: Implemente medidas de segurança para proteger o sistema contra ataques comuns, como injeção de SQL, Cross-Site Scripting (XSS) e Cross-Site Request Forgery (CSRF).
2. **Validações**: Use validações robustas para garantir a integridade dos dados antes de salvar no banco de dados.
3. **Segredos**: Armazene segredos, como senhas e chaves de API, em variáveis de ambiente e não inclua-as diretamente no código-fonte.

### Performance

1. **Índices**: Use índices apropriados nas colunas frequentemente consultadas para melhorar o desempenho das consultas.
2. **Eager Loading**: Use eager loading para carregar relacionamentos junto com a consulta principal, evitando N+1 queries.
3. **Paginação**: Implemente paginação adequada para consultas que retornam muitos registros.

### Manutenção

1. **Migrations**: Use migrations para controlar as mudanças no esquema do banco de dados, facilitando a atualização e a reversão de alterações.
2. **Versionamento**: Use versionamento de código para controlar as mudanças no modelo de dados, facilitando a colaboração e a reversão de alterações.
3. **Testes**: Implemente testes unitários e de integração para garantir que o código funciona corretamente em diferentes cenários.

## 1️⃣1️⃣ Exemplos Práticos

### Sistema de Blog

Este exemplo demonstra como criar um sistema de blog completo usando QuentORM. Vamos implementar modelos para usuários, posts, categorias, comentários e tags.

#### 1. Modelos

```python
# app/models/user.py
class User(BaseModel):
    """Modelo de usuário com validações e relacionamentos.
    
    Este modelo representa um usuário do sistema, com campos básicos
    como nome, email e senha. Inclui validações para garantir
    a integridade dos dados.
    """
    
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    posts = relationship('Post', back_populates='author')
    comments = relationship('Comment', back_populates='user')
    
    # Validações
    __validators__ = {
        'email': DefaultEmailValidator(),
        'password': DefaultSenhaValidator()
    }

# app/models/category.py
class Category(BaseModel):
    """Modelo de categoria para organizar posts.
    
    Permite categorizar posts em tópicos específicos,
    facilitando a navegação e busca de conteúdo.
    """
    
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    slug = Column(String(50), unique=True, nullable=False)
    description = Column(Text)
    
    # Relacionamentos
    posts = relationship('Post', back_populates='category')

# app/models/post.py
class Post(BaseModel):
    """Modelo de post com suporte a tags e comentários.
    
    Representa um artigo do blog, com título, conteúdo,
    status de publicação e métricas de visualização.
    """
    
    __tablename__ = 'posts'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    slug = Column(String(200), unique=True, nullable=False)
    content = Column(Text, nullable=False)
    published = Column(Boolean, default=False)
    views = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    
    # Chaves estrangeiras
    author_id = Column(Integer, ForeignKey('users.id'))
    category_id = Column(Integer, ForeignKey('categories.id'))
    
    # Relacionamentos
    author = relationship('User', back_populates='posts')
    category = relationship('Category', back_populates='posts')
    comments = relationship('Comment', back_populates='post')
    tags = relationship('Tag', secondary='post_tags')

# app/models/comment.py
class Comment(BaseModel):
    """Modelo de comentário com suporte a respostas.
    
    Permite que usuários comentem em posts e respondam
    a outros comentários, criando uma estrutura hierárquica.
    """
    
    __tablename__ = 'comments'
    
    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Chaves estrangeiras
    user_id = Column(Integer, ForeignKey('users.id'))
    post_id = Column(Integer, ForeignKey('posts.id'))
    parent_id = Column(Integer, ForeignKey('comments.id'))
    
    # Relacionamentos
    user = relationship('User', back_populates='comments')
    post = relationship('Post', back_populates='comments')
    replies = relationship('Comment', backref=backref('parent', remote_side=[id]))

# app/models/tag.py
class Tag(BaseModel):
    """Modelo de tag para categorização flexível.
    
    Permite marcar posts com palavras-chave,
    facilitando a busca e organização do conteúdo.
    """
    
    __tablename__ = 'tags'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    slug = Column(String(50), unique=True, nullable=False)
    
    # Relacionamentos
    posts = relationship('Post', secondary='post_tags')

# app/models/post_tag.py
class PostTag(BaseModel):
    """Modelo de junção para relacionamento muitos-para-muitos.
    
    Conecta posts e tags, permitindo que um post tenha
    múltiplas tags e uma tag seja usada em múltiplos posts.
    """
    
    orders = relationship('Order', back_populates='customer')
    reviews = relationship('Review', back_populates='user')
    
    def __str__(self):
        return self.name

class Category(Model):
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    slug = Column(String(50), unique=True)
    description = Column(Text, nullable=True)
    parent_id = Column(Integer, ForeignKey('categories.id'), nullable=True)
    
    # Relacionamentos
    products = relationship('Product', back_populates='category')
    parent = relationship('Category', remote_side=[id], backref='children')
    
    def __str__(self):
        return self.name

class Product(Model):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    slug = Column(String(255), unique=True)
    description = Column(Text)
    price = Column(Float)
    stock = Column(Integer)
    sku = Column(String(50), unique=True)
    featured = Column(Boolean, default=False)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Chaves estrangeiras
    category_id = Column(Integer, ForeignKey('categories.id'))
    
    # Relacionamentos
    category = relationship('Category', back_populates='products')
    images = relationship('ProductImage', back_populates='product')
    reviews = relationship('Review', back_populates='product')
    order_items = relationship('OrderItem', back_populates='product')
    
    def __str__(self):
        return self.name
    
    def is_in_stock(self):
        return self.stock > 0
    
    def decrease_stock(self, quantity):
        if self.stock >= quantity:
            self.stock -= quantity
            self.save()
        return True
        return False
    
    def increase_stock(self, quantity):
        self.stock += quantity
        self.save()

class ProductImage(Model):
    __tablename__ = 'product_images'
    
    id = Column(Integer, primary_key=True)
    url = Column(String(255))
    alt = Column(String(255), nullable=True)
    order = Column(Integer, default=0)
    
    # Chave estrangeira
    product_id = Column(Integer, ForeignKey('products.id'))
    
    # Relacionamento
    product = relationship('Product', back_populates='images')
    
    def __str__(self):
        return f"Imagem de {self.product.name}"

class Order(Model):
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True)
    total = Column(Float)
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
    shipping_address = Column(Text)
    billing_address = Column(Text)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Chave estrangeira
    customer_id = Column(Integer, ForeignKey('users.id'))
    
    # Relacionamentos
    customer = relationship('User', back_populates='orders')
    items = relationship('OrderItem', back_populates='order')
    
    def __str__(self):
        return f"Pedido #{self.id}"
    
    def calculate_total(self):
        total = sum(item.subtotal for item in self.items)
        self.total = total
        self.save()
        return total
    
    def update_status(self, status):
        self.status = status
        self.save()
    
    def cancel(self):
        self.status = OrderStatus.CANCELLED
        # Devolver produtos ao estoque
        for item in self.items:
            item.product.increase_stock(item.quantity)
        self.save()

class OrderItem(Model):
    __tablename__ = 'order_items'
    
    id = Column(Integer, primary_key=True)
    quantity = Column(Integer)
    price = Column(Float)
    subtotal = Column(Float)
    
    # Chaves estrangeiras
    order_id = Column(Integer, ForeignKey('orders.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    
    # Relacionamentos
    order = relationship('Order', back_populates='items')
    product = relationship('Product', back_populates='order_items')
    
    def __str__(self):
        return f"{self.quantity}x {self.product.name}"
    
    def calculate_subtotal(self):
        self.subtotal = self.quantity * self.price
        self.save()
        return self.subtotal

class Review(Model):
    __tablename__ = 'reviews'
    
    id = Column(Integer, primary_key=True)
    rating = Column(Integer)  # 1-5
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Chaves estrangeiras
    user_id = Column(Integer, ForeignKey('users.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    
    # Relacionamentos
    user = relationship('User', back_populates='reviews')
    product = relationship('Product', back_populates='reviews')
    
    def __str__(self):
        return f"Avaliação de {self.user.name} para {self.product.name}"
```

#### Exemplos de Uso

```python
# Criar um cliente
customer = User.create({
    'name': 'Maria Silva',
    'email': 'maria@example.com',
    'password': 'senha123',
    'phone': '(11) 99999-9999',
    'address': 'Rua Exemplo, 123'
})

# Criar uma categoria
electronics = Category.create({
    'name': 'Eletrônicos',
    'slug': 'eletronicos',
    'description': 'Produtos eletrônicos'
})

# Criar um produto
product = Product.create({
    'name': 'Smartphone XYZ',
    'slug': 'smartphone-xyz',
    'description': 'Um smartphone incrível',
    'price': 1999.99,
    'stock': 10,
    'sku': 'SM-XYZ-001',
    'category_id': electronics.id
})

# Adicionar imagens ao produto
image1 = ProductImage.create({
    'url': 'https://example.com/smartphone1.jpg',
    'alt': 'Smartphone XYZ - Frente',
    'product_id': product.id
})

image2 = ProductImage.create({
    'url': 'https://example.com/smartphone2.jpg',
    'alt': 'Smartphone XYZ - Verso',
    'product_id': product.id
})

# Criar um pedido
order = Order.create({
    'customer_id': customer.id,
    'shipping_address': customer.address,
    'billing_address': customer.address
})

# Adicionar itens ao pedido
item = OrderItem.create({
    'order_id': order.id,
    'product_id': product.id,
    'quantity': 2,
    'price': product.price
})

# Calcular subtotal e total
item.calculate_subtotal()
order.calculate_total()

# Atualizar status do pedido
order.update_status(OrderStatus.PROCESSING)

# Criar uma avaliação
review = Review.create({
    'user_id': customer.id,
    'product_id': product.id,
    'rating': 5,
    'comment': 'Produto excelente!'
})

# Consultas
# Buscar produtos em destaque
featured_products = Product.where('featured', True).get()

# Buscar produtos por categoria
electronics_products = Product.where('category_id', electronics.id).get()

# Buscar pedidos em processamento
processing_orders = Order.where('status', OrderStatus.PROCESSING).get()

# Buscar avaliações de um produto
product_reviews = Review.where('product_id', product.id).get()

# Buscar pedidos de um cliente
customer_orders = Order.where('customer_id', customer.id).get()

# Buscar produtos com baixo estoque
low_stock_products = Product.where('stock', '<', 5).get()

# Buscar produtos mais vendidos
best_selling_products = (
    Product.join('order_items')
    .group_by('products.id')
    .order_by('sum(order_items.quantity)', 'desc')
    .limit(10)
    .get()
)
```

### Sistema de E-commerce

Este exemplo demonstra como criar um sistema de e-commerce completo usando QuentORM. Vamos implementar modelos para produtos, categorias, pedidos, clientes e avaliações.

#### 1. Modelos

#### Cliente (Customer)
O modelo `Customer` representa um cliente do e-commerce, com informações pessoais, endereços e métodos de pagamento. Cada cliente pode ter múltiplos endereços para entrega e faturamento.

```python
class Customer(BaseModel):
    """Modelo de cliente com dados de entrega e pagamento."""
    
    __tablename__ = 'customers'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(20))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    addresses = relationship('Address', back_populates='customer')
    orders = relationship('Order', back_populates='customer')
    reviews = relationship('Review', back_populates='customer')
```

#### Endereço (Address)
O modelo `Address` permite que clientes cadastrem múltiplos endereços para entrega e faturamento. Cada endereço está associado a um cliente específico.

```python
class Address(BaseModel):
    """Modelo de endereço para entrega e faturamento."""
    
    __tablename__ = 'addresses'
    
    id = Column(Integer, primary_key=True)
    street = Column(String(200), nullable=False)
    number = Column(String(20), nullable=False)
    complement = Column(String(100))
    neighborhood = Column(String(100), nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(2), nullable=False)
    zip_code = Column(String(9), nullable=False)
    is_default = Column(Boolean, default=False)
    
    # Chave estrangeira
    customer_id = Column(Integer, ForeignKey('customers.id'))
    
    # Relacionamentos
    customer = relationship('Customer', back_populates='addresses')
```

#### Categoria (Category)
O modelo `Category` organiza produtos em categorias e subcategorias, permitindo navegação hierárquica. Cada categoria pode ter uma categoria pai.

```python
class Category(BaseModel):
    """Modelo de categoria para produtos."""
    
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    slug = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    parent_id = Column(Integer, ForeignKey('categories.id'))
    
    # Relacionamentos
    parent = relationship('Category', remote_side=[id])
    products = relationship('Product', back_populates='category')
```

#### Produto (Product)
O modelo `Product` representa um produto do catálogo, com informações detalhadas, preço, estoque e imagens. Cada produto pertence a uma categoria.

```python
class Product(BaseModel):
    """Modelo de produto com variações e imagens."""
    
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    slug = Column(String(200), unique=True, nullable=False)
    description = Column(Text)
    price = Column(Float)
    stock = Column(Integer)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    
    # Chave estrangeira
    category_id = Column(Integer, ForeignKey('categories.id'))
    
    # Relacionamentos
    category = relationship('Category', back_populates='products')
    images = relationship('ProductImage', back_populates='product')
    order_items = relationship('OrderItem', back_populates='product')
    reviews = relationship('Review', back_populates='product')
```

#### Imagem do Produto (ProductImage)
O modelo `ProductImage` permite que produtos tenham múltiplas imagens, com suporte a imagem principal e miniaturas.

```python
class ProductImage(BaseModel):
    """Modelo de imagem de produto."""
    
    __tablename__ = 'product_images'
    
    id = Column(Integer, primary_key=True)
    url = Column(String(255), nullable=False)
    is_main = Column(Boolean, default=False)
    
    # Chave estrangeira
    product_id = Column(Integer, ForeignKey('products.id'))
    
    # Relacionamentos
    product = relationship('Product', back_populates='images')
```

#### Pedido (Order)
O modelo `Order` representa um pedido completo, com itens, status, endereço de entrega e pagamento. Cada pedido está associado a um cliente.

```python
class Order(BaseModel):
    """Modelo de pedido com itens e status."""
    
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True)
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
    total = Column(Numeric(10, 2), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    
    # Chaves estrangeiras
    customer_id = Column(Integer, ForeignKey('customers.id'))
    shipping_address_id = Column(Integer, ForeignKey('addresses.id'))
    billing_address_id = Column(Integer, ForeignKey('addresses.id'))
    
    # Relacionamentos
    customer = relationship('Customer', back_populates='orders')
    shipping_address = relationship('Address', foreign_keys=[shipping_address_id])
    billing_address = relationship('Address', foreign_keys=[billing_address_id])
    items = relationship('OrderItem', back_populates='order')
```

#### Item do Pedido (OrderItem)
O modelo `OrderItem` representa um item específico em um pedido, com quantidade, preço e subtotal.

```python
class OrderItem(BaseModel):
    """Modelo de item do pedido."""
    
    __tablename__ = 'order_items'
    
    id = Column(Integer, primary_key=True)
    quantity = Column(Integer, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    subtotal = Column(Numeric(10, 2), nullable=False)
    
    # Chaves estrangeiras
    order_id = Column(Integer, ForeignKey('orders.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    
    # Relacionamentos
    order = relationship('Order', back_populates='items')
    product = relationship('Product', back_populates='order_items')
```

#### Avaliação (Review)
O modelo `Review` permite que clientes avaliem produtos com nota e comentário.

```python
class Review(BaseModel):
    """Modelo de avaliação de produto."""
    
    __tablename__ = 'reviews'
    
    id = Column(Integer, primary_key=True)
    rating = Column(Integer, nullable=False)
    comment = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Chaves estrangeiras
    customer_id = Column(Integer, ForeignKey('customers.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    
    # Relacionamentos
    customer = relationship('Customer', back_populates='reviews')
    product = relationship('Product', back_populates='reviews')
```

### 2. Migrações

A migração inicial cria todas as tabelas necessárias para o sistema de e-commerce, incluindo índices para otimização de consultas.

```python
class CreateTables(BaseMigration):
    """Cria todas as tabelas necessárias para o sistema de e-commerce."""
    
    def up(self):
        with self.transaction():
            # Criação das tabelas
            self.create_table('customers', [
                Column('id', Integer, primary_key=True),
                Column('name', String(100), nullable=False),
                Column('email', String(100), unique=True, nullable=False),
                Column('phone', String(20)),
                Column('created_at', DateTime, default=datetime.utcnow)
            ])
            
            self.create_table('addresses', [
                Column('id', Integer, primary_key=True),
                Column('street', String(200), nullable=False),
                Column('number', String(20), nullable=False),
                Column('complement', String(100)),
                Column('neighborhood', String(100), nullable=False),
                Column('city', String(100), nullable=False),
                Column('state', String(2), nullable=False),
                Column('zip_code', String(9), nullable=False),
                Column('is_default', Boolean, default=False),
                Column('customer_id', Integer, ForeignKey('customers.id'))
            ])
            
            self.create_table('categories', [
                Column('id', Integer, primary_key=True),
                Column('name', String(100), nullable=False),
                Column('slug', String(100), unique=True, nullable=False),
                Column('description', Text),
                Column('parent_id', Integer, ForeignKey('categories.id'))
            ])
            
            self.create_table('products', [
                Column('id', Integer, primary_key=True),
                Column('name', String(200), nullable=False),
                Column('slug', String(200), unique=True, nullable=False),
                Column('description', Text),
                Column('price', Float),
                Column('stock', Integer),
                Column('active', Boolean, default=True),
                Column('created_at', DateTime, default=datetime.utcnow),
                Column('updated_at', DateTime, onupdate=datetime.utcnow),
                Column('category_id', Integer, ForeignKey('categories.id'))
            ])
            
            self.create_table('product_images', [
                Column('id', Integer, primary_key=True),
                Column('url', String(255), nullable=False),
                Column('is_main', Boolean, default=False),
                Column('product_id', Integer, ForeignKey('products.id'))
            ])
            
            self.create_table('orders', [
                Column('id', Integer, primary_key=True),
                Column('status', Enum(OrderStatus), default=OrderStatus.PENDING),
                Column('total', Numeric(10, 2), nullable=False),
                Column('created_at', DateTime, default=datetime.utcnow),
                Column('updated_at', DateTime, onupdate=datetime.utcnow),
                Column('customer_id', Integer, ForeignKey('customers.id')),
                Column('shipping_address_id', Integer, ForeignKey('addresses.id')),
                Column('billing_address_id', Integer, ForeignKey('addresses.id'))
            ])
            
            self.create_table('order_items', [
                Column('id', Integer, primary_key=True),
                Column('quantity', Integer, nullable=False),
                Column('price', Numeric(10, 2), nullable=False),
                Column('subtotal', Numeric(10, 2), nullable=False),
                Column('order_id', Integer, ForeignKey('orders.id')),
                Column('product_id', Integer, ForeignKey('products.id'))
            ])
            
            self.create_table('reviews', [
                Column('id', Integer, primary_key=True),
                Column('rating', Integer, nullable=False),
                Column('comment', Text),
                Column('created_at', DateTime, default=datetime.utcnow),
                Column('customer_id', Integer, ForeignKey('customers.id')),
                Column('product_id', Integer, ForeignKey('products.id'))
            ])
            
            # Criação dos índices
            self.create_index('customers', 'email')
            self.create_index('addresses', 'customer_id')
            self.create_index('categories', 'slug')
            self.create_index('categories', 'parent_id')
            self.create_index('products', 'slug')
            self.create_index('products', 'category_id')
            self.create_index('product_images', 'product_id')
            self.create_index('orders', 'customer_id')
            self.create_index('orders', 'status')
            self.create_index('order_items', 'order_id')
            self.create_index('order_items', 'product_id')
            self.create_index('reviews', 'customer_id')
            self.create_index('reviews', 'product_id')

    def down(self):
        with self.transaction():
            # Remoção das tabelas na ordem inversa
            self.drop_table('reviews')
            self.drop_table('order_items')
            self.drop_table('orders')
            self.drop_table('product_images')
            self.drop_table('products')
            self.drop_table('categories')
            self.drop_table('addresses')
            self.drop_table('customers')
```

### 3. Exemplos de Uso

Esta seção demonstra como utilizar os modelos do sistema de e-commerce em situações práticas. Cada exemplo inclui explicações detalhadas sobre o que está sendo feito e por quê.

#### Criando um Cliente
Este exemplo mostra como criar um novo cliente com endereço. O processo envolve:
1. Criar uma instância do modelo `Customer` com dados básicos
2. Criar um endereço associado ao cliente
3. Validar os dados antes de salvar
4. Usar uma transação para garantir a consistência dos dados

```python
def create_customer():
    """Demonstra como criar um novo cliente com endereço."""
    # 1. Cria o cliente com dados básicos
    customer = Customer(
        name='Maria Silva',
        email='maria@example.com',
        phone='(11) 99999-9999'
    )
    
    # 2. Cria o endereço associado ao cliente
    address = Address(
        street='Rua das Flores',
        number='123',
        neighborhood='Centro',
        city='São Paulo',
        state='SP',
        zip_code='01234-567',
        is_default=True,
        customer=customer  # Associa o endereço ao cliente
    )
    
    # 3. Valida os dados antes de salvar
    if customer.is_valid():
        # 4. Usa uma transação para garantir consistência
        with transaction():
            customer.save()
            address.save()
            print(f"Cliente {customer.name} criado com sucesso!")
    else:
        print(f"Erros: {customer.errors}")
```

#### Criando um Produto
Este exemplo demonstra como criar um produto com imagens. O processo inclui:
1. Buscar a categoria existente
2. Criar o produto com dados detalhados
3. Adicionar múltiplas imagens
4. Salvar tudo em uma transação

```python
def create_product():
    """Demonstra como criar um novo produto com imagens."""
    # 1. Busca a categoria existente
    category = Category.query.filter_by(slug='eletronicos').first()
    if not category:
        raise Exception("Categoria não encontrada")
    
    # 2. Cria o produto com dados detalhados
    product = Product(
        name='Smartphone XYZ',
        slug='smartphone-xyz',
        description='Smartphone de última geração...',
        price=1999.99,
        stock=10,
        category=category  # Associa o produto à categoria
    )
    
    # 3. Adiciona múltiplas imagens
    image1 = ProductImage(url='smartphone-xyz-1.jpg', is_main=True)
    image2 = ProductImage(url='smartphone-xyz-2.jpg')
    product.images.extend([image1, image2])
    
    # 4. Salva tudo em uma transação
    with transaction():
        product.save()
        print(f"Produto {product.name} criado com sucesso!")
```

#### Processando um Pedido
Este exemplo mostra o fluxo completo de processamento de um pedido:
1. Buscar o cliente e produtos
2. Criar os itens do pedido
3. Criar o pedido com endereços
4. Verificar estoque
5. Atualizar estoque
6. Salvar o pedido

```python
def process_order():
    """Demonstra como criar e processar um pedido."""
    # 1. Busca o cliente e produtos
    customer = Customer.query.filter_by(email='maria@example.com').first()
    if not customer:
        raise Exception("Cliente não encontrado")
    
    product1 = Product.query.filter_by(slug='smartphone-xyz').first()
    product2 = Product.query.filter_by(slug='tablet-abc').first()
    
    # 2. Cria os itens do pedido
    item1 = OrderItem(
        product=product1,
        quantity=1,
        price=product1.price,
        subtotal=product1.price * 1
    )
    
    item2 = OrderItem(
        product=product2,
        quantity=2,
        price=product2.price,
        subtotal=product2.price * 2
    )
    
    # 3. Cria o pedido com endereços
    order = Order(
        customer=customer,
        shipping_address=customer.addresses[0],
        billing_address=customer.addresses[0],
        items=[item1, item2]
    )
    
    # Calcula o total do pedido
    order.total = order.calculate_total()
    
    # Processa o pedido em uma transação
    with transaction():
        # 4. Verifica estoque
        for item in order.items:
            if not item.product.is_in_stock():
                raise Exception(f"Produto {item.product.name} sem estoque")
        
        # 5. Diminui estoque
        for item in order.items:
            item.product.decrease_stock(item.quantity)
        
        # 6. Salva o pedido
        order.save()
        print(f"Pedido #{order.id} criado com sucesso!")
```

#### Consultas Comuns
Este exemplo demonstra consultas frequentes no sistema:
1. Produtos em destaque
2. Produtos por categoria
3. Pedidos pendentes
4. Produtos com baixo estoque
5. Avaliações recentes

```python
def common_queries():
    """Demonstra consultas comuns no sistema de e-commerce."""
    
    # 1. Produtos em destaque (mais recentes)
    featured_products = Product.query.filter_by(
        active=True
    ).order_by(
        Product.created_at.desc()
    ).limit(10).all()
    
    # 2. Produtos por categoria
    electronics = Product.query.join(Category).filter(
        Category.slug == 'eletronicos'
    ).all()
    
    # 3. Pedidos pendentes
    pending_orders = Order.query.filter_by(
        status=OrderStatus.PENDING
    ).all()
    
    # 4. Produtos com baixo estoque
    low_stock = Product.query.filter(
        Product.stock < 5
    ).all()
    
    # 5. Avaliações recentes
    recent_reviews = Review.query.order_by(
        Review.created_at.desc()
    ).limit(10).all()
```

## 1️⃣2️⃣ Solução de Problemas

### Problemas Comuns

1. **Erros de Conexão**: Se você estiver enfrentando problemas de conexão com o banco de dados, verifique se:
   - O driver do banco de dados está instalado corretamente
   - O arquivo `.env` está configurado corretamente
   - O banco de dados está em execução
   - O usuário e senha estão corretos

2. **Erros de Autenticação**: Se você estiver enfrentando problemas de autenticação, verifique se:
   - O usuário e senha estão corretos
   - O banco de dados está configurado para autenticação
   - O arquivo `.env` está configurado corretamente

3. **Erros de Validação**: Se você estiver enfrentando problemas de validação, verifique se:
   - Os campos obrigatórios estão sendo preenchidos
   - As regras de validação estão corretas
   - O sistema de validação está funcionando corretamente

4. **Erros de Eventos**: Se você estiver enfrentando problemas com eventos, verifique se:
   - Os eventos estão sendo disparados corretamente
   - O código de eventos está correto
   - O sistema de eventos está funcionando corretamente

5. **Erros de Migrações**: Se você estiver enfrentando problemas com migrações, verifique se:
   - As migrações estão sendo criadas corretamente
   - O comando `quentorm migrate` está funcionando corretamente
   - O arquivo de migração está correto

6. **Erros de Consultas**: Se você estiver enfrentando problemas com consultas, verifique se:
   - As consultas estão sendo construídas corretamente
   - O código de consultas está correto
   - O sistema de consultas está funcionando corretamente

7. **Erros de Validações**: Se você estiver enfrentando problemas de validação, verifique se:
   - Os campos obrigatórios estão sendo preenchidos
   - As regras de validação estão corretas
   - O sistema de validação está funcionando corretamente

8. **Erros de Eventos**: Se você estiver enfrentando problemas com eventos, verifique se:
   - Os eventos estão sendo disparados corretamente
   - O código de eventos está correto
   - O sistema de eventos está funcionando corretamente

9. **Erros de CLI**: Se você estiver enfrentando problemas com o CLI, verifique se:
   - O comando `quentorm migrate` está funcionando corretamente
   - O comando `quentorm make:migration` está funcionando corretamente
   - O arquivo de migração está correto

10. **Erros de Boas Práticas**: Se você estiver enfrentando problemas com boas práticas, verifique se:
    - O código está organizado corretamente
    - O código está seguindo as boas práticas
    - O sistema está funcionando corretamente

### Soluções

1. **Erros de Conexão**: Verifique se o banco de dados está em execução e se o usuário e senha estão corretos.
2. **Erros de Autenticação**: Verifique se o banco de dados está configurado para autenticação e se o usuário e senha estão corretos.
3. **Erros de Validação**: Verifique se os campos obrigatórios estão sendo preenchidos e se as regras de validação estão corretas.
4. **Erros de Eventos**: Verifique se os eventos estão sendo disparados corretamente e se o código de eventos está correto.
5. **Erros de Migrações**: Verifique se as migrações estão sendo criadas corretamente e se o comando `quentorm migrate` está funcionando corretamente.
6. **Erros de Consultas**: Verifique se as consultas estão sendo construídas corretamente e se o código de consultas está correto.
7. **Erros de Validações**: Verifique se os campos obrigatórios estão sendo preenchidos e se as regras de validação estão corretas.
8. **Erros de Eventos**: Verifique se os eventos estão sendo disparados corretamente e se o código de eventos está correto.
9. **Erros de CLI**: Verifique se o comando `quentorm migrate` está funcionando corretamente e se o comando `quentorm make:migration` está funcionando corretamente.
10. **Erros de Boas Práticas**: Verifique se o código está organizado corretamente e se está seguindo as boas práticas.

## 1️⃣3️⃣ Cache

O sistema de cache do QuentORM permite armazenar temporariamente dados frequentemente acessados para melhorar o desempenho da aplicação. Existem três principais formas de utilizar o cache:

### Cache Básico

O cache básico é ideal para armazenar resultados de métodos que retornam dados que não mudam com frequência. Por exemplo, detalhes de um produto ou avaliações podem ser cacheados por um período determinado para reduzir consultas ao banco de dados.

```python
from quentorm import BaseModel, cache

class Product(BaseModel):
    __tablename__ = 'products'
    
    @cache('product_details', ttl=3600)  # Cache por 1 hora
    def get_details(self):
        return {
            'name': self.name,
            'price': self.price,
            'stock': self.stock,
            'category': self.category.name
        }
    
    @cache('product_reviews', ttl=1800)  # Cache por 30 minutos
    def get_reviews(self):
        return [
            {'user': review.user.name, 'rating': review.rating}
            for review in self.reviews
        ]
```

O decorador `@cache` recebe dois parâmetros principais:
- `key`: Uma string única que identifica o cache
- `ttl`: Tempo de vida do cache em segundos

### Cache de Consultas

Para consultas que são executadas frequentemente mas não precisam estar sempre atualizadas, o QuentORM oferece o cache de consultas. Isso é particularmente útil para estatísticas ou listagens que podem ser atualizadas periodicamente.

```python
from quentorm import BaseModel, cache_query

class User(BaseModel):
    __tablename__ = 'users'
    
    @classmethod
    @cache_query(ttl=300)  # Cache por 5 minutos
    def get_active_users(cls):
        return cls.where('active', True).all()
    
    @classmethod
    @cache_query(ttl=600)  # Cache por 10 minutos
    def get_user_count_by_role(cls):
        return cls.group_by('role').count()
```

O decorador `@cache_query` é específico para métodos que retornam consultas ao banco de dados.

### Invalidação de Cache

Em alguns casos, é necessário invalidar o cache manualmente quando os dados são modificados. O QuentORM fornece o decorador `@invalidate_cache` para esse propósito.

```python
from quentorm import BaseModel, invalidate_cache

class Order(BaseModel):
    __tablename__ = 'orders'
    
    @invalidate_cache('user_orders')
    def save(self):
        super().save()
    
    @invalidate_cache(['user_stats', 'order_stats'])
    def process(self):
        self.status = 'processed'
        self.save()
```

O decorador `@invalidate_cache` pode receber:
- Uma única chave de cache como string
- Uma lista de chaves de cache para invalidar múltiplos caches de uma vez

## 1️⃣4️⃣ Logging

O sistema de logging do QuentORM permite rastrear eventos e operações importantes na aplicação. Existem três níveis principais de logging:

### Logging Básico

O logging básico é útil para registrar operações importantes no sistema, como login de usuários ou alterações de status.

```python
from quentorm import BaseModel, log

class User(BaseModel):
    __tablename__ = 'users'
    
    @log('info')
    def login(self):
        self.last_login = datetime.now()
        self.save()
    
    @log('warning')
    def block(self):
        self.active = False
        self.blocked_at = datetime.now()
        self.save()
```

O decorador `@log` aceita diferentes níveis de log:
- `debug`: Para informações de desenvolvimento
- `info`: Para eventos normais do sistema
- `warning`: Para situações potencialmente problemáticas
- `error`: Para erros que precisam de atenção
- `critical`: Para erros críticos que afetam o funcionamento do sistema

### Logging de Consultas

Para monitorar consultas específicas ao banco de dados, especialmente aquelas que podem impactar o desempenho, use o logging de consultas.

```python
from quentorm import BaseModel, log_query

class Product(BaseModel):
    __tablename__ = 'products'
    
    @classmethod
    @log_query
    def get_low_stock_products(cls):
        return cls.where('stock', '<', 10).all()
    
    @classmethod
    @log_query(level='warning')
    def get_out_of_stock_products(cls):
        return cls.where('stock', 0).all()
```

O decorador `@log_query` registra:
- Tempo de execução da consulta
- SQL gerado
- Parâmetros utilizados
- Número de registros retornados

### Logging Personalizado

Para casos mais específicos, o QuentORM permite criar logs personalizados com informações detalhadas.

```python
from quentorm import BaseModel, custom_log

class Order(BaseModel):
    __tablename__ = 'orders'
    
    @custom_log
    def process_payment(self, payment_data):
        log_data = {
            'order_id': self.id,
            'amount': self.total,
            'payment_method': payment_data['method']
        }
        return log_data
    
    @custom_log(handler='audit')
    def refund(self, reason):
        log_data = {
            'order_id': self.id,
            'amount': self.total,
            'reason': reason,
            'user': self.refunded_by
        }
        return log_data
```

O decorador `@custom_log` permite:
- Definir quais dados serão registrados
- Usar handlers personalizados para diferentes tipos de log
- Integrar com sistemas externos de logging

### Recursos Adicionais

- [Documentação do SQLAlchemy](https://docs.sqlalchemy.org/)
- [Documentação do Alembic](https://alembic.sqlalchemy.org/)
- [Documentação do Pydantic](https://pydantic-docs.helpmanual.io/)
- [Documentação do Click](https://click.palletsprojects.com/)

### Suporte

Se você ainda tiver dúvidas ou problemas:

1. Consulte a documentação oficial
2. Abra uma issue no GitHub
3. Participe da comunidade no Discord
4. Procure ajuda no Stack Overflow

Lembre-se: A melhor forma de aprender é praticando e experimentando!