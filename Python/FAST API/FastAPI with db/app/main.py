from fastapi import FastAPI
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel, OAuthFlowPassword, SecurityScheme
from fastapi.openapi.utils import get_openapi
import jwt
#import PyJWT
from app.routes import auth, create_user

app = FastAPI()

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(create_user.router, tags=["users"])

# Custom OpenAPI schema with security schemes
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Simple FastAPI APP",
        version="1.0.0",
        description="This is a simple FastAPI application.",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "OAuth2PasswordBearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    openapi_schema["security"] = [{"OAuth2PasswordBearer": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
