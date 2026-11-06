import json
import uuid_utils as uuid

from pathlib import Path
from fastapi import FastAPI, HTTPException, status
from models.report import Report

app = FastAPI()

REPORTS_DIR = Path("reports_storage")
REPORTS_DIR.mkdir(exist_ok=True)

@app.post("/report/")
def create_appeal(report: Report):
    try:
        report_data = report.model_dump(mode="json")

        file_name = f"report_{uuid.uuid7()}.json"
        file_path = REPORTS_DIR / file_name

        with open(file_path, "w", encoding="utf-8") as f:
                json.dump(report_data, f, ensure_ascii=False, indent=4)
                
        return {
            "status": "success",
            "message": "Обращение успешно зарегистрировано",
            "saved_file": file_name
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Внутренняя ошибка при сохранении отчета: {str(e)}"
        )

