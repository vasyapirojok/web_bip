import uvicorn
from fastapi import FastAPI, Form
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, Response, JSONResponse
import hashlib
from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi_csrf_protect import CsrfProtect
from fastapi_csrf_protect.exceptions import CsrfProtectError
from pydantic import BaseModel
import ast
from site_parser import parse_page
from handle_shop_resp import handle_shop_resp
import requests
import random
from http import HTTPStatus
import json
from ration import *
from db import DB
import re

validate_email_reg = r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'


app = FastAPI()
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=['*'],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
templates = Jinja2Templates(directory="pages")
database = DB()


class CsrfSettings(BaseModel):
  secret_key: str = "asecrettoeverybody"
  cookie_samesite: str = "strict"

@CsrfProtect.load_config
def get_csrf_config():
  return CsrfSettings()

def set_cookie(token, response) -> Response:
    
    response.set_cookie(
        key="access_token", 
        value=token,
        httponly=True
    )
    return response

def set_base_cookie(email, response) -> Response:
    
    response.set_cookie(
        key="email", 
        value=email,
        httponly=True
    )
    return response


def check_cookie(token):
    if token is None:
        return False
    headers = { "Authorization": "Bearer " + token}
    resp = requests.get(url='http://127.0.0.1:8002/users/me', headers=headers)
    return resp.status_code == HTTPStatus.OK


@app.get("/signup")
async def signup(request: Request, csrf_protect: CsrfProtect = Depends()):
    csrf_token = csrf_protect.generate_csrf()
    response = templates.TemplateResponse(
        "auth/signup.html", {"request": request, "csrf_token": csrf_token}
    )
    
    csrf_protect.set_csrf_cookie(csrf_token, response)
    
    return response


@app.get("/login")
async def login(request: Request, csrf_protect: CsrfProtect = Depends()):
    if 'access_token' in list(request.cookies.keys()) and check_cookie(request.cookies['access_token']):    
        return FileResponse('pages/list_of_shops.html', headers={
        "Content-Security-Policy": "frame-ancestors",
        "X-Content-Type-Options": "nosniff"
    })
    csrf_token = csrf_protect.generate_csrf()
    response = templates.TemplateResponse(
        "auth/login.html", {"request": request, "csrf_token": csrf_token}
    )
    csrf_protect.set_csrf_cookie(csrf_token, response)
    return FileResponse("pages/auth/login.html", headers={
        "Content-Security-Policy": "frame-ancestors",
        "X-Content-Type-Options": "nosniff",
        "X-CSRF-Token": "aaaaa"
    })


@app.get("/")
async def root(response: FileResponse, request: Request):
    return FileResponse("pages/index.html")


@app.post("/login_form")
async def login_form(request: Request, csrf_protect: CsrfProtect = Depends(), email=Form(default=None), password=Form(default=None)):
    if re.match(validate_email_reg, email) is None:
        return JSONResponse(content='Incorrect email', headers={
        "Content-Security-Policy": "frame-ancestors",
        "X-Content-Type-Options": "nosniff"
    })
    resp = requests.get(url=f'http://127.0.0.1:8002/login_salt?email={email}')
    available = resp.json().get('available')
    salt = resp.json().get('salt')
    if not available:
        return JSONResponse(content='Wrong email'
    )
    h = hashlib.new('sha256')
    h.update(str(password + salt).encode())
    hash_passwd = h.hexdigest()
    resp = requests.post(url=f'http://127.0.0.1:8002/login_creds?email={email}&password={hash_passwd}')
    if ast.literal_eval(resp.text)['status'] != 'OK':
        return JSONResponse(content='Invalid credentials')
    if resp.json().get('status') != 'OK':
        return JSONResponse(content='Invalid credentials')
    csrf_token = csrf_protect.generate_csrf()
    response = templates.TemplateResponse(
        "auth/login_submit.html", {"request": request, "csrf_token": csrf_token},
        headers={
        "Content-Security-Policy": "frame-ancestors",
        "X-Content-Type-Options": "nosniff",
        "X-CSRF-Token": "aaaaa"
    }
    )
    # response = FileResponse("pages/auth/login_submit.html")
    response = set_base_cookie(email=email, response=response)
    
    csrf_protect.set_csrf_cookie(csrf_token, response)
    resp = requests.post(url=f'http://127.0.0.1:8002/set_csrf?email={email}&csrf={csrf_token}')
    # response = FileResponse("pages/auth/login_submit.html")
    # response = set_base_cookie(email=email, response=response)
    
    return response


