"""Phase 1 verification script."""

import sys
from pathlib import Path

def check_structure():
    """Verify project structure."""
    print("🔍 Checking project structure...")
    
    required_files = [
        "config.py",
        "logger.py",
        "main.py",
        "streamlit_app.py",
        "requirements.txt",
        ".env.example",
        "README.md",
        ".gitignore",
    ]
    
    required_dirs = [
        "agents",
        "tools",
        "graph",
        "data/uploads",
        "data/outputs",
        "data/samples",
        "tests",
    ]
    
    errors = []
    
    for file in required_files:
        if not Path(file).exists():
            errors.append(f"❌ Missing file: {file}")
        else:
            print(f"✅ {file}")
    
    for dir in required_dirs:
        if not Path(dir).exists():
            errors.append(f"❌ Missing directory: {dir}")
        else:
            print(f"✅ {dir}/")
    
    return errors


def check_config():
    """Verify configuration."""
    print("\n🔧 Checking configuration...")
    try:
        from config import settings
        print(f"✅ Config module loaded")
        print(f"  - API Title: {settings.API_TITLE}")
        print(f"  - Model: {settings.OPENAI_MODEL}")
        print(f"  - Debug: {settings.DEBUG}")
        
        # Check for API key
        if not settings.OPENAI_API_KEY:
            return ["⚠️  OPENAI_API_KEY not set (required for Phase 2+)"]
        return []
    except Exception as e:
        return [f"❌ Config error: {str(e)}"]


def check_imports():
    """Verify critical imports."""
    print("\n📦 Checking imports...")
    errors = []
    
    imports = [
        ("fastapi", "FastAPI"),
        ("streamlit", "Streamlit"),
        ("pandas", "Pandas"),
        ("langchain", "LangChain"),
        ("langgraph", "LangGraph"),
    ]
    
    for module, name in imports:
        try:
            __import__(module)
            print(f"✅ {name}")
        except ImportError:
            errors.append(f"❌ {name} not installed (run: pip install -r requirements.txt)")
    
    return errors


def main():
    """Run all checks."""
    print("=" * 60)
    print("Phase 1 Verification")
    print("=" * 60)
    
    all_errors = []
    
    # Check structure
    all_errors.extend(check_structure())
    
    # Check config
    all_errors.extend(check_config())
    
    # Check imports
    all_errors.extend(check_imports())
    
    # Report
    print("\n" + "=" * 60)
    if all_errors:
        print("⚠️  Issues found:")
        for error in all_errors:
            print(f"  {error}")
        print("\nNext steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Configure .env: cp .env.example .env && edit .env")
        print("3. Verify again: python verify_phase1.py")
        return 1
    else:
        print("✅ Phase 1 setup verified successfully!")
        print("\n📝 Next steps:")
        print("1. Verify imports work: pip install -r requirements.txt")
        print("2. Set up environment: cp .env.example .env")
        print("3. Add OpenAI API key to .env")
        print("4. Start Phase 2 (Data Profiler Agent)")
        return 0


if __name__ == "__main__":
    sys.exit(main())
