# API de Tarefas

API REST para gerenciamento de tarefas, construída com FastAPI e SQLite.

## Requisitos

- Python 3.10+

## Instalação

```bash
pip install -r requirements.txt
```

## Executando

```bash
uvicorn app.main:app --reload
```

A API estará disponível em `http://localhost:8000`.

Documentação interativa: `http://localhost:8000/docs`

## Endpoints

### Listar tarefas
```
GET /tarefas?skip=0&limit=10
```

### Buscar tarefa por ID
```
GET /tarefas/{id}
```

### Criar tarefa
```
POST /tarefas
Content-Type: application/json

{
  "titulo": "Estudar FastAPI",
  "descricao": "Ver a documentação oficial",
  "concluida": false
}
```

### Atualizar tarefa
```
PUT /tarefas/{id}
Content-Type: application/json

{
  "concluida": true
}
```

Todos os campos são opcionais — envie apenas o que deseja alterar.

### Deletar tarefa
```
DELETE /tarefas/{id}
```

## Testes

```bash
python3 -m pytest tests/ -v
```

## Estrutura do projeto

```
app/
├── main.py       # rotas
├── models.py     # modelos ORM e schemas Pydantic
└── database.py   # configuração do SQLAlchemy
tests/
└── test_api.py   # testes de integração
requirements.txt
```