@app.post("/signup_form")
async def signup_form(request: Request, csrf_protect: CsrfProtect = Depends(), email=Form(default=None), password=Form(default=None)):
    
    # csrf = request.cookies["fastapi-csrf-token"]
    # resp = requests.post(url=f'http://127.0.0.1:8002/check_csrf?email={email}&csrf={csrf}')
    # if resp.json().get('status') != 'OK':
    #     return 'Wrong csrf'
    if re.match(validate_email_reg, email) is None:
        return 'Incorrect email'
    resp = requests.get(url=f'http://127.0.0.1:8002/signup_salt?email={email}')
    available = resp.json().get('available')
    salt = resp.json().get('salt')
    if not available:
        return 'Email is already used'
    h = hashlib.new('sha256')
    h.update(str(password + salt).encode())
    hash_passwd = h.hexdigest()
    resp = requests.post(url=f'http://127.0.0.1:8002/signup_creds?email={email}&password={hash_passwd}')
    csrf_token = csrf_protect.generate_csrf()
    
    response = templates.TemplateResponse(
        "auth/login_submit.html", {"request": request, "csrf_token": csrf_token},
        headers={"X-CSRF-Token": "AAAA"}
    )
    # response = FileResponse("pages/auth/login_submit.html")
    response = set_base_cookie(email=email, response=response)
    
    csrf_protect.set_csrf_cookie(csrf_token, response)
    resp = requests.post(url=f'http://127.0.0.1:8002/set_csrf?email={email}&csrf={csrf_token}')
    return response


@app.post("/login_submit_form")
async def login_form(request: Request, response: FileResponse, auth_code=Form(default=None), csrf_protect: CsrfProtect = Depends()):
    
    email = request.cookies["email"]
    csrf = request.cookies["fastapi-csrf-token"]
    resp = requests.post(url=f'http://127.0.0.1:8002/check_csrf?email={email}&csrf={csrf}')
    resp_text = resp.text
    resp = ast.literal_eval(resp_text)
    status = resp['status']
    if status != "OK":
        return JSONResponse(content={"status": status, "msg": 'invalid csrf'})
    
    resp = requests.post(url=f'http://127.0.0.1:8002/check_code?email={email}&code={auth_code}')
    if resp.json().get('status') != 'OK':
        return 'Wrong code'
    
    a = requests.post(url=f'http://127.0.0.1:8002/token?email={email}')
    token = ast.literal_eval(a.content.decode('utf-8'))["access_token"]
    csrf_token = csrf_protect.generate_csrf()
    
    response = templates.TemplateResponse(
        "list_of_shops.html", {"request": request, "csrf_token": csrf_token},
        headers={"X-CSRF-Token": "AAAA"}
    )
    
    
    # response = FileResponse('pages/list_of_shops.html')
    response = set_cookie(token, response)
    csrf_protect.set_csrf_cookie(csrf_token, response)
    resp = requests.post(url=f'http://127.0.0.1:8002/set_csrf?email={email}&csrf={csrf_token}')
    return response


