from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from io import StringIO
from fastapi.responses import PlainTextResponse
from datetime import datetime
import os
import secrets

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# Session middleware
app.add_middleware(SessionMiddleware, secret_key="super-secret-session-key")

USERS = {
    "admin": "supersecret",
    "briggs": "password123",
    "merjel": "ediportal",
    "ops": "logistics"
}

# -----------------------------
# AUTH FUNCTIONS
# -----------------------------
def get_current_user(request: Request):
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=401)
    return user


# -----------------------------
# ROUTES
# -----------------------------
@app.get("/", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
def login(request: Request, username: str = Form(...), password: str = Form(...)):
    if username not in USERS:
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Invalid username or password"}
        )

    correct_password = secrets.compare_digest(password, USERS[username])

    if not correct_password:
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Invalid username or password"}
        )

    request.session["user"] = username
    return RedirectResponse("/dashboard", status_code=302)


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, user: str = Depends(get_current_user)):
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "user": user}
    )

@app.post("/cw/outbound")
async def receive_xml(request: Request):
    body = await request.body()
    xml_data = body.decode("utf-8")

    print(f"Saved XML file: {filename}")
    print(f"XML length: {len(xml_data)}")

    return PlainTextResponse("OK")

@app.post("/download")
def download_csv(
    request: Request,
    job_number: str = Form(...),
    company: str = Form(...),
    user: str = Depends(get_current_user)
):
    csv_data = StringIO()
    csv_data.write("job,company\n")
    csv_data.write(f"{job_number},{company}\n")
    csv_data.seek(0)

    return StreamingResponse(
        csv_data,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=report.csv"}
    )


@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/", status_code=302)
