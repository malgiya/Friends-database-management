from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
import os
import logging

# Environment variables and configuration
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:root@localhost/frndsdb")
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)  # Example of connection pooling
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

Base = declarative_base()

class Friend(Base):
    __tablename__ = 'friends'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    dob = Column(Date)
    category = Column(String(20))

Base.metadata.create_all(bind=engine)

class FriendCreate(BaseModel):
    name: str
    dob: str
    category: str

def manage_friend(db: Session, name: str, dob: str, category: str, action: str):
    try:
        if action == "create":
            friend = db.query(Friend).filter(Friend.name == name).first()
            if friend:
                raise HTTPException(status_code=400, detail="Friend with this name already exists.")
            new_friend = Friend(name=name, dob=dob, category=category)
            db.add(new_friend)
            db.commit()
            db.refresh(new_friend)
            return new_friend
        elif action == "update":
            friend = db.query(Friend).filter(Friend.name == name).first()
            if not friend:
                raise HTTPException(status_code=404, detail="Friend not found.")
            friend.dob = dob
            friend.category = category
            db.commit()
            db.refresh(friend)
            return friend
        elif action == "delete":
            friend = db.query(Friend).filter(Friend.name == name).first()
            if not friend:
                raise HTTPException(status_code=404, detail="Friend not found.")
            db.delete(friend)
            db.commit()
            return {"message": "Friend deleted successfully"}
        else:
            raise HTTPException(status_code=400, detail="Invalid action. Choose 'create', 'update', or 'delete'.")
    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/process-friend", response_class=HTMLResponse)
async def process_friend(
    request: Request,
    name: str = Form(...),
    dob: str = Form(...),
    category: str = Form(...),
    action: str = Form(...)
):
    db = SessionLocal()
    try:
        result = manage_friend(db, name=name, dob=dob, category=category, action=action)
        context = {
            "request": request,
            "message": result.get('message') if isinstance(result, dict) else None,
            "name": getattr(result, 'name', None),
            "dob": getattr(result, 'dob', None),
            "category": getattr(result, 'category', None)
        }
    except HTTPException as e:
        return HTMLResponse(content=f"<h1>Error: {e.detail}</h1>", status_code=e.status_code)
    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
        return HTMLResponse(content=f"<h1>Internal Server Error: {str(e)}</h1>", status_code=500)
    finally:
        db.close()

    return templates.TemplateResponse("result.html", context)

@app.get("/view-all", response_class=HTMLResponse)
async def view_all(request: Request):
    db = SessionLocal()
    try:
        friends = db.query(Friend).all()
        context = {
            "request": request,
            "friends": friends
        }
    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
        return HTMLResponse(content=f"<h1>Internal Server Error: {str(e)}</h1>", status_code=500)
    finally:
        db.close()
    
    return templates.TemplateResponse("all_records.html", context)
