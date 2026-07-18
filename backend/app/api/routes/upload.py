from fastapi import APIRouter

router = APIRouter()


@router.post("/voice")
async def upload_voice():
    """Placeholder — implemented in Phase 7."""
    return {"message": "Voice upload coming in Phase 7"}


@router.post("/image")
async def upload_image():
    """Placeholder — implemented in Phase 8."""
    return {"message": "Image upload coming in Phase 8"}