from typing import List
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import TodoItem, Base  # Import Base from models
from app.db import SessionLocal, engine
from app.schemas import TodoCreate, TodoUpdate, TodoResponse

# Create all database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()  # Create a new session
    try:
        yield db
    finally:
        db.close()  # Close the session

@app.post("/todos/", response_model=TodoResponse)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    db_todo = TodoItem(
        title=todo.title,
        description=todo.description,
        completed=todo.completed
    )
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return TodoResponse.from_orm(db_todo)

@app.get("/todos/", response_model=List[TodoResponse])
def read_todos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    todos = db.query(TodoItem).offset(skip).limit(limit).all()
    return [TodoResponse.from_orm(todo) for todo in todos]

@app.get("/todos/{id}", response_model=TodoResponse)
def read_todo(id: int, db: Session = Depends(get_db)):
    todo = db.query(TodoItem).filter(TodoItem.id == id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return TodoResponse.from_orm(todo)

@app.put("/todos/{id}", response_model=TodoResponse)
def update_todo(id: int, todo: TodoUpdate, db: Session = Depends(get_db)):
    db_todo = db.query(TodoItem).filter(TodoItem.id == id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    db_todo.title = todo.title
    db_todo.description = todo.description
    db_todo.completed = todo.completed
    
    db.commit()
    db.refresh(db_todo)
    return TodoResponse.from_orm(db_todo)

@app.delete("/todos/{id}", response_model=TodoResponse)
def delete_todo(id: int, db: Session = Depends(get_db)):
    db_todo = db.query(TodoItem).filter(TodoItem.id == id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(db_todo)
    db.commit()
    return TodoResponse.from_orm(db_todo)
