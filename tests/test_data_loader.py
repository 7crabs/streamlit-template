import pandas as pd
import pytest

from src.utils.data_loader import load_sample_data


def test_load_sample_data() -> None:
    """Test that the load_sample_data function returns the expected DataFrame"""
    # Load sample data with default seed
    data = load_sample_data()

    # Verify the structure of the DataFrame
    assert isinstance(data, pd.DataFrame)
    assert not data.empty
    assert "date" in data.columns
    assert "value" in data.columns
    assert "category" in data.columns

    # Verify the data types
    assert pd.api.types.is_datetime64_any_dtype(data["date"])
    assert pd.api.types.is_numeric_dtype(data["value"])
    assert pd.api.types.is_object_dtype(data["category"])

    # Verify the date range
    assert data["date"].min() == pd.Timestamp("2024-01-01")
    assert data["date"].max() == pd.Timestamp("2024-12-31")

    # Verify the categories
    assert set(data["category"].unique()) == {"A", "B", "C"}


def test_load_sample_data_reproducibility() -> None:
    """Test that the load_sample_data function produces reproducible results with the same seed"""
    # Load sample data twice with the same seed
    data1 = load_sample_data(seed=42)
    data2 = load_sample_data(seed=42)

    # Verify that the data is identical
    pd.testing.assert_frame_equal(data1, data2)

    # Load sample data with a different seed
    data3 = load_sample_data(seed=100)

    # Verify that the data is different
    with pytest.raises(AssertionError):
        pd.testing.assert_frame_equal(data1, data3)
