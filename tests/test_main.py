from streamlit.testing.v1 import AppTest


def test_main_function() -> None:
    """Test the main function using Streamlit's testing module"""
    # Initialize the app test
    at = AppTest.from_file("main.py").run()

    # Verify that the DataVizComponent is rendered
    # Check for the title that DataVizComponent renders
    assert at.title[0].value == "📊 Data Analysis Dashboard"

    # Verify that the sidebar contains the expected elements
    assert at.sidebar.header[0].value == "Data Filters"
    assert "Select Date Range" in at.sidebar.date_input[0].label
    assert "Select Categories" in at.sidebar.multiselect[0].label

    # Verify that the main content contains the expected headers
    assert at.header[0].value == "Summary Statistics"
    assert at.header[1].value == "Time Series Analysis"
    assert at.header[2].value == "Distribution Analysis"
    assert at.header[3].value == "Raw Data"
