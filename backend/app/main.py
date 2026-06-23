from fastapi import FastAPI

from app.api.project import router as project_router

app = FastAPI(
    title="AI Test Generation Platform",
    version="1.0.0"
)

app.include_router(project_router)


@app.get("/")
def root():
    return {
        "message": "AI Test Generation Platform Running"
    }


@app.get("/health")
def health():
    return {
        "status": "UP"
    }