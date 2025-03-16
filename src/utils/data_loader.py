import numpy as np
import pandas as pd


def load_sample_data(seed: int | None = 42) -> pd.DataFrame:
    """
    Load a sample dataset for testing and demonstration purposes.

    Args:
        seed: Random seed for reproducibility

    Returns:
        DataFrame with sample data containing date, value, and category columns
    """
    # Set random seed for reproducibility
    np.random.seed(seed)

    # Generate sample data
    dates = pd.date_range(start="2024-01-01", end="2024-12-31", freq="D")
    values = np.random.normal(loc=100, scale=15, size=len(dates))
    seasonal = 20 * np.sin(2 * np.pi * np.arange(len(dates)) / 365)

    # Create DataFrame
    data = pd.DataFrame(
        {
            "date": dates,
            "value": values + seasonal,
            "category": np.random.choice(["A", "B", "C"], size=len(dates)),
        }
    )

    return data
