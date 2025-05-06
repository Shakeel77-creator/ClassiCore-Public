from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.src.api.classify_controller import classify_router

def create_app():
    app = FastAPI(
        title="ClassiCore Classification API",
        description="API to classify product names into UNSPSC codes using Granite model.",
        version="1.0.0"
    )

    # ✅ CORS config
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ✅ Router
    app.include_router(classify_router, prefix="/api/classify")

    return app

app = create_app()
