from fastapi import FastAPI
from omnibridge.api.protected_routes import router as protected_router
from omnibridge.api.auth_routes import router as auth_router
from omnibridge.accounts.routes import router as accounts_router
from omnibridge.api.sources import router as sources_router
from omnibridge.api.search import router as search_router


app = FastAPI()

app.include_router(auth_router)
app.include_router(protected_router)
app.include_router(accounts_router)
app.include_router(sources_router)
app.include_router(search_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
