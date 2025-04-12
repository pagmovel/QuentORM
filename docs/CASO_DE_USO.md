# 📚 Casos de Uso do QuentORM

## 🎯 Introdução

Este documento apresenta exemplos práticos de como utilizar o QuentORM em diferentes cenários de desenvolvimento.

## 📋 Índice

1. [Modelos Básicos](#modelos-básicos)
2. [Relacionamentos](#relacionamentos)
3. [Consultas Avançadas](#consultas-avançadas)
4. [Validações](#validações)
5. [Eventos](#eventos)

## 📦 Modelos Básicos

### Usuário

```python
from quentorm import Model

class Usuario(Model):
    __fillable__ = ['nome', 'email', 'senha']
    __hidden__ = ['senha']
    
    def validar(self):
        if not self.email or '@' not in self.email:
            raise ValueError("Email inválido")
        return True

# Criar usuário
usuario = Usuario()
usuario.nome = "João Silva"
usuario.email = "joao@email.com"
usuario.senha = "123456"
usuario.save()

# Buscar usuário
usuario = Usuario.find(1)
print(usuario.nome)  # João Silva
```

### Post

```python
from quentorm import Model

class Post(Model):
    __fillable__ = ['titulo', 'conteudo', 'usuario_id']
    
    def validar(self):
        if not self.titulo or len(self.titulo) < 3:
            raise ValueError("Título muito curto")
        return True

# Criar post
post = Post()
post.titulo = "Meu Primeiro Post"
post.conteudo = "Conteúdo do post..."
post.usuario_id = 1
post.save()
```

## 🔗 Relacionamentos

### Um para Um

```python
class Usuario(Model):
    def perfil(self):
        return self.has_one(Perfil)

class Perfil(Model):
    def usuario(self):
        return self.belongs_to(Usuario)

# Usar relacionamento
usuario = Usuario.find(1)
perfil = usuario.perfil
print(perfil.bio)
```

### Um para Muitos

```python
class Usuario(Model):
    def posts(self):
        return self.has_many(Post)

class Post(Model):
    def usuario(self):
        return self.belongs_to(Usuario)

# Usar relacionamento
usuario = Usuario.find(1)
posts = usuario.posts
for post in posts:
    print(post.titulo)
```

### Muitos para Muitos

```python
class Usuario(Model):
    def roles(self):
        return self.belongs_to_many(Role)

class Role(Model):
    def usuarios(self):
        return self.belongs_to_many(Usuario)

# Usar relacionamento
usuario = Usuario.find(1)
roles = usuario.roles
for role in roles:
    print(role.nome)
```

## 🔍 Consultas Avançadas

### Eager Loading

```python
# Carregar usuários com posts
usuarios = Usuario.with_('posts').get()

for usuario in usuarios:
    print(f"{usuario.nome} tem {len(usuario.posts)} posts")
```

### Consultas Complexas

```python
# Posts recentes de usuários ativos
posts = Post.join('usuarios', 'usuarios.id', '=', 'posts.usuario_id') \
           .where('usuarios.ativo', True) \
           .where('posts.data', '>', '2023-01-01') \
           .order_by('posts.data', 'desc') \
           .get()
```

### Agregações

```python
# Estatísticas de posts
estatisticas = Post.select(
    'usuario_id',
    Post.raw('COUNT(*) as total_posts'),
    Post.raw('MAX(data) as ultimo_post')
).group_by('usuario_id').get()
```

## ✅ Validações

### Validação de Modelo

```python
class Produto(Model):
    __fillable__ = ['nome', 'preco', 'estoque']
    
    def validar(self):
        if self.preco <= 0:
            raise ValueError("Preço deve ser maior que zero")
        if self.estoque < 0:
            raise ValueError("Estoque não pode ser negativo")
        return True

# Usar validação
try:
    produto = Produto()
    produto.nome = "Notebook"
    produto.preco = -1000
    produto.save()
except ValueError as e:
    print(f"Erro: {e}")
```

### Validação em Massa

```python
def validar_produtos(produtos):
    validos = []
    invalidos = []
    
    for produto in produtos:
        try:
            produto.validar()
            validos.append(produto)
        except ValueError as e:
            invalidos.append({
                'produto': produto,
                'erro': str(e)
            })
    
    return validos, invalidos
```

## 🔔 Eventos

### Observers

```python
from quentorm import Observer

class ProdutoObserver(Observer):
    def creating(self, produto):
        produto.sku = gerar_sku(produto.nome)
    
    def updating(self, produto):
        if produto.is_dirty('preco'):
            registrar_alteracao_preco(produto)
    
    def deleting(self, produto):
        if produto.estoque > 0:
            raise ValueError("Não é possível deletar produto com estoque")

# Registrar observer
Produto.observe(ProdutoObserver())
```

### Eventos Personalizados

```python
class Produto(Model):
    def baixar_estoque(self, quantidade):
        if quantidade > self.estoque:
            raise ValueError("Estoque insuficiente")
        
        self.estoque -= quantidade
        self.save()
        
        # Disparar evento
        self.fire_event('estoque_baixado', {
            'quantidade': quantidade,
            'novo_estoque': self.estoque
        })
``` 