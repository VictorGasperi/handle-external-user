from datetime import datetime, timezone
import secrets
from uuid import uuid4
import fastapi
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

from app.exchange_code import ExchangeCode
from app.mock import DynoSimulated

repo_codes = DynoSimulated()

app = fastapi.FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post('/start')
async def start(
    email: str = fastapi.Form(...),
    password: str = fastapi.Form(...),
):
    # Criar o user em auth
    # Criar o user em users
    # Criar o code e salvar em dyno
    # Redirecionar para uma pagina HTTP

    print({
        'email': email,
        'password': password
    })

    uid = str(uuid4())

    code = ExchangeCode(
        code = secrets.token_urlsafe(),
        uid = uid,
        expiresAt = int(datetime.now(timezone.utc).timestamp()) + 300,
        usedAt = None
    )
    
    print(code.to_dict())

    repo_codes.dyno.append(code)

    return RedirectResponse(
        url=f'http://localhost:8080/entry.html?code={code.code}',
        status_code=302
    )

@app.get('/auth/exchange')
def auth_exchange(exchangeable_code: str = fastapi.Query(..., description='Exchange code')):
    
    print(repo_codes.dyno)

    token = 'AQUI ESTA O TOKEN'

    for c in repo_codes.dyno:
        if exchangeable_code == c.code:
            if c.expiresAt < int(datetime.now(timezone.utc).timestamp()):
                raise fastapi.HTTPException(status_code=401, detail='Invalid code')
            
            if c.usedAt is not None:
                raise fastapi.HTTPException(status_code=401, detail='Invalid code')

            usedAt = int(datetime.now(timezone.utc).timestamp())

            c.usedAt = usedAt

            return {
                "token": token,
                "expiresAt": "NEVER!"
            }
        
    raise fastapi.HTTPException(status_code=401, detail='Invalid code')
            
