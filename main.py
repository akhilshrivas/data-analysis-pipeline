"""FastAPI backend for autonomous data analysis pipeline."""

from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn
from pathlib import Path

from agents.copilot import AnalyticsCopilotAgent
from config import settings
from graph.workflow import run_analysis
from logger import setup_logger
from services.run_store import RunStore

logger = setup_logger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description=settings.API_DESCRIPTION,
    debug=settings.DEBUG,
)

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create uploads directory
uploads_dir = Path("data/uploads")
uploads_dir.mkdir(parents=True, exist_ok=True)
run_store = RunStore()
copilot_agent = AnalyticsCopilotAgent()


class CopilotQuestion(BaseModel):
    """Request body for analytics copilot Q&A."""

    question: str
    run_id: str | None = None


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"status": "healthy", "service": "Data Analysis Pipeline API"}


@app.get("/health")
async def health_check():
    """Detailed health check."""
    return {
        "status": "healthy",
        "openai_configured": bool(settings.OPENAI_API_KEY),
        "version": settings.API_VERSION,
    }


@app.post("/analyze")
async def analyze_data(
    file: UploadFile = File(...),
    analysis_type: str = Form("Quick Profile"),
    include_anomalies: bool = Form(True),
    include_insights: bool = Form(True),
    include_visualizations: bool = Form(True),
    include_report: bool = Form(True),
):
    """
    Upload and analyze data file.
    
    Accepts: CSV, JSON, XLSX, TXT
    Returns: Analysis results with insights, anomalies, and visualizations
    """
    try:
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")
        
        # Validate file extension
        file_ext = file.filename.split(".")[-1].lower()
        if file_ext not in settings.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type. Allowed: {settings.ALLOWED_EXTENSIONS}"
            )
        
        # Save uploaded file
        file_path = uploads_dir / file.filename
        contents = await file.read()
        
        if len(contents) > settings.MAX_FILE_SIZE_MB * 1024 * 1024:
            raise HTTPException(
                status_code=413,
                detail=f"File too large. Max: {settings.MAX_FILE_SIZE_MB}MB"
            )
        
        with open(file_path, "wb") as f:
            f.write(contents)
        
        logger.info(f"File uploaded: {file.filename}")
        
        options = {
            "analysis_type": analysis_type,
            "include_anomalies": include_anomalies,
            "include_insights": include_insights,
            "include_visualizations": include_visualizations,
            "include_report": include_report,
        }
        result = await run_analysis(
            str(file_path),
            file.filename,
            options=options,
        )
        saved_run = run_store.save_run(
            file_name=file.filename,
            file_path=str(file_path),
            options=options,
            result=result,
        )
        result["run_id"] = saved_run["run_id"]
        result["workspace_summary"] = saved_run["summary"]
        return JSONResponse(content=result)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/analyze-streaming")
async def analyze_data_streaming(file: UploadFile = File(...)):
    """
    Analyze data with streaming results (SSE).
    
    Returns: Server-sent events with real-time analysis progress
    """
    # TODO: Implement streaming analysis
    pass


@app.get("/runs")
async def list_runs():
    """List saved analysis runs."""
    runs = run_store.list_runs()
    return {
        "runs": [
            {
                "run_id": run["run_id"],
                "created_at": run["created_at"],
                "file_name": run["file_name"],
                "summary": run.get("summary", {}),
                "options": run.get("options", {}),
            }
            for run in runs
        ]
    }


@app.get("/runs/latest")
async def latest_run():
    """Return the most recent saved run."""
    run = run_store.latest_run()
    if not run:
        raise HTTPException(status_code=404, detail="No saved runs found")
    return run


@app.get("/runs/{run_id}")
async def get_run(run_id: str):
    """Fetch a saved run by id."""
    run = run_store.get_run(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    return run


@app.post("/copilot/ask")
async def ask_copilot(payload: CopilotQuestion):
    """Answer a question against a saved workspace run."""
    run = run_store.get_run(payload.run_id) if payload.run_id else run_store.latest_run()
    if not run:
        raise HTTPException(status_code=404, detail="No run available for copilot context")
    answer = copilot_agent.answer(payload.question, run)
    return {
        "run_id": run["run_id"],
        "file_name": run["file_name"],
        **answer,
    }


def run_server():
    """Run FastAPI server."""
    try:
        settings.validate()
        logger.info("Configuration validated successfully")
        logger.info(f"Starting API server on http://{settings.API_HOST}:{settings.API_PORT}")
        uvicorn.run(app, host=settings.API_HOST, port=settings.API_PORT)
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        raise


if __name__ == "__main__":
    run_server()
