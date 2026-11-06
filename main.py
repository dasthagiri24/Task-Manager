from fastapi import FastAPI, Request, Depends, Form, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session
import database
import models
from database import get_db

app = FastAPI(title="Task Manager Application")

models.Base.metadata.create_all(bind=database.engine)

templates = Jinja2Templates(directory="templates")

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)
@app.get("/")
def home(request: Request, db: Session = Depends(get_db)):

    tasks = db.query(models.Task).order_by(
        models.Task.id.desc()
    ).all()

    total = db.query(models.Task).count()

    completed = db.query(models.Task).filter(
        models.Task.completed == True
    ).count()

    pending = total - completed

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "tasks": tasks,
            "total": total,
            "completed": completed,
            "pending": pending
        }
    )

@app.post("/add")
def add_task(
    title: str = Form(...),
    description: str = Form(""),
    db: Session = Depends(get_db)
):

    new_task = models.Task(
        title=title,
        description=description
    )

    db.add(new_task)
    db.commit()

    return RedirectResponse("/", status_code=303)

@app.post("/complete/{task_id}")
def complete_task(
    task_id: int,
    db: Session = Depends(get_db)
):

    task = db.query(models.Task).filter(
        models.Task.id == task_id
    ).first()

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    task.completed = not task.completed

    db.commit()

    return RedirectResponse("/", status_code=303)

@app.post("/edit/{task_id}")
def edit_task(
    task_id: int,
    title: str = Form(...),
    description: str = Form(""),
    db: Session = Depends(get_db)
):

    task = db.query(models.Task).filter(
        models.Task.id == task_id
    ).first()

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    task.title = title
    task.description = description

    db.commit()

    return RedirectResponse("/", status_code=303)

@app.post("/delete/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    task = db.query(models.Task).filter(
        models.Task.id == task_id
    ).first()

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    db.delete(task)
    db.commit()

    return RedirectResponse("/", status_code=303)