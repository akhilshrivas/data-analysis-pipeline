"""Phase 2 testing: Data Profiler Agent."""

import sys
from pathlib import Path
from agents.profiler import DataProfilerAgent

def test_data_profiler():
    """Test the Data Profiler Agent."""
    print("=" * 70)
    print("Phase 2: Data Profiler Agent Test")
    print("=" * 70)
    
    # Sample file
    sample_file = Path("data/samples/sales_data.csv")
    
    if not sample_file.exists():
        print(f"❌ Sample file not found: {sample_file}")
        print("Run: python create_samples.py")
        return False
    
    try:
        print(f"\n📊 Testing Data Profiler Agent on: {sample_file.name}")
        print("-" * 70)
        
        # Initialize agent
        agent = DataProfilerAgent()
        print("✓ Agent initialized")
        
        # Run profiler
        print("\n🔍 Running analysis (this may take a moment)...\n")
        result = agent.run(str(sample_file))
        
        # Display results
        if result["status"] == "success":
            print("✓ Analysis completed successfully!\n")
            
            profile = result.get("profile", {})
            
            # Data shape
            shape = profile.get("shape", {})
            print(f"📈 Data Shape: {shape.get('rows', 'N/A'):,} rows × {shape.get('columns', 'N/A')} columns")
            
            # Columns
            columns = profile.get("columns", [])
            print(f"📋 Columns: {', '.join(columns)}")
            
            # Missing values
            missing = profile.get("missing_percentage", {})
            if missing:
                print(f"\n⚠️  Missing Values:")
                for col, pct in missing.items():
                    if pct > 0:
                        print(f"   - {col}: {pct:.1f}%")
            
            # Data types
            dtypes = profile.get("dtypes", {})
            print(f"\n🔤 Data Types:")
            for col, dtype in list(dtypes.items())[:3]:
                print(f"   - {col}: {dtype}")
            if len(dtypes) > 3:
                print(f"   ... and {len(dtypes) - 3} more columns")
            
            # Numeric statistics
            numeric_stats = profile.get("numeric_statistics", {})
            if numeric_stats:
                print(f"\n📊 Numeric Statistics (sample):")
                for col in list(numeric_stats.keys())[:2]:
                    stats = numeric_stats[col]
                    mean_val = stats.get('mean')
                    std_val = stats.get('std')
                    mean_str = f"{mean_val:.2f}" if mean_val is not None else "N/A"
                    std_str = f"{std_val:.2f}" if std_val is not None else "N/A"
                    print(f"   {col}:")
                    print(f"      Mean: {mean_str}")
                    print(f"      Std Dev: {std_str}")
            
            # Agent summary
            summary = result.get("agent_summary", "")
            if summary:
                print(f"\n🤖 Agent Analysis Summary:")
                print(summary[:300] + "..." if len(summary) > 300 else summary)
            
            print("\n" + "=" * 70)
            print("✅ Phase 2 Test Passed!")
            print("=" * 70)
            return True
        else:
            error = result.get("error", "Unknown error")
            print(f"❌ Analysis failed: {error}")
            return False
    
    except Exception as e:
        print(f"❌ Error during test: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_data_profiler()
    sys.exit(0 if success else 1)
