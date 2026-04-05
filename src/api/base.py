from fastapi import APIRouter, Request, Depends, HTTPException, Form, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse

from src.dependencies import get_db
from src.dao.user_dao import UserDao
from src.services.secrets import create_hash
from src.schemas import RegisterRequest, Register_DB

base_router = APIRouter()

templates = Jinja2Templates(directory='templates')


@base_router.get("/register", response_class=HTMLResponse)
async def register_get(
    request: Request,
):
    return templates.TemplateResponse(
        request=request,
        name="register.html",
        # context=""
    )


@base_router.post("/register", status_code=201)
async def register_post(
    # request: Request,
    username = Form(...),
    user_email = Form(...),
    user_phone = Form(...),
    user_fio = Form(...),
    user_password = Form(...),
    
    db = Depends(get_db),
):
    try:
        user_data = RegisterRequest(
            username=username,
            email=user_email,
            phone_number=user_phone,
            fio=user_fio,
            password=user_password
        )
        dao = UserDao(session=db)
        password_hash = create_hash(user_data.password)
        create_user_data = Register_DB(
            username=user_data.username,
            email=user_data.email,
            password_hash=password_hash,
            fio=user_data.fio,
            phone_number=user_data.phone_number
        )
        
        await dao.register_user(user_data=create_user_data)
        
        # return {"ok": True, "messege": "New user was succsesfully created"}
        return RedirectResponse("/login", status_code=status.HTTP_303_SEE_OTHER)
    
    except Exception as e:
        print(f"Ошибка при регистрации: {e}")
        raise HTTPException(500, "Internal server error")


# @base_router.get("/login")
# async def login_get(
    
    
#     db: Depends(get_db)
# ):
    























@base_router.get("/test", tags=["TEST"])
async def test_handler(
    request: Request
):
    return {
        "method": request.method,
        "url": str(request.url),
        "path": request.url.path,
        "query_params": dict(request.query_params),
        "headers": dict(request.headers),
        "cookies": dict(request.cookies),
        "client": {
            "host": request.client.host if request.client else None,
            "port": request.client.port if request.client else None,
        },
        "path_params": dict(request.path_params),
        "scheme": request.scope.get("scheme"),
        "http_version": request.scope.get("http_version"),
    }