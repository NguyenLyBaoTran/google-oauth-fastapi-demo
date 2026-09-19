# Google OAuth 2.0 Login Demo with FastAPI

A simple Google OAuth 2.0 login demo built with **FastAPI** and **Authlib**.

## Technologies

* Python
* FastAPI
* Uvicorn
* Authlib
* Google OAuth 2.0
* SessionMiddleware
* ngrok

## Project Structure

```text
TestOauth/
├── .env.example
├── .gitignore
├── main.py
├── requirements.txt
└── README.md
```

## Setup

### 1. Clone the project

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd TestOauth
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

Windows:

```powershell
.venv\Scripts\activate
```

macOS:

```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure environment variables

Create a `.env` file based on `.env.example`:

```env
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_REDIRECT_URI=http://localhost:8081/auth/google/callback
SESSION_SECRET=your_session_secret
```

Replace the placeholder values with your own Google OAuth credentials.

> Do not upload the `.env` file to GitHub.

## Google OAuth Configuration

Create a Google OAuth Client in Google Cloud Console.

For local testing, add this Authorized Redirect URI:

```text
http://localhost:8081/auth/google/callback
```

The Redirect URI in Google Cloud must exactly match the `GOOGLE_REDIRECT_URI` in `.env`.

## Run the Application

Start the FastAPI server:

```bash
uvicorn main:app --reload --port 8081
```

The application will run at:

```text
http://localhost:8081
```

## Using ngrok

ngrok can create a public HTTPS URL that forwards requests to the local FastAPI server.

This is useful when demonstrating OAuth with a public HTTPS URL or when the application needs to be accessed from outside the local computer.

### 1. Authenticate ngrok

If ngrok has not been authenticated yet:

```bash
ngrok config add-authtoken YOUR_NGROK_AUTHTOKEN
```

> Keep your ngrok authtoken private. Do not commit it to GitHub.

### 2. Run FastAPI

In the first terminal:

```powershell
cd C:\Users\Admin\Documents\A.HocTap\2026-2027\SOA\TestOauth
.venv\Scripts\activate
uvicorn main:app --reload --port 8081
```

Keep this terminal running.

### 3. Start ngrok

Open a second terminal and run:

```powershell
ngrok http 8081
```

ngrok will display a public forwarding URL similar to:

```text
Forwarding    https://example.ngrok-free.app -> http://localhost:8081
```

The actual URL may be different each time ngrok starts.

### 4. Update the Redirect URI

When using ngrok, update `.env`:

```env
GOOGLE_REDIRECT_URI=https://example.ngrok-free.app/auth/google/callback
```

Also add the same URL to Google Cloud Console under:

**Authorized Redirect URIs**

```text
https://example.ngrok-free.app/auth/google/callback
```

The URL must match exactly.

### 5. Test with ngrok

Open the public URL:

```text
https://example.ngrok-free.app
```

To start Google Login:

```text
https://example.ngrok-free.app/login/google
```

The OAuth flow is:

```text
User
→ /login/google
→ Google Login
→ /auth/google/callback
→ Save User in Session
→ /me
```

### Localhost vs ngrok

| Method | URL                            | HTTPS | Public Access |
| ------ | ------------------------------ | ----- | ------------- |
| Local  | `http://localhost:8081`        | No    | No            |
| ngrok  | `https://xxxxx.ngrok-free.app` | Yes   | Yes           |

ngrok does not replace FastAPI. It only creates a public HTTPS tunnel to the local FastAPI application.

## Test Google Login

Open the following URL in a browser:

```text
http://localhost:8081/login/google
```

Or, when using ngrok:

```text
https://YOUR_NGROK_URL/login/google
```

After successful login, Google redirects the browser to:

```text
/auth/google/callback
```

The application then saves the Google user information in the session.

## API Endpoints

| Method | Endpoint                | Description                         |
| ------ | ----------------------- | ----------------------------------- |
| GET    | `/`                     | Check if the application is running |
| GET    | `/login/google`         | Start Google OAuth login            |
| GET    | `/auth/google/callback` | Handle Google's OAuth callback      |
| GET    | `/me`                   | Get the current logged-in user      |

## Swagger UI

FastAPI provides Swagger UI at:

```text
http://localhost:8081/docs
```

When using ngrok:

```text
https://YOUR_NGROK_URL/docs
```

The `/me` endpoint can be tested from Swagger after completing Google Login in the browser.

The `/login/google` endpoint should be opened directly in a browser because it starts a redirect to Google.

## OAuth Flow

```text
User
  ↓
/login/google
  ↓
Google OAuth 2.0
  ↓
Google Login & Consent
  ↓
/auth/google/callback
  ↓
Exchange Authorization Code
  ↓
Get Google User Information
  ↓
Save User in Session
  ↓
/me
```

## Notes

This project is a simple OAuth 2.0 demonstration.

It currently stores the logged-in user's Google identity in the session. It does not create or store user accounts in a database.

For ngrok testing, the public URL may change when the ngrok session is restarted. If the URL changes, update both:

1. `GOOGLE_REDIRECT_URI` in `.env`
2. Authorized Redirect URI in Google Cloud Console
