# Validações no Quentorm

## Índice

1. [Introdução](#introdução)
2. [Tipos de Validação](#tipos-de-validação)
3. [Mensagens de Validação](#mensagens-de-validação)
4. [Exemplos de Uso](#exemplos-de-uso)
5. [Boas Práticas](#boas-práticas)

## Introdução

O Quentorm oferece um sistema robusto de validação de dados, com suporte a múltiplos tipos de validação e internacionalização de mensagens.

## Tipos de Validação

### Documentos

#### CPF

Valida números de CPF (Cadastro de Pessoas Físicas) brasileiros.

**Regras:**
- Deve conter 11 dígitos
- Não pode ter todos os dígitos iguais
- Deve ter dígitos verificadores válidos

**Exemplo:**
```python
from quentorm import Model, Field

class Cliente(Model):
    cpf = Field(str, validators=['cpf'])
```

#### CNPJ

Valida números de CNPJ (Cadastro Nacional da Pessoa Jurídica) brasileiros.

**Regras:**
- Deve conter 14 dígitos
- Não pode ter todos os dígitos iguais
- Deve ter dígitos verificadores válidos

**Exemplo:**
```python
from quentorm import Model, Field

class Fornecedor(Model):
    cnpj = Field(str, validators=['cnpj'])
```

#### CPF/CNPJ Automático

Detecta automaticamente se o número é CPF ou CNPJ e aplica a validação apropriada.

**Exemplo:**
```python
from quentorm import Model, Field

class Pessoa(Model):
    documento = Field(str, validators=['cpf_cnpj'])
```

### Dados Bancários

#### Agência

Valida números de agência bancária.

**Regras:**
- Deve conter 4 dígitos
- Deve conter apenas números

**Exemplo:**
```python
from quentorm import Model, Field

class ContaBancaria(Model):
    agencia = Field(str, validators=['agencia'])
```

#### Conta

Valida números de conta bancária.

**Regras:**
- Deve conter entre 5 e 10 dígitos
- Deve conter apenas números

**Exemplo:**
```python
from quentorm import Model, Field

class ContaBancaria(Model):
    conta = Field(str, validators=['conta'])
```

#### Dígito Verificador

Valida dígitos verificadores de contas bancárias.

**Regras:**
- Deve conter no máximo 2 dígitos
- Pode ser vazio

**Exemplo:**
```python
from quentorm import Model, Field

class ContaBancaria(Model):
    digito = Field(str, validators=['digito'])
```

### Dados Pessoais

#### Email

Valida endereços de email.

**Regras:**
- Deve seguir o formato padrão de email
- Deve conter um domínio válido

**Exemplo:**
```python
from quentorm import Model, Field

class Cliente(Model):
    email = Field(str, validators=['email'])
```

#### Telefone

Valida números de telefone brasileiros.

**Regras:**
- Deve conter entre 10 e 11 dígitos
- Deve seguir o formato brasileiro

**Exemplo:**
```python
from quentorm import Model, Field

class Cliente(Model):
    telefone = Field(str, validators=['telefone'])
```

#### CEP

Valida códigos postais brasileiros.

**Regras:**
- Deve conter 8 dígitos
- Deve conter apenas números

**Exemplo:**
```python
from quentorm import Model, Field

class Endereco(Model):
    cep = Field(str, validators=['cep'])
```

## Mensagens de Validação

As mensagens de validação são armazenadas em arquivos JSON na pasta `config/messages/`. Por padrão, são fornecidos arquivos em português (pt-br) e inglês (en).

### Estrutura do Arquivo de Mensagens

```json
{
    "cpf": {
        "invalid_length": "CPF deve conter 11 dígitos",
        "invalid_digits": "CPF não pode ter todos os dígitos iguais",
        "invalid_verifier": "CPF inválido",
        "valid": "CPF válido"
    },
    "cnpj": {
        "invalid_length": "CNPJ deve conter 14 dígitos",
        "invalid_digits": "CNPJ não pode ter todos os díginhos iguais",
        "invalid_verifier": "CNPJ inválido",
        "valid": "CNPJ válido"
    }
}
```

### Adicionando um Novo Idioma

Para adicionar um novo idioma:

1. Crie um arquivo JSON na pasta `config/messages/` com o código do idioma (ex: `es.json` para espanhol)
2. Copie a estrutura do arquivo de mensagens existente
3. Traduza as mensagens para o novo idioma

## Exemplos de Uso

### Validação Básica

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

### Validação em Massa

```python
from quentorm import Model, Field

class Cliente(Model):
    nome = Field(str)
    cpf = Field(str, validators=['cpf'])
    email = Field(str, validators=['email'])

# Lista de clientes para validar
clientes = [
    {"nome": "João Silva", "cpf": "12345678901", "email": "joao@exemplo.com"},
    {"nome": "Maria Santos", "cpf": "98765432100", "email": "maria@exemplo.com"}
]

# Validando todos os clientes
for dados in clientes:
    cliente = Cliente(**dados)
    try:
        cliente.validate()
        print(f"Cliente {cliente.nome} válido")
    except ValidationError as e:
        print(f"Erro no cliente {cliente.nome}: {e.message}")
```

## Boas Práticas

1. **Valide cedo e frequentemente**
   - Valide os dados assim que eles entram no sistema
   - Não confie em validações do frontend

2. **Mensagens claras**
   - Use mensagens de erro descritivas
   - Inclua sugestões de correção quando possível

3. **Tratamento de erros**
   - Capture e trate exceções de validação
   - Registre erros de validação para análise

4. **Validação em camadas**
   - Use validações no modelo
   - Adicione validações específicas no serviço
   - Implemente validações de negócio quando necessário

5. **Testes**
   - Teste casos válidos e inválidos
   - Teste casos limite
   - Teste internacionalização

6. **Internacionalização**
   - Use o sistema de mensagens internacionalizado
   - Mantenha as mensagens atualizadas
   - Adicione novos idiomas conforme necessário

7. **Performance**
   - Evite validações desnecessárias
   - Use validações em massa quando possível
   - Cache resultados de validação quando apropriado