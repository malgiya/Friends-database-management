from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel

app = FastAPI()
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:root@localhost/frndsdb"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
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
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
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
        if isinstance(result, dict):  
            message = result.get('message', 'Operation completed successfully')
            context = {
                "request": request,
                "message": message
            }
        else: 
            context = {
                "request": request,
                "name": result.name,
                "dob": result.dob,
                "category": result.category
            }
    except HTTPException as e:
        return HTMLResponse(content=f"<h1>Error: {e.detail}</h1>", status_code=e.status_code)
    except Exception as e:
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
        return HTMLResponse(content=f"<h1>Internal Server Error: {str(e)}</h1>", status_code=500)
    finally:
        db.close()
    
    return templates.TemplateResponse("all_records.html", context)
