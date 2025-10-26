from fastapi import FastAPI
from pydantic import BaseModel
import re
import uvicorn

app = FastAPI()

# Root route to confirm the app is running
@app.get("/")
def root():
    return {"message": "FastAPI MIME Detector is running!"}

# Pydantic models for request
class Attachment(BaseModel):
    url: str

class RequestModel(BaseModel):
    attachments: Attachment

# POST endpoint to detect MIME type
@app.post("/file")
async def detect_mime_type(data: RequestModel):
    data_uri = data.attachments.url

    # Match data URI pattern
    match = re.match(r"^data:([\w\-/]+);base64,", data_uri)
    if not match:
        return {"type": "unknown"}

    mime_type = match.group(1)
    main_type = mime_type.split('/')[0]

    if main_type in ["image", "text", "application"]:
        return {"type": main_type}
    else:
        return {"type": "unknown"}

# Optional: only needed if running locally
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

