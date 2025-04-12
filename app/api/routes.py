"""
Exemplo de API usando modelos importados.

Este módulo demonstra como usar os modelos base
em uma API REST.
"""

from flask import Flask, request, jsonify
from app.models.base import Cliente, ContaBancaria
from pyquent.utils.validators import validar_cpf, validar_agencia, validar_conta

app = Flask(__name__)

@app.route('/api/clientes', methods=['POST'])
def criar_cliente():
    """Cria um novo cliente."""
    dados = request.json
    
    # Validar CPF
    if not validar_cpf(dados['cpf']):
        return jsonify({
            "erro": "CPF inválido"
        }), 400
        
    # Criar cliente
    cliente = Cliente.create(
        nome=dados['nome'],
        cpf=dados['cpf'],
        email=dados['email'],
        telefone=dados['telefone']
    )
    
    # Salvar no banco
    cliente.save()
    
    return jsonify({
        "mensagem": "Cliente criado com sucesso",
        "cliente": cliente.to_dict()
    }), 201

@app.route('/api/clientes/<int:cliente_id>/contas', methods=['POST'])
def criar_conta(cliente_id):
    """Cria uma nova conta para o cliente."""
    dados = request.json
    
    # Validar dados bancários
    if not validar_agencia(dados['agencia']):
        return jsonify({
            "erro": "Agência inválida"
        }), 400
        
    if not validar_conta(dados['conta']):
        return jsonify({
            "erro": "Conta inválida"
        }), 400
        
    # Buscar cliente
    cliente = Cliente.find(cliente_id)
    if not cliente:
        return jsonify({
            "erro": "Cliente não encontrado"
        }), 404
        
    # Criar conta
    conta = ContaBancaria.create(
        agencia=dados['agencia'],
        conta=dados['conta'],
        digito=dados['digito'],
        cliente_id=cliente.id
    )
    
    # Salvar no banco
    conta.save()
    
    return jsonify({
        "mensagem": "Conta criada com sucesso",
        "conta": conta.to_dict()
    }), 201

@app.route('/api/clientes', methods=['GET'])
def listar_clientes():
    """Lista todos os clientes."""
    clientes = Cliente.all()
    
    return jsonify({
        "clientes": [cliente.to_dict() for cliente in clientes]
    })

@app.route('/api/clientes/<int:cliente_id>', methods=['GET'])
def buscar_cliente(cliente_id):
    """Busca um cliente específico."""
    cliente = Cliente.find(cliente_id)
    
    if not cliente:
        return jsonify({
            "erro": "Cliente não encontrado"
        }), 404
        
    return jsonify({
        "cliente": cliente.to_dict()
    })

@app.route('/api/clientes/<int:cliente_id>/contas', methods=['GET'])
def listar_contas_cliente(cliente_id):
    """Lista as contas de um cliente."""
    cliente = Cliente.find(cliente_id)
    
    if not cliente:
        return jsonify({
            "erro": "Cliente não encontrado"
        }), 404
        
    contas = ContaBancaria.where('cliente_id', cliente_id).get()
    
    return jsonify({
        "contas": [conta.to_dict() for conta in contas]
    }) 