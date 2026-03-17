"""Generate sample datasets for testing."""

import pandas as pd
import numpy as np
from pathlib import Path

def create_sales_dataset():
    """Create a sample sales dataset."""
    np.random.seed(42)
    
    dates = pd.date_range('2023-01-01', periods=1000, freq='D')
    regions = np.random.choice(['North', 'South', 'East', 'West'], 1000)
    product = np.random.choice(['Product A', 'Product B', 'Product C', 'Product D'], 1000)
    
    # Quantity with some missing values
    quantity = np.random.randint(1, 100, 1000).astype(float)
    quantity[np.random.choice(1000, 50, replace=False)] = np.nan
    
    # Price with some missing values
    price = np.random.uniform(10, 500, 1000)
    price[np.random.choice(1000, 30, replace=False)] = np.nan
    
    # Sales = quantity * price with some noise
    sales = quantity * price + np.random.normal(0, 100, 1000)
    
    df = pd.DataFrame({
        'date': dates,
        'region': regions,
        'product': product,
        'quantity': quantity,
        'price': price,
        'sales': sales,
    })
    
    return df

def create_customer_dataset():
    """Create a sample customer dataset."""
    np.random.seed(42)
    
    n = 500
    age = np.random.randint(18, 80, n).astype(float)
    age[np.random.choice(n, 20)] = np.nan
    
    df = pd.DataFrame({
        'customer_id': range(1, n+1),
        'age': age,
        'income': np.random.randint(20000, 200000, n),
        'purchase_count': np.random.randint(0, 100, n),
        'customer_tenure_months': np.random.randint(0, 120, n),
        'status': np.random.choice(['Active', 'Inactive', 'Churned'], n),
    })
    
    # Add duplicates
    df = pd.concat([df, df.iloc[:10]], ignore_index=True)
    
    return df

if __name__ == "__main__":
    # Create sample directory
    sample_dir = Path("data/samples")
    sample_dir.mkdir(parents=True, exist_ok=True)
    
    # Create and save datasets
    sales_df = create_sales_dataset()
    sales_df.to_csv(sample_dir / "sales_data.csv", index=False)
    print(f"✓ Created sales_data.csv ({sales_df.shape[0]} rows)")
    
    customer_df = create_customer_dataset()
    customer_df.to_csv(sample_dir / "customer_data.csv", index=False)
    print(f"✓ Created customer_data.csv ({customer_df.shape[0]} rows)")
