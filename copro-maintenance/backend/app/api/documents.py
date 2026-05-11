import os
import uuid
import aiofiles
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import FileResponse

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.building import Building
from app.models.equipment import Equipment
from app.models.document import Document

router = APIRouter(prefix="/documents", tags=["documents"])

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)


class DocumentResponse(BaseModel):
    id: int
    equipment_id: int | None
    filename: str
    original_name: str
    content_type: str
    size: int
    uploaded_at: str

    model_config = {"from_attributes": True}


@router.post("/upload", status_code=status.HTTP_201_CREATED, response_model=DocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
    equipment_id: int | None = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    # If equipment_id provided, verify it belongs to user
    if equipment_id is not None:
        result = await db.execute(
            select(Equipment)
            .join(Building, Equipment.building_id == Building.id)
            .where(Equipment.id == equipment_id, Building.user_id == current_user.id)
        )
        eq = result.scalar_one_or_none()
        if not eq:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Equipment not found")

    # Generate unique filename
    ext = os.path.splitext(file.filename or "file")[1]
    unique_name = f"{uuid.uuid4().hex}{ext}"
    file_path = os.path.join(UPLOAD_DIR, unique_name)

    # Save file
    async with aiofiles.open(file_path, "wb") as f:
        content = await file.read()
        await f.write(content)

    # Create document record
    doc = Document(
        equipment_id=equipment_id,
        user_id=current_user.id,
        filename=unique_name,
        original_name=file.filename or "unknown",
        content_type=file.content_type or "application/octet-stream",
        size=len(content),
    )
    db.add(doc)
    await db.commit()
    await db.refresh(doc)

    return DocumentResponse(
        id=doc.id,
        equipment_id=doc.equipment_id,
        filename=doc.filename,
        original_name=doc.original_name,
        content_type=doc.content_type,
        size=doc.size,
        uploaded_at=doc.uploaded_at.isoformat() if doc.uploaded_at else "",
    )


@router.get("/{document_id}")
async def download_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Document).where(Document.id == document_id, Document.user_id == current_user.id)
    )
    doc = result.scalar_one_or_none()
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")

    file_path = os.path.join(UPLOAD_DIR, doc.filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found on disk")

    return FileResponse(
        path=file_path,
        filename=doc.original_name,
        media_type=doc.content_type,
    )


@router.get("", response_model=list[DocumentResponse])
async def list_documents(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Document)
        .where(Document.user_id == current_user.id)
        .order_by(Document.uploaded_at.desc())
    )
    docs = result.scalars().all()

    return [
        DocumentResponse(
            id=d.id,
            equipment_id=d.equipment_id,
            filename=d.filename,
            original_name=d.original_name,
            content_type=d.content_type,
            size=d.size,
            uploaded_at=d.uploaded_at.isoformat() if d.uploaded_at else "",
        )
        for d in docs
    ]
