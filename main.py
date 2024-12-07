from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from app.config.database import create_db_and_tables
from app.routes.auth.main import router as auth_router
from app.routes.users.main import router as user_router
from app.routes.api.main import router as api_router
from app.config.config import APP_NAME, VERSION


app = FastAPI(
    title=APP_NAME,
    version=VERSION,
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# # ---- Do this for all of your routes ----
app.include_router(auth_router, prefix='/api/v1.0')
app.include_router(user_router, prefix='/api/v1.0')
app.include_router(api_router, prefix='/api/v1.0')
# # ----------------------------------------


# Redirect / -> Swagger-UI documentation
@app.get("/", include_in_schema=False)
def main_function():
    """
    # Redirect
    to documentation (`/docs/`).
    """
    return RedirectResponse(url="/docs/")


# # Swagger expects the auth-URL to be /token, but in our case it is /auth/token
# # So, we redirect /token -> /auth/token
@app.post("/token", include_in_schema=False)
def forward_to_login():
    """
    # Redirect
    to token-generation (`/auth/token`). Used to make Auth in Swagger-UI work.
    """
    return RedirectResponse(url="/api/v1/auth/token")
