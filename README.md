# Google OAuth FastAPI Demo

A simple FastAPI application demonstrating **Google OAuth 2.0 authentication** using **Authlib** and **SessionMiddleware**.

The project demonstrates:

- Google Login with OAuth 2.0
- OpenID Connect user information
- Dynamic Redirect URI
- Access Token
- ID Token
- Refresh Token
- Token expiration
- User session
- Logout

---

## Table of Contents

1. [Requirements](#requirements)
2. [Setup](#setup)
3. [Google OAuth Configuration](#google-oauth-configuration)
4. [Environment Variables](#environment-variables)
5. [Run the Application](#run-the-application)
6. [Using ngrok](#using-ngrok)
7. [Dynamic Redirect URI](#dynamic-redirect-uri)
8. [Test Google Login](#test-google-login)
9. [OAuth Tokens](#oauth-tokens)
10. [Refresh Token and Token Expiration](#refresh-token-and-token-expiration)
11. [Logout](#logout)
12. [Localhost vs ngrok](#localhost-vs-ngrok)
13. [API Endpoints](#api-endpoints)
14. [Swagger UI](#swagger-ui)
15. [OAuth Flow](#oauth-flow)
16. [Notes](#notes)

---

## Requirements

Before starting, make sure you have:

- Python 3.10 or later
- Git
- A Google account
- A Google Cloud project
- ngrok account (only required if you want to use a public HTTPS URL)

---

## Setup

### 1. Clone the project

Clone the repository:

```bash
git clone https://github.com/NguyenLyBaoTran/google-oauth-fastapi-demo TestOauth
cd TestOauth
```

If you already have the project downloaded, simply open a terminal in the project directory.

---

### 2. Create a virtual environment

```bash
python -m venv .venv
```

If `python` is not available, try:

```bash
python3 -m venv .venv
```

---

### 3. Activate the virtual environment

#### Windows PowerShell

```powershell
.venv\Scripts\activate
```

#### Windows Command Prompt

```cmd
.venv\Scripts\activate.bat
```

#### Linux / macOS

```bash
source .venv/bin/activate
```

#### Linux with fish shell

```fish
source .venv/bin/activate.fish
```

After activation, you should see `(.venv)` at the beginning of the terminal prompt.

---

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Google OAuth Configuration

This application uses **Google OAuth 2.0** for authentication.

You need to create a Google OAuth Client before running the application.

### 1. Open Google Cloud Console

Open Google Cloud Console and select an existing project or create a new project.

### 2. Configure Google Auth Platform

Configure:

- Branding
- Audience
- Data Access
- Clients

For this demo, the application requests:

```text
openid
email
profile
```

These scopes allow the application to identify the user and retrieve basic account information such as email, name, and profile picture.

### 3. Create OAuth Client

Go to:

```text
Google Auth Platform → Clients
```

Create a new OAuth Client.

Application type:

```text
Web application
```

Google will provide:

```text
Client ID
Client Secret
```

Keep the **Client Secret** private.

---

### 4. Add Authorized Redirect URIs

Google only redirects users to URLs registered under **Authorized redirect URIs**.

For localhost, add:

```text
http://localhost:8081/auth/google/callback
```

If you use `127.0.0.1` instead, register the matching URI:

```text
http://127.0.0.1:8081/auth/google/callback
```

For ngrok, add:

```text
https://YOUR_NGROK_URL/auth/google/callback
```

Example:

```text
https://abc123.ngrok-free.app/auth/google/callback
```

> The Redirect URI must exactly match the URL used by the application.

---

## Environment Variables

### 1. Create `.env`

Create `.env` from `.env.example`.

#### Windows PowerShell

```powershell
Copy-Item .env.example .env
```

Open it:

```powershell
notepad .env
```

#### Linux / macOS

```bash
cp .env.example .env
nano .env
```

---

### 2. Configure `.env`

```env
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
SESSION_SECRET=your_session_secret
```

Replace:

- `your_google_client_id` with the Google OAuth Client ID
- `your_google_client_secret` with the Google OAuth Client Secret
- `your_session_secret` with a random secret string

The Redirect URI is **not stored in `.env`** because the application generates it dynamically.

---

### 3. Generate a Session Secret

#### Windows

```powershell
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

#### Linux / macOS

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

Copy the generated value into:

```env
SESSION_SECRET=your_generated_secret
```

---

### 4. Protect Sensitive Information

Never commit `.env` to GitHub.

Make sure `.gitignore` contains:

```text
.env
.venv/
__pycache__/
```

Never commit:

- Client Secret
- Session Secret
- Access Token
- Refresh Token
- ID Token

---

## Run the Application

### Windows

```powershell
.venv\Scripts\activate
uvicorn main:app --reload --port 8081
```

### Linux / macOS

```bash
source .venv/bin/activate
uvicorn main:app --reload --port 8081
```

The application should now be available at:

```text
http://localhost:8081
```

Test the root endpoint:

```text
http://localhost:8081/
```

---

## Using ngrok

ngrok creates a public HTTPS URL that forwards requests to the local FastAPI server.

### 1. Run FastAPI

Terminal 1:

```powershell
.venv\Scripts\activate
uvicorn main:app --reload --port 8081
```

Keep this terminal running.

---

### 2. Authenticate ngrok

Open another terminal.

If ngrok has not been authenticated yet:

```bash
ngrok config add-authtoken YOUR_NGROK_AUTHTOKEN
```

This step normally only needs to be completed once.

Keep the ngrok authtoken private.

---

### 3. Start ngrok

Terminal 2:

```bash
ngrok http 8081
```

Example output:

```text
Forwarding
https://abc123.ngrok-free.app
→
http://localhost:8081
```

Keep this terminal running.

---

### 4. Add ngrok Redirect URI to Google

If the ngrok URL is:

```text
https://abc123.ngrok-free.app
```

add this to Google Cloud:

```text
https://abc123.ngrok-free.app/auth/google/callback
```

Then start OAuth from:

```text
https://abc123.ngrok-free.app/login/google
```

> Free ngrok URLs may change when the tunnel is restarted.

If the ngrok domain changes, update the **Authorized redirect URI in Google Cloud**.

You do **not** need to change the Redirect URI in the FastAPI source code or `.env`.

---

## Dynamic Redirect URI

The application generates the OAuth callback URL dynamically.

Example:

```python
redirect_uri = request.url_for("google_callback")
```

This means the Redirect URI depends on the URL used to access the application.

### Localhost

If OAuth starts from:

```text
http://localhost:8081/login/google
```

the application can generate:

```text
http://localhost:8081/auth/google/callback
```

### ngrok

If OAuth starts from:

```text
https://abc123.ngrok-free.app/login/google
```

the application can generate:

```text
https://abc123.ngrok-free.app/auth/google/callback
```

Therefore, the source code does not need a hard-coded:

```text
GOOGLE_REDIRECT_URI
```

However, Google still requires the generated Redirect URI to be registered under:

```text
Authorized redirect URIs
```

Dynamic Redirect URI does **not** bypass Google's Redirect URI validation.

---

## Test Google Login

### Localhost

Open:

```text
http://localhost:8081/login/google
```

### ngrok

Open:

```text
https://YOUR_NGROK_URL/login/google
```

The application redirects the browser to Google.

After successful authentication, Google redirects the browser to:

```text
/auth/google/callback
```

The callback:

1. Processes the Google OAuth response.
2. Exchanges the authorization code for tokens.
3. Retrieves Google user information.
4. Stores user information in the session.
5. Returns token information for demonstration.

Example response:

```json
{
  "message": "Google OAuth login successful",
  "user": {
    "google_id": "...",
    "email": "...",
    "name": "...",
    "picture": "..."
  },
  "token": {
    "access_token": "...",
    "refresh_token": "...",
    "token_type": "Bearer",
    "expires_in": 3599,
    "id_token": "..."
  }
}
```

> Tokens are displayed only for educational demonstration. Real applications should not expose sensitive tokens unnecessarily.

---

## OAuth Tokens

The callback can return several token-related values.

### Access Token

```text
access_token
```

The Access Token is used to access APIs or resources that the user has authorized.

In this demo, the requested scopes are:

```text
openid email profile
```

---

### ID Token

```text
id_token
```

The ID Token is part of **OpenID Connect**.

It contains identity information about the authenticated user.

Simple difference:

```text
Access Token → access authorized resources

ID Token     → information about who the user is
```

---

### Token Type

```text
token_type = Bearer
```

This indicates how the Access Token is normally sent when calling an API.

---

### expires_in

Example:

```text
expires_in = 3599
```

`expires_in` is measured in seconds.

```text
3599 seconds
≈ 59 minutes 59 seconds
≈ 1 hour
```

This means the Access Token is valid for approximately one hour.

Token expiration is a normal OAuth security mechanism.

---

### Refresh Token

```text
refresh_token
```

The Refresh Token can be used to obtain a new Access Token after the current Access Token expires.

To request offline access, the login flow can use:

```python
access_type="offline"
```

For testing or demonstration, Google OAuth can also be requested with:

```python
prompt="consent"
```

`prompt="consent"` forces Google to show the consent screen again. This can be useful during testing when demonstrating Refresh Token behavior.

It is not the mechanism that refreshes the Access Token.

---

## Refresh Token and Token Expiration

An Access Token is intentionally short-lived.

Example:

```text
Access Token
     ↓
expires_in ≈ 1 hour
     ↓
Access Token expires
```

The application should not try to manually increase `expires_in`.

Instead, a real application can use a Refresh Token:

```text
Access Token expires
        ↓
Use Refresh Token
        ↓
Google Token Endpoint
        ↓
New Access Token
        ↓
Continue using the application
```

Therefore, the user normally does **not** need to sign in again every time the Access Token expires, as long as a valid Refresh Token is available.

If the Refresh Token is no longer valid or has been revoked, the user may need to authenticate or authorize the application again.

---

## Logout

To log out from this FastAPI application:

```text
/logout
```

The logout endpoint clears the application session:

```python
request.session.clear()
```

Flow:

```text
Logged-in User
      ↓
/logout
      ↓
Clear FastAPI Session
      ↓
Logged out from the application
```

This logs the user out of the **FastAPI application**.

It does **not** automatically:

- Sign the user out of their Google account
- Sign the user out of Google Chrome
- Revoke Google OAuth permissions

Therefore, after logout, Google may still recognize the Google account when the user starts the login process again.

---

## Localhost vs ngrok

| Environment | Example URL | HTTPS | Public |
|---|---|---|---|
| Localhost | `http://localhost:8081` | No | No |
| ngrok | `https://YOUR_NGROK_URL` | Yes | Yes |

### Localhost

Use:

```text
http://localhost:8081/login/google
```

Generated callback:

```text
http://localhost:8081/auth/google/callback
```

### ngrok

Use:

```text
https://YOUR_NGROK_URL/login/google
```

Generated callback:

```text
https://YOUR_NGROK_URL/auth/google/callback
```

If the free ngrok URL changes:

```text
Old:
https://abc123.ngrok-free.app

New:
https://xyz789.ngrok-free.app
```

you only need to register the new callback in Google Cloud:

```text
https://xyz789.ngrok-free.app/auth/google/callback
```

The FastAPI source code does not need to be changed.

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Check whether the application is running |
| GET | `/login/google` | Start Google OAuth login |
| GET | `/auth/google/callback` | Handle OAuth callback and receive tokens |
| GET | `/me` | Get the currently authenticated user |
| GET | `/logout` | Clear the session and log out from the application |

### Local

```text
http://localhost:8081/
http://localhost:8081/login/google
http://localhost:8081/me
http://localhost:8081/logout
```

### ngrok

```text
https://YOUR_NGROK_URL/
https://YOUR_NGROK_URL/login/google
https://YOUR_NGROK_URL/me
https://YOUR_NGROK_URL/logout
```

Open `/login/google` directly in a browser because the endpoint redirects the browser to Google's authentication page.

---

## Swagger UI

FastAPI provides interactive API documentation through Swagger UI.

### Local

```text
http://localhost:8081/docs
```

### ngrok

```text
https://YOUR_NGROK_URL/docs
```

Swagger UI can be used to view the available API endpoints.

For the Google OAuth login flow, it is easier to open:

```text
/login/google
```

directly in the browser because OAuth requires browser redirects.

---

## OAuth Flow

### Complete Flow

```text
User
 ↓
/login/google
 ↓
Generate Dynamic Redirect URI
 ↓
Redirect to Google
 ↓
Google Login / Consent
 ↓
/auth/google/callback
 ↓
Exchange Authorization Code
 ↓
Access Token + ID Token + Refresh Token
 ↓
Get Google User Information
 ↓
Save User in Session
 ↓
/me
 ↓
Authenticated User
```

### Token Expiration

```text
Access Token
 ↓
expires_in ≈ 1 hour
 ↓
Token expires
 ↓
Refresh Token
 ↓
Request new Access Token
 ↓
Continue without Google Login again
```

### Logout

```text
Authenticated User
 ↓
/logout
 ↓
Clear Session
 ↓
Logged out from FastAPI application
```

---

## Step-by-Step OAuth Process

1. The user opens `/login/google`.
2. FastAPI dynamically creates the callback URL.
3. The application redirects the browser to Google.
4. The user signs in with a Google account.
5. Google asks for consent when required.
6. Google redirects the browser to `/auth/google/callback`.
7. Authlib processes the OAuth callback.
8. The authorization code is exchanged for OAuth tokens.
9. The application retrieves the user's Google account information.
10. The user information is stored in the session.
11. `/me` reads the session and returns the authenticated user.
12. When the Access Token expires, a valid Refresh Token can be used to obtain a new Access Token.
13. `/logout` clears the application session.

---

## Notes

- This project is an educational demonstration of Google OAuth 2.0 and OpenID Connect with FastAPI.
- Authlib handles the OAuth/OpenID Connect flow.
- `SessionMiddleware` maintains the application login session.
- `SESSION_SECRET` is used to sign and protect session data.
- The application requests `openid email profile`.
- `access_type="offline"` can be used when a Refresh Token is required.
- `prompt="consent"` can be used during testing to force the Google consent screen to appear again.
- Access Tokens normally have a limited lifetime.
- A Refresh Token can be used to obtain a new Access Token without requiring the user to sign in again.
- `/logout` clears the FastAPI session but does not sign the user out of Google.
- No database is used to store user information in this demo.
- `.env` must not be committed to GitHub.
- Client Secret, Session Secret, Access Token, Refresh Token, and ID Token should not be exposed publicly.
- The Redirect URI is generated dynamically and is no longer stored in `.env`.
- Google still requires every Redirect URI used by the application to be registered in **Authorized redirect URIs**.
- If a free ngrok domain changes, update the Authorized Redirect URI in Google Cloud.
- The FastAPI server and ngrok tunnel must both be running when testing through ngrok.
