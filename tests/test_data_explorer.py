from streamlit.testing.v1 import AppTest

from src.utils.data_loader import load_sample_data


def test_data_explorer_page() -> None:
    """Test the data explorer page using Streamlit's testing module"""
    # Initialize the app test
    at = AppTest.from_file("src/pages/01_data_explorer.py").run()

    # Verify that the title is rendered correctly
    assert at.title[0].value == "Data Explorer"

    # Verify that the sidebar contains the expected elements
    assert at.sidebar.header[0].value == "Filters"
    assert "Select Categories" in at.sidebar.multiselect[0].label
    assert "Value Range" in at.sidebar.slider[0].label

    # Verify that the main content contains the expected headers
    assert at.header[0].value == "Data Summary"
    assert at.header[1].value == "Data Visualization"
    assert at.header[2].value == "Data Table"

    # Verify that metrics are displayed
    assert len(at.metric) >= 4  # Number of Records, Average, Min, Max
    assert "Number of Records" in at.metric[0].label

    # Test interaction with category filter
    # Select only category A
    at.sidebar.multiselect[0].set_value(["A"]).run()

    # Verify that the metrics are updated
    sample_data = load_sample_data()
    category_a_count = len(sample_data[sample_data["category"] == "A"])
    assert int(at.metric[0].value) == category_a_count


def test_data_explorer_value_filter() -> None:
    """Test the value range filter in the data explorer page"""
    # Initialize the app test
    at = AppTest.from_file("src/pages/01_data_explorer.py").run()

    # Get the initial number of records
    initial_count = int(at.metric[0].value)

    # Set a narrower value range
    sample_data = load_sample_data()
    min_value = float(sample_data["value"].min())
    max_value = float(sample_data["value"].max())
    mid_value = (min_value + max_value) / 2

    # Set the slider to filter for values above the midpoint
    at.sidebar.slider[0].set_value((mid_value, max_value)).run()

    # Verify that the number of records has decreased
    filtered_count = int(at.metric[0].value)
    assert filtered_count < initial_count

    # Verify that the filtered data matches our expectation
    expected_count = len(sample_data[sample_data["value"] >= mid_value])
    assert filtered_count == expected_count
