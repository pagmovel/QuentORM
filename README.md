# QuentORM

QuentORM é um ORM (Object-Relational Mapping) moderno e intuitivo para Python, projetado para simplificar o desenvolvimento de aplicações financeiras.

## Características

- Validação robusta de dados
- Suporte a múltiplos bancos de dados
- Interface de linha de comando (CLI)
- Documentação completa e didática
- Sistema de mensagens internacionalizado

## Instalação

```bash
pip install quentorm
```

## Uso Básico

```python
from quentorm import Model, Field

class Cliente(Model):
    nome = Field(str)
    cpf = Field(str, validators=['cpf'])
    email = Field(str, validators=['email'])

# Criar um novo cliente
cliente = Cliente(nome="João Silva", cpf="12345678901", email="joao@exemplo.com")
cliente.save()
```

## Documentação

A documentação completa está disponível em:

- [Manual](docs/MANUAL.md)
- [CLI](docs/QUENTORM-CLI.md)
- [Validações](docs/VALIDACOES.md)
- [Casos de Uso](docs/CASO_DE_USO.md)

## Contribuição

Contribuições são bem-vindas! Por favor, leia nosso [guia de contribuição](CONTRIBUTING.md) para mais detalhes.

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 🙏 Agradecimentos

- [Laravel](https://laravel.com/) pelo Eloquent ORM
- [SQLAlchemy](https://www.sqlalchemy.org/) pela base de dados
- Todos os [contribuidores](CONTRIBUTORS.md) deste projeto 