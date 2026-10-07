import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from authlib.integrations.starlette_client import OAuth
from starlette.requests import Request
from starlette.middleware.sessions import SessionMiddleware

load_dotenv()

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
SESSION_SECRET = os.getenv("SESSION_SECRET") or "dev-secret-key"

app = FastAPI(
    title="Google OAuth 2.0 Login Demo"
)

app.add_middleware(
    SessionMiddleware,
    secret_key=SESSION_SECRET,
    same_site="lax",
    https_only=False
)

oauth = OAuth()

oauth.register(
    name="google",
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url=(
        "https://accounts.google.com/"
        ".well-known/openid-configuration"
    ),

    client_kwargs={
        "scope": "openid email profile"
    }
)


@app.get("/")
def home():
    return {"message": "FastAPI Google OAuth 2.0 Demo"}

@app.get("/login/google")
async def login_google(request: Request):
    redirect_uri = request.url_for("google_callback")   
    return await oauth.google.authorize_redirect(
        request,
        redirect_uri,
        access_type="offline",
        prompt="consent"
    )

@app.get("/auth/google/callback")
async def google_callback(request: Request):

    token = await oauth.google.authorize_access_token(request)

    user = token.get("userinfo")

    if not user:
        raise HTTPException(
            status_code=400,
            detail="Cannot get Google user information"
        )

    request.session["user"] = {
        "google_id": user.get("sub"),
        "email": user.get("email"),
        "name": user.get("name"),
        "picture": user.get("picture")
    }

    return {
        "message": "Google OAuth login successful",
        "user": {
            "google_id": user.get("sub"),
            "email": user.get("email"),
            "name": user.get("name"),
            "picture": user.get("picture")
        },
        "token": {
            "access_token": token.get("access_token"),
            "refresh_token": token.get("refresh_token"),
            "token_type": token.get("token_type"),
            "expires_in": token.get("expires_in"),
            "id_token": token.get("id_token")
        }
    }

@app.get("/me")
async def get_current_user(request: Request):
    user = request.session.get("user")

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Not logged in"
        )
    return user

@app.get("/logout")
async def logout(request: Request):

    request.session.clear()

    return {
        "message": "Logout successful"
    }