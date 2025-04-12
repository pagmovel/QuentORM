# QuentORM CLI

O QuentORM CLI é uma ferramenta de linha de comando que facilita o desenvolvimento com o QuentORM, oferecendo comandos similares ao Artisan do Laravel, mas focados em operações de banco de dados.

## Instalação

```bash
pip install quentorm-cli
```

## Comandos Disponíveis

### 1. Criar Projeto

O comando `new` é interativo e guia você na criação de um novo projeto. Ele suporta múltiplos idiomas e pode ser configurado para diferentes regiões.

#### Uso Básico

```bash
# Criar projeto com idioma padrão (pt-br)
quentorm new nome-do-projeto

# Criar projeto em inglês
quentorm new nome-do-projeto --lang en

# Criar projeto em espanhol
quentorm new nome-do-projeto --lang es
```

#### Configuração de Mensagens

As mensagens do CLI são gerenciadas através de arquivos JSON na pasta `config/messages/`. Cada idioma tem seu próprio arquivo:

```
config/
└── messages/
    ├── pt_br.json  # Português (padrão)
    ├── en.json     # Inglês
    └── es.json     # Espanhol
```

Para acessar as mensagens no código:

```python
from config.messages import messages

# Obter mensagem específica
welcome = messages.get('cli.new.welcome')

# Obter lista de mensagens
next_steps = messages.get_list('cli.new.next_steps')

# Mudar idioma
messages.set_language('en')
```

#### Estrutura das Mensagens

As mensagens são organizadas em seções:

1. **CLI**: Mensagens do comando `new`
2. **Validações**: Mensagens de validação (CPF, CNPJ, dados bancários)

Exemplo de estrutura:
```json
{
    "cli": {
        "new": {
            "welcome": "Bem-vindo ao assistente...",
            "project_name": "Digite o nome...",
            // ...
        }
    },
    "validations": {
        "cpf": {
            "invalid_length": "CPF deve ter...",
            // ...
        }
    }
}
```

#### Adicionando Novo Idioma

Para adicionar um novo idioma:

1. Crie um arquivo `config/messages/{idioma}.json`
2. Copie a estrutura do `pt_br.json`
3. Traduza as mensagens
4. O idioma estará automaticamente disponível no CLI

#### Exemplo de Uso com Diferentes Idiomas

```bash
# Português (padrão)
quentorm new meu-projeto
# Saída: "Bem-vindo ao assistente de criação de projetos QuentORM!"

# Inglês
quentorm new my-project --lang en
# Saída: "Welcome to QuentORM project creation wizard!"

# Espanhol
quentorm new mi-proyecto --lang es
# Saída: "¡Bienvenido al asistente de creación de proyectos QuentORM!"
```

#### Boas Práticas

1. **Organização**:
   - Mantenha as mensagens na pasta `config/messages/`
   - Use estrutura hierárquica clara
   - Documente alterações nas mensagens

2. **Internacionalização**:
   - Considere diferenças culturais
   - Adapte formatos de data/hora
   - Use caracteres especiais corretamente

3. **Manutenção**:
   - Mantenha arquivos de mensagens organizados
   - Teste em diferentes idiomas
   - Versionamento das mensagens

### 2. Gerenciamento de Modelos

#### Criar Modelo
```bash
quentorm make:model NomeDoModelo
```

Opções disponíveis:
- `--table`: Especificar nome da tabela
- `--migration`: Criar migração junto
- `--controller`: Criar controller junto
- `--resource`: Criar modelo com todos os recursos

Exemplo:
```bash
quentorm make:model User --table=users --migration --controller
```

#### Gerar Modelo a partir do Banco
```bash
quentorm model:generate
```

Opções disponíveis:
- `--connection`: Conexão específica
- `--table`: Tabela específica
- `--output`: Diretório de saída
- `--namespace`: Namespace dos modelos

Exemplo:
```bash
quentorm model:generate --connection=mysql --table=users --output=app/Models
```

### 3. Gerenciamento de Migrações

#### Criar Migração
```bash
quentorm make:migration nome_da_migracao
```

Exemplo:
```bash
quentorm make:migration create_users_table
```

#### Executar Migrações
```bash
quentorm migrate
```

Opções disponíveis:
- `--fresh`: Recriar banco de dados
- `--seed`: Executar seeders
- `--step`: Executar em etapas
- `--pretend`: Mostrar SQL sem executar

#### Rollback de Migrações
```bash
quentorm migrate:rollback
```

Opções disponíveis:
- `--step`: Número de migrações para reverter
- `--pretend`: Mostrar SQL sem executar

### 4. Gerenciamento de Seeders

#### Criar Seeder
```bash
quentorm make:seeder NomeDoSeeder
```

