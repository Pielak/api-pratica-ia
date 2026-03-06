from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.models import TarefaDB, TarefaCreate, TarefaUpdate, Tarefa
from app import database

database.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="API de Tarefas", version="2.0")


@app.get("/tarefas", response_model=list[Tarefa])
def listar(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    return db.query(TarefaDB).offset(skip).limit(limit).all()


@app.get("/tarefas/{id}", response_model=Tarefa)
def buscar(id: int, db: Session = Depends(database.get_db)):
    tarefa = db.query(TarefaDB).filter(TarefaDB.id == id).first()
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return tarefa


@app.post("/tarefas", response_model=Tarefa, status_code=status.HTTP_201_CREATED)
def criar(tarefa: TarefaCreate, db: Session = Depends(database.get_db)):
    nova = TarefaDB(**tarefa.model_dump())
    db.add(nova)
    db.commit()
    db.refresh(nova)
    return nova


@app.put("/tarefas/{id}", response_model=Tarefa)
def atualizar(id: int, dados: TarefaUpdate, db: Session = Depends(database.get_db)):
    tarefa = db.query(TarefaDB).filter(TarefaDB.id == id).first()
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(tarefa, campo, valor)
    db.commit()
    db.refresh(tarefa)
    return tarefa
## teste de comentário

@app.delete("/tarefas/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar(id: int, db: Session = Depends(database.get_db)):
    tarefa = db.query(TarefaDB).filter(TarefaDB.id == id).first()
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    db.delete(tarefa)
    db.commit()
