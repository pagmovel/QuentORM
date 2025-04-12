# 📚 Manual do QuentORM

## 🎯 Introdução

O QuentORM é um ORM (Object-Relational Mapping) inspirado no Laravel/Eloquent, projetado para Python. Ele oferece uma forma elegante e intuitiva de interagir com bancos de dados, seguindo os mesmos princípios e padrões do Eloquent.

## 📋 Índice

1. [Instalação](#instalação)
2. [Configuração](#configuração)
3. [Modelos](#modelos)
4. [Relacionamentos](#relacionamentos)
5. [Consultas](#consultas)
6. [Validações](#validações)
7. [Eventos](#eventos)
8. [Boas Práticas](#boas-práticas)

## 💻 Instalação

```bash
pip install quentorm
```

## ⚙️ Configuração

### Conexão com Banco de Dados

```python
from quentorm import Database

# Configurar conexão
Database.config({
    'driver': 'postgresql',
    'host': 'localhost',
    'database': 'meu_banco',
    'user': 'usuario',
    'password': 'senha'
})
```

### Configurações Adicionais

```python
# Configurar prefixo de tabelas
Database.set_table_prefix('app_')

# Configurar timezone
Database.set_timezone('America/Sao_Paulo')

# Configurar charset
Database.set_charset('utf8')
```

## 📦 Modelos

### Criar Modelo

```python
from quentorm import Model

class Usuario(Model):
    # Nome da tabela (opcional)
    __table__ = 'usuarios'
    
    # Chave primária (opcional)
    __primary_key__ = 'id'
    
    # Timestamps (opcional)
    __timestamps__ = True
    
    # Campos preenchíveis
    __fillable__ = ['nome', 'email', 'senha']
    
    # Campos ocultos
    __hidden__ = ['senha']
```

### Usar Modelo

```python
# Criar
usuario = Usuario()
usuario.nome = 'João'
usuario.email = 'joao@email.com'
usuario.save()

# Buscar
usuario = Usuario.find(1)
usuarios = Usuario.where('ativo', True).get()

# Atualizar
usuario.nome = 'João Silva'
usuario.save()

# Remover
usuario.delete()
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
```

### Um para Muitos

```python
class Usuario(Model):
    def posts(self):
        return self.has_many(Post)

class Post(Model):
    def usuario(self):
        return self.belongs_to(Usuario)
```

### Muitos para Muitos

```python
class Usuario(Model):
    def roles(self):
        return self.belongs_to_many(Role)

class Role(Model):
    def usuarios(self):
        return self.belongs_to_many(Usuario)
```

## 🔍 Consultas

### Básicas

```python
# Todos
usuarios = Usuario.all()

# Buscar por ID
usuario = Usuario.find(1)

# Primeiro
usuario = Usuario.first()

# Último
usuario = Usuario.last()
```

### Condicionais

```python
# Where
usuarios = Usuario.where('idade', '>', 18).get()

# Or
usuarios = Usuario.where('idade', '>', 18).or_where('ativo', True).get()

# In
usuarios = Usuario.where_in('id', [1, 2, 3]).get()

# Like
usuarios = Usuario.where('nome', 'like', '%João%').get()
```

### Ordenação e Limite

```python
# Order by
usuarios = Usuario.order_by('nome', 'asc').get()

# Limit
usuarios = Usuario.limit(10).get()

# Offset
usuarios = Usuario.offset(10).limit(10).get()
```

### Agregação

```python
# Count
total = Usuario.count()

# Sum
total_idade = Usuario.sum('idade')

# Avg
media_idade = Usuario.avg('idade')

# Max
maior_idade = Usuario.max('idade')

# Min
menor_idade = Usuario.min('idade')
```

## ✅ Validações

O QuentORM oferece um sistema robusto de validações para garantir a integridade dos dados. Consulte a documentação completa em `docs/VALIDACOES.md`.

### Exemplo Rápido

```python
from quentorm.utils.validators import validar_cpf

class Usuario(Model):
    def validar(self):
        resultado = validar_cpf(self.cpf)
        if not resultado.success:
            raise ValueError(resultado.message)
        return True
```

## 🔔 Eventos

### Observers

```python
from quentorm import Observer

class UsuarioObserver(Observer):
    def creating(self, usuario):
        usuario.senha = hash_password(usuario.senha)
    
    def updating(self, usuario):
        if usuario.is_dirty('senha'):
            usuario.senha = hash_password(usuario.senha)
```

### Registrando Observers

```python
Usuario.observe(UsuarioObserver())
```

## 💡 Boas Práticas

### Modelos

- Use nomes descritivos para modelos e tabelas
- Defina relacionamentos claramente
- Use fillable/hidden para controle de dados
- Implemente validações

### Consultas

- Use eager loading para relacionamentos
- Aproveite o query builder
- Otimize consultas complexas
- Use índices apropriados

### Performance

- Cache resultados quando possível
- Use paginação para grandes conjuntos
- Monitore queries lentas
- Otimize índices do banco

### Segurança

- Valide todos os inputs
- Use prepared statements
- Implemente controle de acesso
- Mantenha logs de alterações 