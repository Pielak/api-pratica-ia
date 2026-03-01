tarefas = []
contador_id = 1

def get_all():
    return tarefas

def get_by_id(id):
    for t in tarefas:
        if t["id"] == id:
            return t
    return None

def create(tarefa):
    global contador_id
    nova = tarefa.dict()
    nova["id"] = contador_id
    contador_id += 1
    tarefas.append(nova)
    return nova

def delete(id):
    global tarefas
    tarefas = [t for t in tarefas if t["id"] != id]
