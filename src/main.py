import uvicorn
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from config import get_settings
from dependencies.db import get_db
from routers import api

app = FastAPI(
    openapi_url=f"{get_settings().api_str}/openapi.json",
    debug=get_settings().debug,
    docs_url="/api/docs",
)
app.include_router(api.api_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# if get_settings().debug:
#     app.add_middleware(
#         DebugToolbarMiddleware,
#         # panels=["debug_toolbar.panels.sqlalchemy.SQLAlchemyPanel"],
#     )


@app.get("/")
def handle(db: Session = Depends(get_db)) -> str:
    return "Hello world"


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
