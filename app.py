from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from io import StringIO
import secrets

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Session middleware
app.add_middleware(SessionMiddleware, secret_key="super-secret-session-key")

USERNAME = "admin"
PASSWORD = "supersecret"


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
    correct_username = secrets.compare_digest(username, USERNAME)
    correct_password = secrets.compare_digest(password, PASSWORD)

    if not (correct_username and correct_password):
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
