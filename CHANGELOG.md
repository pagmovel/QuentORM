# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

## [0.1.0] - 2025-04-12 15:20

### Adicionado
- Suporte a múltiplas conexões de banco de dados (MySQL, PostgreSQL, SQLite)
- Suporte a múltiplos schemas no PostgreSQL
- Interface fluente para consultas
- Relacionamentos entre modelos
- Migrações de banco de dados
- Geração automática de modelos a partir do banco de dados
- Suporte a transações
- Interface similar ao Eloquent do Laravel

### Alterado
- Estrutura inicial do projeto
- Configuração de banco de dados para suportar múltiplas conexões
- Documentação atualizada

### Corrigido
- Problemas iniciais de configuração
- Bugs na geração de modelos

## [0.2.0] - Planejado

### Adicionado
- Sistema de eventos e observers
- Hooks para before/after save, create, update, delete
- Eventos personalizáveis
- Sistema de listeners

### Alterado
- Melhorias na performance das consultas
- Otimização do gerenciamento de conexões

## [0.3.0] - Planejado

### Adicionado
- Suporte a soft deletes
- Restauração de registros deletados
- Filtros automáticos para excluir registros deletados
- Métodos para forçar delete permanente

## [0.4.0] - Planejado

### Adicionado
- Sistema de cache integrado
- Cache de consultas frequentes
- Cache de relacionamentos
- Invalidação automática de cache

## [1.0.0] - Planejado

### Adicionado
- Suporte completo a todos os recursos do Eloquent
- Documentação completa
- Testes unitários e de integração
- Exemplos de uso em diferentes frameworks

### Alterado
- API estável e documentada
- Melhorias de performance
- Otimização de memória

### Corrigido
- Todos os bugs conhecidos
- Problemas de compatibilidade 