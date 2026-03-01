from sqlalchemy import Column, Integer, String, Boolean
from pydantic import BaseModel, ConfigDict
from typing import Optional
from app.database import Base


class TarefaDB(Base):
    __tablename__ = "tarefas"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    descricao = Column(String, nullable=False)
    concluida = Column(Boolean, default=False)


class TarefaCreate(BaseModel):
    titulo: str
    descricao: str
    concluida: bool = False


class TarefaUpdate(BaseModel):
    titulo: Optional[str] = None
    descricao: Optional[str] = None
    concluida: Optional[bool] = None


class Tarefa(TarefaCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
