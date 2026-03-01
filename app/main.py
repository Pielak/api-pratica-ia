from fastapi import FastAPI, HTTPException
from app.models import Tarefa
from app import database

app = FastAPI(title="API de Tarefas", version="1.0")

@app.get("/tarefas")
def listar():
    return database.get_all()

@app.get("/tarefas/{id}")
def buscar(id: int):
    tarefa = database.get_by_id(id)
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return tarefa

@app.post("/tarefas")
def criar(tarefa: Tarefa):
    return database.create(tarefa)

@app.delete("/tarefas/{id}")
def deletar(id: int):
    database.delete(id)
    return {"mensagem": "Tarefa deletada"}
