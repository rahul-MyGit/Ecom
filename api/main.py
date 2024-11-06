from fastapi import FastAPI
from routers.user import USER_ROUTER 
from routers.auth import AUTH_ROUTER

app = FastAPI()

@app.get('/')
def check_status():
    return {'ok': True}

app.include_router(AUTH_ROUTER, prefix='/auth')
app.include_router(USER_ROUTER, prefix='/users')

if __name__ == '__main__': 
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)