from fastapi import FastAPI, Path, Body
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import Field, field_validator, BaseModel
from typing import List
import asyncio
import time
import json

app = FastAPI(title="AI-ML 90 days - Streaming MLOps")

class PredictRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=800)
    model_type: str = Field(default="llama3-8b")
    stream: bool = Field(default=False, description="True=chatgpt typing")

    @field_validator('text')
    @classmethod
    def no_empty(cls, v):
        if not v.strip():
            raise ValueError("Empty not allowed")
        return v

class Student(BaseModel):
    roll_no: int
    sem: int
    marks: List[float]

async def fake_llama_stream(prompt: str, model_type: str):
    response_text = f"Received {len(prompt)} chars for {model_type}. Hello MLOps Engineer you said: {prompt}"
    for word in response_text.split():
        data = json.dumps({"token": word, "model": model_type})
        yield f"data: {data}\n\n"
        await asyncio.sleep(0.15)
    yield "data: [DONE]\n\n"

@app.post("/predict")
async def predict(req: PredictRequest):
    if not req.stream:
        start = time.time()
        result = f"Received {len(req.text)} chars for {req.model_type}"
        latency = (time.time() - start) * 1000
        return JSONResponse(content={
            "prediction": result,
            "latency_ms": round(latency, 2),
            "model_version": req.model_type,
            "type": "json"
        })
    else:
        return StreamingResponse(
            fake_llama_stream(req.text, req.model_type),
            media_type="text/event-stream",
            headers={"X-model_type": req.model_type}
        )

@app.post("/student/{roll_no}/marks/")
async def create_report(
    roll_no: int = Path(..., gt=0),
    student: Student = Body(...)
):
    total = sum(student.marks)
    avg = round(total / len(student.marks), 2) if student.marks else 0

    if avg >= 85:
        grade = "Grade A"
    elif avg >= 65:
        grade = "Grade B"
    elif avg >= 35:
        grade = "Grade C"
    else:
        grade="Fail"   

    return {
        "student_roll_no": roll_no,
        "total": total,
        "average": avg,
        "grade": grade,
    }

@app.get("/")
async def home():
    return {"docs": "/docs", "test_stream": "POST /predict with stream=True"}