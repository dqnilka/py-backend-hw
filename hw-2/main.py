from fastapi import FastAPI
import uvicorn
import sys
from prometheus_fastapi_instrumentator import Instrumentator

sys.path.append('../../../')

from app_cart import router_cart
from app_item import router_item

app = FastAPI(
    docs_url='/docs',
    openapi_url='/docs.json',
    title="Shop API",
)

app.include_router(router_cart)
app.include_router(router_item)

Instrumentator().instrument(app).expose(app)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
