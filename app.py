from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from io import StringIO
from pathlib import Path

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

@app.post("/download")
def download_csv(
    job_number: str = Form(...),
    company: str = Form(...)
):
    csv_data = StringIO()
    csv_data.write("job,company\n")
    csv_data.write(f"{job_number},{company}\n")
    csv_data.seek(0)

    return StreamingResponse(
        csv_data,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=test.csv"}
    )
