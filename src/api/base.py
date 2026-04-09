from fastapi import APIRouter, Request, Depends, HTTPException, Form, status, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse

from src.dao.orders_dao import OrderDao
from src.dao.product_dao import ProductDao
from src.dependencies import get_db, user_validate
from src.dao.user_dao import UserDao
from src.services.secrets import create_hash, verify_hash
from src.schemas import OrderResponse, Product, RegisterRequest, Register_DB, UserRoles, UserValidateData
from src.services.login_serrvice import authorize
from src.config import config

base_router = APIRouter()

templates = Jinja2Templates(directory='templates')


@base_router.get("/", response_class=HTMLResponse)
async def home_page_get(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="home.html"
    )

@base_router.get("/register", response_class=HTMLResponse)
async def register_get(
    request: Request,
):
    return templates.TemplateResponse(
        request=request,
        name="register.html",
        # context=""
    )


@base_router.post("/register", status_code=201, response_class=RedirectResponse)
async def register_post(
    # request: Request,
    username = Form(...),
    user_email = Form(...),
    user_phone = Form(...),
    user_fio = Form(...),
    user_password = Form(...),
    
    db = Depends(get_db),
):
    role = UserRoles.USER
    if username == config.ADMIN_USERNAME and user_password == config.ADMIN_PASSWORD:
        role = UserRoles.ADMIN
        
    try:
        dao = UserDao(session=db)
        password_hash = create_hash(user_password)
        create_user_data = Register_DB(
            username=username,
            email=user_email,
            password_hash=password_hash,
            fio=user_fio,
            role=role,
            phone_number=user_phone,
        )
        
        await dao.register_user(user_data=create_user_data)
        
        # return {"ok": True, "messege": "New user was succsesfully created"}
        return RedirectResponse("/login", status_code=status.HTTP_303_SEE_OTHER)
    
    except Exception as e:
        print(f"Ошибка при регистрации: {e}")
        raise HTTPException(500, "Internal server error")








@base_router.get("/login", response_class=HTMLResponse)
async def login_get(
    request: Request,
):
    return templates.TemplateResponse(
        request=request,
        name="auth.html",
        # context=""
    )

@base_router.post("/login")
async def login_post(
    request: Request,
    
    username = Form(...),
    password = Form(...),
    
    db = Depends(get_db),
):
    try:
        user_id = await authorize(db, username, password)
        
        response = RedirectResponse(
            "/orders/new/create",
            status_code=status.HTTP_303_SEE_OTHER
        )
        
        request.session["user_id"] = user_id
        request.session["role"] = UserRoles.USER
        
        return response
    
    except HTTPException as e:
        raise e
    
    except Exception as e:
        print(f'Ошибка при авторизации: {e}')
        raise HTTPException(500, "Internal server error")






@base_router.get("/orders/new/create", response_class=HTMLResponse)
async def create_orders_get(
    request: Request,
  
    user_data: UserValidateData = Depends(user_validate),
    db = Depends(get_db) , 
): 
    
    try:
        dao = ProductDao(db)
        products = await dao.get_products()
        products = [Product(
            id=p.id,
            name=p.name,
            price=p.price
        ) for p in products]
    except Exception as e:
        print(f'Ошибка при показе товаров: {e}')
        raise HTTPException(500, "Internal server error")
        

    return templates.TemplateResponse(
        request=request,
        name="create_orders.html",
        context={"products": products}
    )


@base_router.post("/orders/new/create", response_class=RedirectResponse)
async def create_order_post(
    request: Request,
    
    selected_item = Form(...),
    quantity = Form(...),
    address = Form(...),
    
    user_data: UserValidateData = Depends(user_validate),
    db = Depends(get_db),
):
    
    try:
        dao = OrderDao(db)
        new_order = await dao.create_order(user_id=user_data.user_id, product_id=selected_item, quantity=quantity, address=address)
        
        return RedirectResponse(
            "/orders/new/create",
            status_code=status.HTTP_303_SEE_OTHER
        )
    except Exception as e:
        print(f"Ошибка при создании заказа: {e}")
        raise HTTPException(500, "Internal server error")



@base_router.get("/orders", response_class=HTMLResponse)
async def user_orders_get(
    requst: Request,
    
    user_data: UserValidateData = Depends(user_validate),
    db = Depends(get_db)
):

        
    dao = OrderDao(db)
    orders = await dao.get_user_orders(user_data.user_id)
    context = [OrderResponse(
        product_name=order.product.name,
        quantity=order.quantity,
        address=order.delivery_address,
        status=order.status,
        created_at=order.created_at
    ) for order in orders]
    
    
    return templates.TemplateResponse(
        request=requst,
        name="orders.html",
        context={"orders": context}
    )


@base_router.get("/admin", response_class=HTMLResponse)
async def admin_login_get(
    request: Request,
    
    db = Depends(get_db),
    user_data = Depends(user_validate)
):
    pass





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