"""
Teste do QuentORM
"""
import logging
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

try:
    from quentorm import BaseModel, Column, String, Integer
except ImportError as e:
    print(f"Erro ao importar QuentORM: {e}")
    print("Verifique se o pacote está instalado corretamente.")
    sys.exit(1)

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestModel(BaseModel):
    """Modelo de teste"""
    __tablename__ = 'test_table'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50))

def main():
    """Função principal"""
    try:
        # Criar engine em memória para teste
        engine = create_engine('sqlite:///:memory:', echo=True)
        
        # Criar tabelas
        BaseModel.metadata.create_all(engine)
        
        # Criar sessão
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # Criar instância do modelo
        test = TestModel(name='Teste')
        session.add(test)
        session.commit()
        
        # Buscar instância
        result = session.query(TestModel).first()
        print(f"Modelo criado: {result.name}")
        
    except Exception as e:
        logger.error(f"Erro durante o teste: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 