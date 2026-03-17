"""Phase 2 testing: Data Profiler Agent - simplified."""

import sys
from pathlib import Path
from agents.profiler import DataProfilerAgent

def test_data_profiler():
    """Test the Data Profiler Agent."""
    print("=" * 70)
    print("Phase 2: Data Profiler Agent Test")
    print("=" * 70)
    
    sample_file = Path("data/samples/sales_data.csv")
    
    if not sample_file.exists():
        print(f"ERROR: Sample file not found: {sample_file}")
        print("Run: python create_samples.py")
        return False
    
    try:
        print(f"\nTesting Data Profiler Agent on: {sample_file.name}")
        print("-" * 70)
        
        agent = DataProfilerAgent()
        print("OK: Agent initialized")
        
        print("\nRunning analysis...\n")
        result = agent.run(str(sample_file))
        
        if result["status"] == "success":
            print("OK: Analysis completed successfully!\n")
            
            # Show summary
            summary = result.get("summary", "")
            print(summary)
            
            print("\n" + "=" * 70)
            print("SUCCESS: Phase 2 Test Passed!")
            print("=" * 70)
            return True
        else:
            error = result.get("error", "Unknown error")
            print(f"ERROR: Analysis failed: {error}")
            return False
    
    except Exception as e:
        print(f"ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_data_profiler()
    sys.exit(0 if success else 1)
