from fastapi import APIRouter, HTTPException
from app.models.blueprint import GenerateRequest, GenerateResponse, BusinessBlueprint
from app.agents.orchestrator import run_pipeline
from app.core.database import get_db

router = APIRouter()


@router.post("/generate", response_model=GenerateResponse)
async def generate_blueprint(request: GenerateRequest) -> GenerateResponse:
    if not request.skill_text and not request.skill_image_url and not request.skill_audio_url:
        raise HTTPException(status_code=400, detail="At least one skill input is required.")

    final_state = await run_pipeline(
        skill_text=request.skill_text,
        skill_image_url=request.skill_image_url,
        skill_audio_url=request.skill_audio_url,
        language=request.language,
    )

    if not final_state.get("blueprint_ready"):
        errors = final_state.get("errors", {})
        raise HTTPException(status_code=500, detail=f"Pipeline failed: {errors}")

    blueprint_data = final_state.get("compiled_blueprint")
    if not blueprint_data:
        raise HTTPException(status_code=500, detail="No blueprint generated.")

    db = get_db()
    await db.blueprints.insert_one({**blueprint_data})

    return GenerateResponse(
        blueprint_id=blueprint_data["id"],
        status="completed",
        message="Blueprint generated successfully",
    )


@router.get("/blueprint/{blueprint_id}", response_model=BusinessBlueprint)
async def get_blueprint(blueprint_id: str) -> BusinessBlueprint:
    db = get_db()
    doc = await db.blueprints.find_one({"id": blueprint_id})

    if not doc:
        raise HTTPException(status_code=404, detail="Blueprint not found.")

    doc.pop("_id", None)
    return BusinessBlueprint(**doc)