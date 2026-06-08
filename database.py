from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

# 1. A String de Conexão (Onde a mágica do SQLite acontece)
# O "sqlite:///banco.db" diz para o Python criar um arquivo local chamado banco.db
engine = create_engine('sqlite:///banco.db', echo=True)

# 2. A Base Declarativa
Base = declarative_base()

# 3. A Classe que substitui a sua Tabela SQL
class Usuario(Base):
    __tablename__ = 'usuarios' # Nome da tabela no banco
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    senha_hash = Column(String(255), nullable=False)
    data_cadastro = Column(DateTime, default=datetime.utcnow)

# 4. O Comando que cria as tabelas fisicamente no arquivo .db
Base.metadata.create_all(engine)