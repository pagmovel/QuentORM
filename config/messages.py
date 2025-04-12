import json
import os
from typing import Dict, Any

class MessageConfig:
    """Configuração de mensagens do sistema."""
    
    def __init__(self, lang: str = 'pt_br'):
        """
        Inicializa a configuração de mensagens.
        
        Args:
            lang (str): Idioma padrão (pt_br, en, es)
        """
        self.lang = lang
        self.messages = self._load_messages()
    
    def _load_messages(self) -> Dict[str, Any]:
        """
        Carrega as mensagens do arquivo JSON correspondente ao idioma.
        
        Returns:
            Dict[str, Any]: Dicionário com as mensagens
        """
        messages_path = os.path.join(
            os.path.dirname(__file__),
            'messages',
            f'{self.lang}.json'
        )
        
        try:
            with open(messages_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise ValueError(f"Arquivo de mensagens não encontrado para o idioma: {self.lang}")
    
    def get(self, path: str, default: str = None) -> str:
        """
        Obtém uma mensagem específica usando um caminho.
        
        Args:
            path (str): Caminho da mensagem (ex: 'cli.new.welcome')
            default (str): Valor padrão caso a mensagem não seja encontrada
            
        Returns:
            str: Mensagem encontrada ou valor padrão
        """
        keys = path.split('.')
        current = self.messages
        
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return default
        
        return current
    
    def get_list(self, path: str) -> list:
        """
        Obtém uma lista de mensagens.
        
        Args:
            path (str): Caminho da lista de mensagens
            
        Returns:
            list: Lista de mensagens
        """
        result = self.get(path)
        return result if isinstance(result, list) else []
    
    def set_language(self, lang: str) -> None:
        """
        Altera o idioma das mensagens.
        
        Args:
            lang (str): Novo idioma
        """
        self.lang = lang
        self.messages = self._load_messages()

# Instância global para uso em todo o sistema
messages = MessageConfig() 