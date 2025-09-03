from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Enable CORS for the Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,   # allow cookies/headers like auth
    allow_methods=["*"],      # for http meths like GET, POST
    allow_headers=["*"],      # allow custom headers like Content-Type
)

@app.get("/")
def read_root():
    return {"message": "Studybuddy API is running!"} # confirm api is live

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)): # tells FastAPI to expect a file upload
    return {"filename": file.filename}

# Starts the backend server so it can accept requests.
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)