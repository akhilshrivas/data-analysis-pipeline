import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """Application settings from environment variables."""
    
    # OpenAI Config
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4")
    
    # FastAPI Config
    API_TITLE: str = "Data Analysis Pipeline API"
    API_VERSION: str = "0.1.0"
    API_DESCRIPTION: str = "Advanced autonomous data analysis with LangChain & LangGraph"
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8010"))
    
    # Database Config
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./analysis.db")
    
    # Vector DB Config (Pinecone)
    PINECONE_API_KEY: str = os.getenv("PINECONE_API_KEY", "")
    PINECONE_INDEX: str = os.getenv("PINECONE_INDEX", "analysis-patterns")
    
    # Data Config
    MAX_FILE_SIZE_MB: int = int(os.getenv("MAX_FILE_SIZE_MB", "1024"))
    ALLOWED_EXTENSIONS: list = ["csv", "json", "xlsx"]
    
    # Analysis Config
    ANALYSIS_TIMEOUT_SECONDS: int = 300
    CHUNK_SIZE: int = 10000
    OUTPUTS_DIR: str = os.getenv("OUTPUTS_DIR", "data/outputs")
    RUNS_DIR: str = os.getenv("RUNS_DIR", "data/runs")
    DATA_PIPELINE_API_URL: str = os.getenv("DATA_PIPELINE_API_URL", "http://localhost:8010")
    
    def validate(self):
        """Validate required settings."""
        if not self.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY environment variable is required")

settings = Settings()
