from fastapi import FastAPI, Depends
from routers import user_login, voting_for_president, voting_for_vice_president, student
from database import models
from database.database import engine
from fastapi import Request
from fastapi.templating import Jinja2Templates
from database.database import get_db
from sqlalchemy.orm import Session
import asyncio
from fastapi import WebSocket
import datetime
app = FastAPI()
app.include_router(student.router)

app.include_router(voting_for_president.router)
app.include_router(voting_for_vice_president.router)

app.include_router(user_login.router)

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")


@app.on_event("startup")
def startup():
    with open('logs.txt', 'a') as file:
        file.write(f'\nApp opened at {datetime.datetime.now()}')


@app.on_event("shutdown")
async def startup():
    with open('logs.txt', 'a') as file:
        file.write(f'\nApp Closed at {datetime.datetime.now()}')



async def realtime_vote_updates(db: Session = Depends(get_db)):
    await asyncio.sleep(3)

    query = db.query(models.President.id,models.President.name, models.President.total_votes).order_by(models.President.total_votes.desc()).all()

    db.commit()
    result = {}
    for i in query:
        result[i[0]] = {'name': i[1]}, {'total_votes': i[2]}
    print(result)

    return result


async def realtime_vote_updates_vice_president(db: Session = Depends(get_db)):
    await asyncio.sleep(3)

    query = db.query(models.VicePresident.id, models.VicePresident.name, models.VicePresident.total_votes).order_by(models.VicePresident.total_votes.desc()).all()

    db.commit()
    result = {}
    for i in query:
        result[i[0]] = {'name': i[1]}, {'total_votes': i[2]}
    print(result)

    return result


@app.get("/realtime_president_voting")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, db: Session = Depends(get_db)):
    await websocket.accept()
    try:
        while True:
            await asyncio.sleep(1)
            query = await realtime_vote_updates(db)

            await websocket.send_json(query)
    except:
        print('disconnected')


@app.get("/realtime_vicepresident_voting")
def read_root(request: Request):
    return templates.TemplateResponse("index2.html", {"request": request})


@app.websocket("/ws2")
async def websocket_endpoint(websocket: WebSocket, db: Session = Depends(get_db)):
    await websocket.accept()
    try:
        while True:
            await asyncio.sleep(1)
            query = await realtime_vote_updates_vice_president(db)

            await websocket.send_json(query)
    except:
        print('disconnected')


