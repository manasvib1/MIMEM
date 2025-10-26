from fastapi import FastAPI
from pydantic import BaseModel
import re

app = FastAPI()

class Attachment(BaseModel):
    url: str

class RequestModel(BaseModel):
    attachments: Attachment

@app.post("/file")
async def detect_mime_type(data: RequestModel):
    data_uri = data.attachments.url
    match = re.match(r"^data:([\w\-/]+);base64,", data_uri)
    if not match:
        return {"type": "unknown"}

    mime_type = match.group(1)
    main_type = mime_type.split('/')[0]
    if main_type in ["image", "text", "application"]:
        return {"type": main_type}
    else:
        return {"type": "unknown"}
