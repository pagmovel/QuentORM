from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50))

if __name__ == '__main__':
    # Criar engine em memória para teste
    engine = create_engine('sqlite:///:memory:', echo=True)
    
    # Criar tabelas
    Base.metadata.create_all(engine)
    
    # Criar sessão
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Criar usuário
    user = User(name='Teste')
    session.add(user)
    session.commit()
    
    # Buscar usuário
    result = session.query(User).first()
    print(f"Usuário criado: {result.name}") 