Exemplo:
```bash
quentorm make:seeder UserSeeder
```

#### Executar Seeders
```bash
quentorm db:seed
```

Opções disponíveis:
- `--class`: Seeder específico
- `--database`: Conexão específica

### 5. Gerenciamento de Banco de Dados

#### Criar Banco de Dados
```bash
quentorm db:create
```

#### Dropar Banco de Dados
```bash
quentorm db:drop
```

#### Limpar Banco de Dados
```bash
quentorm db:wipe
```

### 6. Comandos de Desenvolvimento

#### Iniciar Servidor de Desenvolvimento
```bash
quentorm serve
```

Opções disponíveis:
- `--host`: Host do servidor
- `--port`: Porta do servidor
- `--debug`: Modo debug

#### Limpar Cache
```bash
quentorm cache:clear
```

#### Gerar Documentação
```bash
quentorm docs:generate
```

### 7. Comandos de Produção

#### Otimizar Aplicação
```bash
quentorm optimize
```

#### Gerar Chave de Segurança
```bash
quentorm key:generate
```

## Comandos de Banco de Dados

### 1. Criar Banco de Dados
```bash
# Criar banco de dados padrão
quentorm db:create

# Criar banco específico
quentorm db:create --database=meu_banco

# Criar com configurações personalizadas
quentorm db:create --connection=mysql --charset=utf8mb4 --collation=utf8mb4_unicode_ci
```

Este comando:
- Cria um novo banco de dados
- Usa configurações do `.env` ou `config/database.py`
- Suporta diferentes drivers (MySQL, PostgreSQL, SQLite)
- Pode criar schemas em PostgreSQL

### 2. Dropar Banco de Dados
```bash
# Dropar banco padrão
quentorm db:drop

# Dropar banco específico
quentorm db:drop --database=meu_banco

# Dropar com confirmação
quentorm db:drop --force
```

Este comando:
- Remove o banco de dados completamente
- Pede confirmação antes de dropar
- Mantém backups se configurado
- Limpa conexões existentes

### 3. Limpar Banco de Dados
```bash
# Limpar todas as tabelas
quentorm db:wipe

# Limpar tabelas específicas
quentorm db:wipe --tables=users,posts

# Limpar com confirmação
quentorm db:wipe --force
```

Este comando:
- Remove todos os dados das tabelas
- Mantém a estrutura do banco
- Reseta sequências e auto-incrementos
- Pode ser usado em desenvolvimento

### 4. Backup do Banco de Dados
```bash
# Criar backup completo
quentorm db:backup

# Backup com nome específico
quentorm db:backup --name=backup_2023

# Backup de tabelas específicas
quentorm db:backup --tables=users,posts

# Backup com compressão
quentorm db:backup --compress
```

Este comando:
- Cria dump do banco de dados
- Suporta diferentes formatos (SQL, CSV, JSON)
- Mantém histórico de backups
- Pode ser agendado

### 5. Restaurar Backup
```bash
# Restaurar último backup
quentorm db:restore

# Restaurar backup específico
quentorm db:restore backup_2023.sql

# Restaurar com confirmação
quentorm db:restore --force
```

Este comando:
- Restaura dados do backup
- Verifica integridade
- Mantém logs de restauração
- Pode restaurar parcialmente

### 6. Otimizar Banco de Dados
```bash
# Otimizar todas as tabelas
quentorm db:optimize

# Otimizar tabelas específicas
quentorm db:optimize --tables=users,posts

# Otimizar com análise
quentorm db:optimize --analyze
```

Este comando:
- Otimiza tabelas e índices
- Analisa estatísticas
- Remove fragmentação
- Melhora performance

### 7. Verificar Status
```bash
# Verificar status do banco
quentorm db:status

# Verificar tamanho das tabelas
quentorm db:status --size

# Verificar conexões
quentorm db:status --connections
```

Este comando:
- Mostra informações do banco
- Exibe estatísticas
- Verifica saúde
- Monitora recursos

## Comandos de Validação

### Validar Documentos
```bash
# Validar CPF
quentorm validate:cpf 123.456.789-09

# Validar CNPJ
quentorm validate:cnpj 12.345.678/0001-95

# Validar CPF/CNPJ (automático)
quentorm validate:document 123.456.789-09
quentorm validate:document 12.345.678/0001-95
```

### Validar Dados Bancários
```bash
# Validar Agência
quentorm validate:agency 1234-5

# Validar Conta
quentorm validate:account 12345-6

# Validar Dígito
quentorm validate:digit 7
```

### Validação em Massa
```bash
# Validar múltiplos documentos
quentorm validate:batch documents.txt

# Validar múltiplas contas
quentorm validate:batch accounts.txt
```

