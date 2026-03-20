from fastapi import FastAPI, Request, Form, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from io import StringIO
import secrets

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# -----------------------------
# AUTH SETUP
# -----------------------------
security = HTTPBasic()

USERNAME = "admin"
PASSWORD = "supersecret"

def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, USERNAME)
    correct_password = secrets.compare_digest(credentials.password, PASSWORD)

    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


# -----------------------------
# ROUTES
# -----------------------------

# Public route (no login)
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


# Protected route (requires login popup)
@app.post("/download")
def download_csv(
    request: Request,
    job_number: str = Form(...),
    company: str = Form(...),
    user: str = Depends(authenticate)  # 🔒 Protect this route
):
    csv_data = StringIO()
    csv_data.write("job,company\n")
    csv_data.write(f"{job_number},{company}\n")
    csv_data.seek(0)

    return StreamingResponse(
        csv_data,
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=test.csv"
        }
    )


# Optional: Test protected GET route
@app.get("/protected")
def protected_route(user: str = Depends(authenticate)):
    return {"message": f"Welcome {user}"}
