# Google OAuth FastAPI Demo

A simple FastAPI application demonstrating Google OAuth 2.0 authentication using Authlib and SessionMiddleware.

---

## Requirements

Before starting, make sure you have:

* Python 3.10 or later
* Git
* A Google account
* A Google Cloud project
* ngrok account (only required if you want to use a public HTTPS URL)

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

Create a Python virtual environment:

```bash
python -m venv .venv
```

If `python` is not available, try:

```bash
python3 -m venv .venv
```

---

### 3. Activate the virtual environment

#### Windows

PowerShell:

```powershell
.venv\Scripts\activate
```

Command Prompt:

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

After activation, you should see `(.venv)` at the beginning of your terminal prompt.

---

### 4. Install dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

---

## Google OAuth Configuration

This application uses Google OAuth 2.0 for user authentication.

You need to create a Google OAuth client and configure the redirect URI before running the application.

### 1. Open Google Cloud Console

Open:

[Google Cloud Console](https://console.cloud.google.com/?utm_source=chatgpt.com)

Select an existing project or create a new Google Cloud project.

### 2. Create OAuth credentials

Depending on the Google Cloud Console interface, you can access OAuth configuration through either:

**Google Auth Platform → Clients**

or:

**APIs & Services → Credentials**

Create a new **OAuth client ID**.

For the application type, select:

```text
Web application
```

### 3. Configure the redirect URI

For local development, add the following under **Authorized redirect URIs**:

```text
http://localhost:8081/auth/google/callback
```

The redirect URI must exactly match the value used by the application.

### 4. Get the Client ID and Client Secret

After creating the OAuth client, Google provides:

```text
Client ID
Client Secret
```

Keep the Client Secret private.

You will use these values in the `.env` file.

---

## Environment Variables

### 1. Create the `.env` file

Create `.env` from `.env.example`.

#### Windows PowerShell

```powershell
Copy-Item .env.example .env
```

Open the file:

```powershell
notepad .env
```

#### Linux / macOS

```bash
cp .env.example .env
nano .env
```

You can also use VS Code:

```bash
code .env
```

### 2. Configure `.env`

Set the following values:

```env
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_REDIRECT_URI=http://localhost:8081/auth/google/callback
SESSION_SECRET=your_session_secret
```

Replace:

* `your_google_client_id` with your Google OAuth Client ID
* `your_google_client_secret` with your Google OAuth Client Secret
* `your_session_secret` with a random secret string

### 3. Generate a session secret

You can generate a secure random session secret using Python.

Windows:

```powershell
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Linux / macOS:

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

Copy the generated value into:

```env
SESSION_SECRET=your_generated_secret
```

### 4. Check the `.env` file

Windows PowerShell:

```powershell
Get-Content .env
```

Linux / macOS:

```bash
cat .env
```

> Never commit `.env` to GitHub.

Make sure `.gitignore` contains:

```text
.env
.venv/
__pycache__/
```

---

## Run the Application

Start the FastAPI development server.

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

### Linux with fish shell

```fish
source .venv/bin/activate.fish
uvicorn main:app --reload --port 8081
```

The application should now be available at:

```text
http://localhost:8081
```

You can test the root endpoint by opening:

```text
http://localhost:8081/
```

---

## Using ngrok

ngrok creates a public HTTPS URL that forwards requests to your local FastAPI server.

This is useful when you need to demonstrate the application using a public HTTPS URL or access the application from another device.

### 1. Install ngrok

Download and install ngrok from the official website:

[Download ngrok](https://ngrok.com/download?utm_source=chatgpt.com)

After installation, verify that ngrok is available:

```bash
ngrok version
```

If the command displays the ngrok version, the installation was successful.

### 2. Run the FastAPI application

First, start the FastAPI server.

#### Windows

```powershell
.venv\Scripts\activate
uvicorn main:app --reload --port 8081
```

#### Linux / macOS

```bash
source .venv/bin/activate
uvicorn main:app --reload --port 8081
```

#### Linux with fish shell

```fish
source .venv/bin/activate.fish
uvicorn main:app --reload --port 8081
```

Keep this terminal running.

The application should now be available at:

```text
http://localhost:8081
```

### 3. Authenticate ngrok

Open a **new terminal**.

If ngrok has not been authenticated yet, run:

```bash
./ngrok config add-authtoken YOUR_NGROK_AUTHTOKEN
```

Replace `YOUR_NGROK_AUTHTOKEN` with your ngrok authentication token.

> This step only needs to be done once.

> Keep your ngrok authtoken private. Do not commit it to GitHub.

### 4. Start ngrok

In the new terminal, run:

```bash
ngrok http 8081
```

ngrok will display a public HTTPS URL similar to:

```text
Forwarding    https://abc123.ngrok-free.app -> http://localhost:8081
```

Copy the HTTPS URL:

```text
https://abc123.ngrok-free.app
```

Keep the ngrok terminal running.

### 5. Update the Google OAuth Redirect URI

Open your `.env` file and update:

```env
GOOGLE_REDIRECT_URI=https://abc123.ngrok-free.app/auth/google/callback
```

Replace `abc123.ngrok-free.app` with your actual ngrok URL.

Then add the **same redirect URI** to Google Cloud under **Authorized redirect URIs**.

For example:

```text
https://abc123.ngrok-free.app/auth/google/callback
```

> The redirect URI in `.env` and Google Cloud must match exactly.

### 6. Restart the FastAPI application

After changing `.env`, restart FastAPI so the new environment variables are loaded.

Stop the FastAPI server with:

```text
Ctrl + C
```

Then start it again.

#### Windows

```powershell
.venv\Scripts\activate
uvicorn main:app --reload --port 8081
```

#### Linux / macOS

```bash
source .venv/bin/activate
uvicorn main:app --reload --port 8081
```

#### Linux with fish shell

```fish
source .venv/bin/activate.fish
uvicorn main:app --reload --port 8081
```

Keep both terminals running:

```text
Terminal 1:
FastAPI → http://localhost:8081

Terminal 2:
ngrok   → https://abc123.ngrok-free.app
```

---

## Test Google Login

Open the following URL in your browser:

```text
https://YOUR_NGROK_URL/login/google
```

For example:

```text
https://abc123.ngrok-free.app/login/google
```

You will be redirected to Google to sign in.

After successful authentication, Google redirects you back to:

```text
https://abc123.ngrok-free.app/auth/google/callback
```

The application then stores the authenticated user information in the session.

To check the logged-in user, open:

```text
https://abc123.ngrok-free.app/me
```

If authentication is successful, `/me` returns the authenticated user's information.

---

## Localhost vs ngrok

| Environment | URL                      | HTTPS | Public Access |
| ----------- | ------------------------ | ----- | ------------- |
| Localhost   | `http://localhost:8081`  | No    | No            |
| ngrok       | `https://YOUR_NGROK_URL` | Yes   | Yes           |

Use **localhost** during normal local development.

Use **ngrok** when you need a public HTTPS URL for demonstration or OAuth testing.

> Your ngrok URL may change when the ngrok tunnel is restarted.

If the ngrok URL changes, update both:

1. `GOOGLE_REDIRECT_URI` in `.env`
2. **Authorized redirect URIs** in Google Cloud

---

## API Endpoints

| Method | Endpoint                | Description                              |
| ------ | ----------------------- | ---------------------------------------- |
| GET    | `/`                     | Check whether the application is running |
| GET    | `/login/google`         | Start Google OAuth login                 |
| GET    | `/auth/google/callback` | Handle the Google OAuth callback         |
| GET    | `/me`                   | Get the currently authenticated user     |

### Localhost

```text
http://localhost:8081/
http://localhost:8081/login/google
http://localhost:8081/me
```

### ngrok

```text
https://YOUR_NGROK_URL/
https://YOUR_NGROK_URL/login/google
https://YOUR_NGROK_URL/me
```

> Open `/login/google` directly in a browser because this endpoint redirects the user to Google's login page.

---

## Swagger UI

FastAPI provides interactive API documentation through Swagger UI.

### Localhost

```text
http://localhost:8081/docs
```

### ngrok

```text
https://YOUR_NGROK_URL/docs
```

Swagger UI allows you to view and test the available API endpoints.

For Google OAuth login, open `/login/google` directly in a browser because it redirects to Google.

---

## OAuth Flow

The Google OAuth authentication flow works as follows:

```text
User
  ↓
/login/google
  ↓
Google Login
  ↓
Google Authentication
  ↓
/auth/google/callback
  ↓
Save User Information in Session
  ↓
/me
  ↓
Authenticated User Information
```

### Step-by-step

1. The user opens `/login/google`.
2. The application redirects the user to Google.
3. The user signs in with their Google account.
4. Google redirects the user to `/auth/google/callback`.
5. The application exchanges the authorization code for Google OAuth tokens.
6. The application retrieves the user's Google account information.
7. The user's information is stored in the session.
8. The user can access `/me` to view their authenticated information.

---

## Notes

* This project is a demonstration of Google OAuth 2.0 authentication using FastAPI and Authlib.
* The application uses `SessionMiddleware` to maintain the user's login session.
* No database is used to store user information in this demo.
* The `.env` file contains sensitive configuration and must not be committed to GitHub.
* The ngrok authtoken must also be kept private.
* The ngrok public URL may change when the tunnel is restarted.
* If the ngrok URL changes, update the Google OAuth redirect URI in both `.env` and Google Cloud.
* The FastAPI server and ngrok tunnel must both be running when testing through the public URL.
* For local development, use `http://localhost:8081`.
* For OAuth testing through a public HTTPS URL, use the ngrok URL.
