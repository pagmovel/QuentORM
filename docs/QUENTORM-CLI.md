# 🖥️ Interface de Linha de Comando do QuentORM

## 🎯 Introdução

A CLI (Interface de Linha de Comando) do QuentORM fornece ferramentas para facilitar o desenvolvimento com o ORM.

## 📋 Índice

1. [Comandos Básicos](#comandos-básicos)
2. [Modelos](#modelos)
3. [Migrações](#migrações)
4. [Validações](#validações)
5. [Boas Práticas](#boas-práticas)

## 💻 Comandos Básicos

### Ajuda
```bash
# Mostrar ajuda geral
quentorm --help

# Mostrar ajuda de um comando
quentorm make:model --help
```

### Configuração
```bash
# Inicializar configuração
quentorm init

# Configurar banco de dados
quentorm db:config

# Testar conexão
quentorm db:test
```

## 📦 Modelos

### Criar Modelo
```bash
# Criar modelo básico
quentorm make:model Usuario

# Criar modelo com migração
quentorm make:model Usuario --migration

# Criar modelo com todos os arquivos
quentorm make:model Usuario --all
```

### Gerar Código
```bash
# Gerar código do modelo
quentorm make:code Usuario

# Gerar validações
quentorm make:validators Usuario

# Gerar observers
quentorm make:observers Usuario
```

## 🔄 Migrações

### Criar Migração
```bash
# Criar migração
quentorm make:migration create_usuarios_table

# Criar migração de rollback
quentorm make:migration drop_usuarios_table --rollback
```

### Executar Migrações
```bash
# Executar migrações
quentorm migrate

# Rollback da última migração
quentorm migrate:rollback

# Rollback de todas as migrações
quentorm migrate:reset

# Refresh (rollback + migrate)
quentorm migrate:refresh
```

## ✅ Validações

### Validar Dados
```bash
# Validar CPF
quentorm validate:cpf 12345678901

# Validar CNPJ
quentorm validate:cnpj 12345678000190

# Validar em massa
quentorm validate:mass data.csv
```

### Gerar Validações
```bash
# Gerar validador de CPF
quentorm make:validator CPF

# Gerar validador de CNPJ
quentorm make:validator CNPJ

# Gerar validador personalizado
quentorm make:validator Custom --rules="required,min:3,max:255"
```

## 💡 Boas Práticas

### Desenvolvimento

- Use comandos para gerar código
- Mantenha migrações versionadas
- Documente modelos e validações
- Implemente testes

### Produção

- Faça backup antes de migrações
- Monitore execução de comandos
- Mantenha logs detalhados
- Implemente rollback seguro

### Segurança

- Valide inputs de comandos
- Use credenciais seguras
- Mantenha logs de acesso
- Implemente auditoria

### Performance

- Otimize consultas geradas
- Use índices apropriados
- Monitore tempo de execução
- Implemente cache quando possível 