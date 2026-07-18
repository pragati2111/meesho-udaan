import asyncio
from app.agents.orchestrator import run_pipeline

async def test():
    print("Running full pipeline...")

    result = await run_pipeline(
        skill_text="I make handmade scented candles for weddings and festivals."
    )

    print("\n=== PIPELINE COMPLETE ===")
    print("Blueprint ready:", result.get("blueprint_ready"))
    print("Blueprint ID:", result.get("blueprint_id"))
    print("Errors:", result.get("errors"))

    blueprint = result.get("compiled_blueprint", {})

    if blueprint:
        print("\nBrand:", blueprint.get("brand", {}).get("brand_name"))
        print("Product:", blueprint.get("product", {}).get("name"))
        print("Price:", blueprint.get("pricing", {}).get("recommended_price"))
        print("Demand:", blueprint.get("market", {}).get("demand_level"))

asyncio.run(test())
