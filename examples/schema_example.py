from config.database import DatabaseManager
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import time

# Criando uma classe base para cada schema
BasePublic = declarative_base()
BaseSecondary = declarative_base()
BaseThird = declarative_base()

# Definindo modelos para cada schema
class UserPublic(BasePublic):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'public'}
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(100))

class UserSecondary(BaseSecondary):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'secondary'}
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(100))

class UserThird(BaseThird):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'third'}
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(100))

def bulk_insert_example():
    """Exemplo de inserção em massa"""
    db = DatabaseManager()
    
    # Criando engines para cada schema
    engine_public = db.get_engine('pgsql')
    engine_secondary = db.get_engine('pgsql_secondary')
    engine_third = db.get_engine('pgsql_third')
    
    # Criando sessões para cada schema
    SessionPublic = sessionmaker(bind=engine_public)
    SessionSecondary = sessionmaker(bind=engine_secondary)
    SessionThird = sessionmaker(bind=engine_third)
    
    session_public = SessionPublic()
    session_secondary = SessionSecondary()
    session_third = SessionThird()
    
    try:
        # Gerando dados para inserção em massa
        users_public = [
            UserPublic(name=f'Usuário Public {i}', email=f'user{i}@public.com')
            for i in range(1, 1001)
        ]
        
        users_secondary = [
            UserSecondary(name=f'Usuário Secondary {i}', email=f'user{i}@secondary.com')
            for i in range(1, 1001)
        ]
        
        users_third = [
            UserThird(name=f'Usuário Third {i}', email=f'user{i}@third.com')
            for i in range(1, 1001)
        ]
        
        # Medindo tempo de inserção em massa
        start_time = time.time()
        
        # Inserção em massa no schema public
        session_public.bulk_save_objects(users_public)
        session_public.commit()
        print(f"\nInserção em massa no schema public: {time.time() - start_time:.2f} segundos")
        
        # Inserção em massa no schema secondary
        start_time = time.time()
        session_secondary.bulk_save_objects(users_secondary)
        session_secondary.commit()
        print(f"Inserção em massa no schema secondary: {time.time() - start_time:.2f} segundos")
        
        # Inserção em massa no schema third
        start_time = time.time()
        session_third.bulk_save_objects(users_third)
        session_third.commit()
        print(f"Inserção em massa no schema third: {time.time() - start_time:.2f} segundos")
        
        # Verificando a quantidade de registros em cada schema
        count_public = session_public.query(UserPublic).count()
        count_secondary = session_secondary.query(UserSecondary).count()
        count_third = session_third.query(UserThird).count()
        
        print(f"\nTotal de registros no schema public: {count_public}")
        print(f"Total de registros no schema secondary: {count_secondary}")
        print(f"Total de registros no schema third: {count_third}")
        
    except Exception as e:
        print(f"Erro: {e}")
        session_public.rollback()
        session_secondary.rollback()
        session_third.rollback()
    finally:
        session_public.close()
        session_secondary.close()
        session_third.close()

def main():
    # Obtendo o gerenciador de banco de dados
    db = DatabaseManager()
    
    # Criando engines para cada schema
    engine_public = db.get_engine('pgsql')
    engine_secondary = db.get_engine('pgsql_secondary')
    engine_third = db.get_engine('pgsql_third')
    
    # Criando as tabelas em cada schema
    BasePublic.metadata.create_all(engine_public)
    BaseSecondary.metadata.create_all(engine_secondary)
    BaseThird.metadata.create_all(engine_third)
    
    # Executando o exemplo de inserção em massa
    bulk_insert_example()

if __name__ == '__main__':
    main() 