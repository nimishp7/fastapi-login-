from fastapi import APIRouter, Request, Form, status, Depends
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login.exceptions import InvalidCredentialsException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from passlib.context import CryptContext
from .models import *
from fastapi_login import LoginManager

import typing
import passlib

SECRET = 'your-secret-key'

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
manager = LoginManager(SECRET, token_url='/login_user/')


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password(password):
    return pwd_context.hash(password)


def flash(request: Request, message: typing.Any, category: str = "") -> None:
    if "massages" not in request.session:
        request.session["-massages"] = []
    request.session["_massages"].append(
        {"message": message, "category": category})


def get_flashed_messages(request: Request):
    print(request.session)
    return request.session.pop("_messages") if "_message" in request.session else []
# templates.env.global['get_flashed_message'] = get_flashed_messagespip


@router.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
    })


@router.post("/registration/", response_class=HTMLResponse)
async def read_item(request: Request, name: str = Form(...),
                    email: str = Form(...),
                    phone: str = Form(...),
                    psw: str = Form(...)):
    if await User.filter(email=email).exists():
        flash(request, "Email already register")
        return RedirectResponse("/", status_code=status.HTTP_302_FOUND)

    elif await User.filter(phone=phone).exists():
        flash(request, "phone number already exists")
        return RedirectResponse("/", status_code=status.HTTP_302_FOUND)

    else:
        user_obj = await User.create(email=email, name=name, phone=phone,
                                     password=get_password(psw))
        return RedirectResponse("/login/", status_code=status.HTTP_302_FOUND)
        


@router.get("/login/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("login.html", {
        "request": request,
    })
    
@manager.user_loader()
def load_user(email: str):  # could also be an asynchronous function
    user = User.get(email)
    return user 

@router.post('/login_user/')
def login(data: OAuth2PasswordRequestForm = Depends()):
    email = email   
    password = password

    user = load_user(email)  # we are using the same function to retrieve the user
    if not user:
        raise InvalidCredentialsException  # you can also use your own HTTPException
    elif password != user['password']:
        raise InvalidCredentialsException
    
    access_token = manager.create_access_token(
        data=dict(sub=email)
    )
    return {'access_token': access_token, 'token_type': 'bearer'}