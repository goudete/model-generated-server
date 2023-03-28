from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI()

class Todo(BaseModel):
    title: str
    description: str
    completed: bool

todos: Dict[int, Todo] = {}
todo_id_counter: int = 1

@app.post("/todos/", response_model=Todo)
async def create_todo(todo: Todo) -> Todo:
    global todo_id_counter
    todos[todo_id_counter] = todo
    todo_id_counter += 1
    return todo

@app.get("/todos/", response_model=List[Todo])
async def list_todos() -> List[Todo]:
    return list(todos.values())

@app.get("/todos/{todo_id}", response_model=Todo)
async def get_todo(todo_id: int) -> Todo:
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todos[todo_id]

@app.put("/todos/{todo_id}", response_model=Todo)
async def update_todo(todo_id: int, todo: Todo) -> Todo:
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")
    todos[todo_id] = todo
    return todo

@app.delete("/todos/{todo_id}", response_model=Todo)
async def delete_todo(todo_id: int) -> Todo:
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")
    deleted_todo = todos.pop(todo_id)
    return deleted_todo

if __name__ == "__main__":
    print('NAME: ', __name__)
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)