@app.get("/shop_info")
async def shop_info(request: Request,full_price:str, days_number:str, shops_list:str ):
    
    try:
        full_price = int(full_price)
        days_number = int(days_number)
    except:
        pass
    # shops_list = request['shops_list'].split(',')
    shops_list = shops_list.split(',')
    # products = database.get_products(shops_list)
    print(shops_list)
    page_number = 1
    products, count = database.get_page(shops_list, page_number)
    pages_number = (count//10) + 1
    result_html = handle_shop_resp(products, page_number, pages_number)
    handled_shops_list = str(shops_list).replace('"', "'")
    print(handled_shops_list)
    print('before_replace')
    result_html = result_html.replace('<input type=hidden id="shops_list" name="shops_list_name" value=""/>', f'<input type=hidden id="shops_list" name="shops_list_name" value="{handled_shops_list}"/>')
    print('after_replace')
    # print('<script type="text/javascript">' in result_html)
    with open('./pages/result.html', 'wb') as fd:
        fd.write(result_html.encode('utf-8'))
    return FileResponse('./pages/result.html')

    # products = {'offer': []}
    # for shop in shops_list:
    #     prs = parse_page(city = 'sankt-peterburg', shop= shop, page_num= 1)
        
    #     products["offer"] += prs["offer"]
    with open('./pages/result_shop_info.html', 'wb') as fd:
        fd.write(handle_shop_resp(products, []).encode('utf-8'))
    return FileResponse('./pages/result_shop_info.html')

@app.post("/get_ration")
# async def get_ration(request: Request, list_of_shops=Form(default=None), days_number=Form(default=None), total_money=Form(default=None)):
async def get_ration(request: Request):
    
    request_body = await request.body()
    request = ast.literal_eval(request_body.decode('utf-8'))
    full_price = int(request['full_price'])
    days_number = int(request['days_number'])
    shops_list = request['shops_list'].split(',')
    
    # full_price = 4000
    # days_number = 7
    # shops_list = ['5ka', 'dixy', 'verno', '7shagoff']
    # products = {'offer': []}
    # for shop in shops_list:
    #     prs = parse_page(city = 'sankt-peterburg', shop= shop, page_num= 1)
        
    #     products["offer"] += prs["offer"]
    products = database.get_products(shops_list)
    ration, products_to_buy, money_leftover = magic_ext(products=products, full_price=full_price, days_number=days_number)
    
    if ration is None or money_leftover is None:
        return JSONResponse(content={"products": {}, "ration": []})
    ration_lines = []
    
    for day_number in range(1, days_number + 1):
        breakfast = f'Day {day_number}\n\nBreakfast: \n'
        for elem in ration["breakfast"][day_number-1]:
            breakfast += elem + '\n'
        breakfast += '\n'
        lunch =  f'Lunch: \n'
        for elem in ration["lunch"][day_number-1]:
            lunch +=  f'{elem}\n'
        lunch += '\n'
        dinner =  f'Dinner: \n'
        for elem in ration["dinner"][day_number-1]:
            dinner +=  f'{elem}\n'
        dinner += '\n'
        ration_lines.append(breakfast + lunch + dinner)
    ration_lines.append(f'money leftover: {money_leftover}')
    # with open('example.json', 'wb') as fd:
    #     fd.write(str(products_to_buy).encode('utf-8'))
    with open('./pages/result.html', 'wb') as fd:
        fd.write(handle_shop_resp(products_to_buy,1, 1, ration_lines).encode('utf-8'))
    return FileResponse('./pages/result.html')


@app.get('/get_page')
async def get_page(request: Request, page_number: str, shops_list:str):
    print(shops_list)
    page_number = int(page_number)
    products, count = database.get_page(shops_list, page_number)
    pages_number = (count//10) + 1
    result_html = handle_shop_resp(products, page_number, pages_number)
    handled_shops_list = str(shops_list).replace('"', "'")
    print(handled_shops_list)
    print('before_replace')
    result_html = result_html.replace('<input type=hidden id="shops_list" name="shops_list_name" value=""/>', f'<input type=hidden id="shops_list" name="shops_list_name" value="{handled_shops_list}"/>')
    print('after_replace')
    # print('<script type="text/javascript">' in result_html)
    with open('./pages/result.html', 'wb') as fd:
        fd.write(result_html.encode('utf-8'))
    return FileResponse('./pages/result.html')

####### MOBILE APP #######
@app.post("/login_salt_app")
async def login_salt(request: Request):
    request_body = await request.body()
    request = ast.literal_eval(request_body.decode('utf-8'))
    email = request['email']
    resp = requests.get(url=f'http://127.0.0.1:8002/login_salt?email={email}')

    resp = ast.literal_eval(resp.text)
    # resp_body = await resp.body()
    # resp = ast.literal_eval(resp_body.decode('utf-8'))
    available = resp['available']
    salt = resp['salt']
    if not available:
        return JSONResponse(content={"salt": salt, "available": 0})
    return JSONResponse(content={"salt": salt, "available": 1})

@app.post("/signup_salt_app")
async def signup_salt(request: Request):
    request_body = await request.body()
    request = ast.literal_eval(request_body.decode('utf-8'))
    email = request['email']
    resp = requests.get(url=f'http://127.0.0.1:8002/signup_salt?email={email}')

    resp = ast.literal_eval(resp.text)
    # resp_body = await resp.body()
    # resp = ast.literal_eval(resp_body.decode('utf-8'))
    available = resp['available']
    salt = resp['salt']
    if not available:
        return JSONResponse(content={"salt": salt, "available": 0})
    return JSONResponse(content={"salt": salt, "available": 1})

@app.post("/signup_creds_app")
async def signup_creds_app(request: Request):
    request_body = await request.body()
    request = ast.literal_eval(request_body.decode('utf-8'))
    email = request['email']
    hash_passwd = request['hash_password']
    resp = requests.post(url=f'http://127.0.0.1:8002/signup_creds?email={email}&password={hash_passwd}')
    
    response = JSONResponse(content={"Status": "OK"})
    response = set_base_cookie(email=email, response=response)
    return response

@app.post("/check_code_app")
async def check_code_app(request: Request):
    request_body = await request.body()
    request = ast.literal_eval(request_body.decode('utf-8'))
    code = request['code']
    email = request['email']
    resp = requests.post(url=f'http://127.0.0.1:8002/check_code?email={email}&code={code}')
    resp = ast.literal_eval(resp.text)
    # resp = ast.literal_eval(resp_body.decode('utf-8'))
    status = resp['status']
    if status != "OK":
        return JSONResponse(content={"status": status, "token": ''})    
    a = requests.post(url=f'http://127.0.0.1:8002/token?email={email}')
    token = ast.literal_eval(a.content.decode('utf-8'))["access_token"]
    return JSONResponse(content={"status": status, "token": token})

@app.post("/login_creds_app")
async def login_creds_app(request: Request):
    request_body = await request.body()
    request = ast.literal_eval(request_body.decode('utf-8'))
    email = request['email']
    hash_passwd = request['hash_password']
    resp = requests.post(url=f'http://127.0.0.1:8002/login_creds?email={email}&password={hash_passwd}')
    resp_body = ast.literal_eval(resp.text)
    # resp = ast.literal_eval(resp_body.decode('utf-8'))
    status = resp_body['status']
    return JSONResponse(content={"status": status})


@app.post("/get_ration_app")
async def get_ration_app(request: Request):
    
    request_body = await request.body()
    request = ast.literal_eval(request_body.decode('utf-8'))
    full_price = request['full_price']
    days_number = request['days_number']
    shops_list = request['shops_list']
    # full_price = 2500
    # days_number = 7
    # shops_list = ['5ka', 'dixy', 'verno', '7shagoff']
    products = {'offer': []}
    for shop in shops_list:
        prs = parse_page(city = 'sankt-peterburg', shop= shop, page_num= 1)
        products["offer"] += prs["offer"]
    ration, products_to_buy, money_leftover = magic_ext(products=products['offer'], full_price=full_price, days_number=days_number)
    if ration is None or money_leftover is None:
        return JSONResponse(content={"products": {}, "ration": []})
    ration_lines = []
    
    for day_number in range(1, days_number + 1):
        breakfast = f'Day {day_number}\n\nBreakfast: \n'
        for elem in ration["breakfast"][day_number-1]:
            breakfast += elem + '\n'
        breakfast += '\n'
        lunch =  f'Lunch: \n'
        for elem in ration["lunch"][day_number-1]:
            lunch +=  f'{elem}\n'
        lunch += '\n'
        dinner =  f'Dinner: \n'
        for elem in ration["dinner"][day_number-1]:
            dinner +=  f'{elem}\n'
        dinner += '\n'
        ration_lines.append(breakfast + lunch + dinner)
    ration_lines.append(f'money leftover: {money_leftover}')
    # with open('example.json', 'wb') as fd:
    #     fd.write(str(products_to_buy).encode('utf-8'))
    
    return JSONResponse(content={"products": products_to_buy, "ration": ration_lines})

@app.post('/get_page_app')
async def get_page_app(request: Request):
    request_body = await request.body()
    request = ast.literal_eval(request_body.decode('utf-8'))
    
    shops_list = request['shops_list']
    page_number = request['page_number']
    products, count = database.get_page(shops_list, page_number)
    pages_number = (count//10) + 1
    products = {'offer': []}
    for shop in shops_list:
        prs = parse_page(city = 'sankt-peterburg', shop= shop, page_num= 1)
        products["offer"] += prs["offer"]
    
    return JSONResponse(content=products)

@app.exception_handler(CsrfProtectError)
def csrf_protect_exception_handler(request: Request, exc: CsrfProtectError):
  return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})




if __name__ == '__main__':
    # uvicorn.run(app, port=443, host='0.0.0.0', ssl_keyfile="key.pem", ssl_certfile="cert.pem")
    uvicorn.run(app, host='0.0.0.0', port=8001)

# fastapi-csrf-token
# @app.post("/get_csrf_token")
# async def get_csrf_token(request: Request, response: FileResponse, csrf_protect: CsrfProtect = Depends()):
#     csrf_token = csrf_protect.generate_csrf()
#     # response = Response(headers={"Set-Cookie": f'fastapi-csrf-token={csrf_token}'})
#     response = templates.TemplateResponse(
#         "auth/login_submit.html", {"request": request, "csrf_token": csrf_token}
#     )
#     response = FileResponse("pages/auth/login_submit.html")
#     csrf_protect.set_csrf_cookie(csrf_token, response)
#     return response

# @app.get("/csrftoken/")
# async def get_csrf_token(csrf_protect:CsrfProtect = Depends()):
# 	response = JSONResponse(status_code=200, content={'csrf_token':'cookie'})
# 	csrf_protect.set_csrf_cookie(response)
# 	return response