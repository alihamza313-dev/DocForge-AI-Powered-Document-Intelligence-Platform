from uuid import UUID
import uuid
from datetime import datetime

from pydantic import BaseModel


class DocumentRead(BaseModel):
    id: uuid.UUID
    filename: str
    file_path: str
    status: str
    uploaded_at: datetime

    model_config = {
        "from_attributes": True
    }


class DocumentDetailResponse(BaseModel):
    id: UUID
    filename: str
    status: str
    uploaded_at: datetime
    extracted_text: str



class DocumentListResponse(BaseModel):
    id: UUID
    filename: str
    status: str
    uploaded_at: datetime