from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
import my_script
import os

app = FastAPI()

class Payload(BaseModel):
    base64_pdf: str

@app.post("/run")
def run_job(p: Payload):
    try:
        result = my_script.run({"text": p.base64_pdf})
        return {"ok": True, "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/run-file")
async def run_file(file: UploadFile = File(...)):
    try:
        content = await file.read()
        result = my_script.run({"file_bytes": content, "filename": file.filename})
        return {"ok": True, "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/")
def root():
    return {"status": "healthy", "service": "orderlinks-pdf-api"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
```

## Add a Procfile

Create a new file called **Procfile** (no extension):
```
web: uvicorn app:app --host 0.0.0.0 --port $PORT
