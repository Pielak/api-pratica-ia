from pydantic import BaseModel
from typing import Optional

class Tarefa(BaseModel):
    id: Optional[int] = None
    titulo: str
    descricao: str
    concluida: bool = False