### Gerar Validações
```bash
# Gerar validação de CPF/CNPJ
quentorm make:validator DocumentValidator

# Gerar validação de conta bancária
quentorm make:validator BankAccountValidator
```

### Validações Personalizadas

#### Criar Validador
```bash
# Criar validador básico
quentorm make:validator NomeDoValidador

# Criar validador com configurações
quentorm make:validator NomeDoValidador --config

# Criar validador com testes
quentorm make:validator NomeDoValidador --test
```

#### Registrar Validador
```bash
# Registrar validador para uso no CLI
quentorm validator:register NomeDoValidador

# Registrar com alias
quentorm validator:register NomeDoValidador --alias=meu_validador

# Registrar com configurações
quentorm validator:register NomeDoValidador --config=config.json
```

#### Usar Validação
```bash
# Usar validação registrada
quentorm validate:meu_validador valor

# Validar com configurações
quentorm validate:meu_validador valor --config=config.json

# Validar em lote
quentorm validate:batch arquivo.txt --validator=meu_validador
```

#### Gerenciar Validações
```bash
# Listar validadores registrados
quentorm validator:list

# Mostrar detalhes de um validador
quentorm validator:show NomeDoValidador

# Remover validador
quentorm validator:remove NomeDoValidador
```

### Exemplos de Uso

#### 1. Criando um Validador de Telefone
```bash
# Criar validador
quentorm make:validator TelefoneValidator

# Registrar para uso
quentorm validator:register TelefoneValidator --alias=telefone

# Usar validação
quentorm validate:telefone "(11) 99999-9999"
```

#### 2. Validação de CEP
```bash
# Criar validador com configurações
quentorm make:validator CEPValidator --config

# Registrar com configurações
quentorm validator:register CEPValidator --config=cep_config.json

# Validar CEP
quentorm validate:cep "12345-678"
```

#### 3. Validação em Lote
```bash
# Criar arquivo com dados
echo "12345-678" > ceps.txt
echo "98765-432" >> ceps.txt

# Validar em lote
quentorm validate:batch ceps.txt --validator=cep
```

### Boas Práticas

1. **Organização**:
   - Mantenha validadores em `app/validators/`
   - Use nomes descritivos
   - Documente as regras

2. **Configuração**:
   - Use arquivos de configuração
   - Permita personalização
   - Mantenha padrões

3. **Testes**:
   - Crie testes unitários
   - Teste casos de erro
   - Valide em lote

4. **Documentação**:
   - Documente uso no CLI
   - Inclua exemplos
   - Mantenha atualizado

## Exemplos de Uso

### 1. Criando um Novo Projeto
```bash
# Criar projeto
quentorm new financeiro

# Entrar no diretório
cd financeiro

# Instalar dependências
pip install -r requirements.txt

# Configurar .env
cp .env.example .env
```

### 2. Criando Modelos e Migrações
```bash
# Criar modelo User com migração
quentorm make:model User --migration

# Criar modelo Cliente com todos os recursos
quentorm make:model Cliente --resource

# Gerar modelos a partir do banco
quentorm model:generate --connection=mysql
```

### 3. Gerenciando Migrações
```bash
# Criar migração
quentorm make:migration create_users_table

# Executar migrações
quentorm migrate

# Executar migrações com seeders
quentorm migrate --seed

# Reverter última migração
quentorm migrate:rollback
```

### 4. Populando Banco de Dados
```bash
# Criar seeder
quentorm make:seeder UserSeeder

# Executar seeder específico
quentorm db:seed --class=UserSeeder

# Executar todos os seeders
quentorm db:seed
```

### 5. Desenvolvimento Local
```bash
# Criar banco de desenvolvimento
quentorm db:create --database=dev_db

# Popular com dados de teste
quentorm db:seed

# Limpar após testes
quentorm db:wipe
```

### 6. Produção
```bash
# Criar backup diário
quentorm db:backup --name=daily_$(date +%Y%m%d)

# Otimizar periodicamente
quentorm db:optimize --analyze

# Monitorar status
quentorm db:status --connections
```

### 7. Manutenção
```bash
# Backup antes de atualização
quentorm db:backup --name=pre_update

# Restaurar se necessário
quentorm db:restore pre_update.sql

# Otimizar após atualização
quentorm db:optimize
```

## Boas Práticas

1. **Versionamento**:
   - Sempre versionar migrações
   - Manter seeders atualizados
   - Documentar alterações no banco

2. **Segurança**:
   - Não versionar arquivos .env
   - Usar variáveis de ambiente
   - Manter chaves seguras

3. **Desenvolvimento**:
   - Usar branches para features
   - Testar migrações localmente
   - Manter backup do banco

4. **Produção**:
   - Fazer backup antes de migrar
   - Testar em ambiente de staging
   - Manter logs de operações 