# backend/src/api/classify_controller.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.src.services.classify_service import ClassifyService

# Create Router
classify_router = APIRouter()

# Initialize the service
classifier = ClassifyService()

# Request model
class ClassifyRequest(BaseModel):
    product_name: str

# Response model (optional for OpenAPI docs, but we can keep dynamic for now)

# === API Route ===
@classify_router.post("/")
async def classify_product_api(request: ClassifyRequest):
    """
    Classify a product name and return UNSPSC code and matched name.
    """
    try:
        product_name = request.product_name

        if not product_name:
            raise HTTPException(status_code=400, detail="Missing 'product_name' in request body.")

        results = classifier.classify_product(product_name)

        return {
            "status": "success",
            "data": results
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
