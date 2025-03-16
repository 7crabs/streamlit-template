import pandas as pd
import pytest
from pytest_mock import MockerFixture
from streamlit.testing.v1 import AppTest

from src.components.data_viz import DataVizComponent


class TestDataVizComponent:
    """Test suite for DataVizComponent class"""

    @pytest.fixture
    def data_viz_component(self) -> DataVizComponent:
        """Fixture to create a DataVizComponent instance for testing"""
        return DataVizComponent()

    @pytest.fixture
    def sample_dataframe(self) -> pd.DataFrame:
        """Fixture to create a sample DataFrame for testing"""
        return pd.DataFrame(
            {
                "date": pd.date_range(start="2024-01-01", end="2024-01-10"),
                "value": [100, 110, 95, 105, 115, 90, 100, 110, 105, 95],
                "category": ["A", "B", "A", "C", "B", "A", "C", "B", "A", "C"],
            }
        )

    def test_init(self, data_viz_component: DataVizComponent) -> None:
        """Test that the component initializes with sample data"""
        assert isinstance(data_viz_component.data, pd.DataFrame)
        assert not data_viz_component.data.empty
        assert "date" in data_viz_component.data.columns
        assert "value" in data_viz_component.data.columns
        assert "category" in data_viz_component.data.columns

    def test_calculate_statistics(
        self, data_viz_component: DataVizComponent, sample_dataframe: pd.DataFrame
    ) -> None:
        """Test the calculate_statistics method"""
        result = data_viz_component.calculate_statistics(sample_dataframe)

        # Create expected result
        expected = pd.DataFrame(
            {
                "Mean": [97.5, 111.67, 100],
                "Median": [97.5, 110.0, 100],
                "StdDev": [6.45, 2.89, 5.00],
                "Min": [90, 110, 95],
                "Max": [105, 115, 105],
            },
            index=pd.Index(["A", "B", "C"], name="category"),
        )

        # Compare with rounding to handle floating point precision
        pd.testing.assert_frame_equal(
            result.round(2), expected.round(2), check_exact=False
        )

    def test_plot_time_series(
        self,
        data_viz_component: DataVizComponent,
        sample_dataframe: pd.DataFrame,
        mocker: MockerFixture,
    ) -> None:
        """Test the plot_time_series method"""
        # Mock streamlit's plotly_chart
        mock_plotly_chart = mocker.patch("streamlit.plotly_chart")

        # Execute the method
        data_viz_component.plot_time_series(sample_dataframe)

        # Verify plotly_chart was called
        mock_plotly_chart.assert_called_once()

    def test_plot_distribution(
        self,
        data_viz_component: DataVizComponent,
        sample_dataframe: pd.DataFrame,
        mocker: MockerFixture,
    ) -> None:
        """Test the plot_distribution method"""
        # Mock streamlit's plotly_chart
        mock_plotly_chart = mocker.patch("streamlit.plotly_chart")

        # Execute the method
        data_viz_component.plot_distribution(sample_dataframe)

        # Verify plotly_chart was called
        mock_plotly_chart.assert_called_once()

    def test_render(
        self, data_viz_component: DataVizComponent, mocker: MockerFixture
    ) -> None:
        """Test the render method"""
        # Mock various streamlit methods
        mocker.patch("streamlit.title")
        mocker.patch("streamlit.sidebar.header")
        mocker.patch(
            "streamlit.sidebar.date_input",
            return_value=(
                pd.Timestamp("2024-01-01").date(),
                pd.Timestamp("2024-12-31").date(),
            ),
        )
        mocker.patch("streamlit.sidebar.multiselect", return_value=["A", "B", "C"])
        mocker.patch("streamlit.header")
        mocker.patch("streamlit.dataframe")
        mock_plot_time_series = mocker.patch.object(
            data_viz_component, "plot_time_series"
        )
        mock_plot_distribution = mocker.patch.object(
            data_viz_component, "plot_distribution"
        )

        # Execute the method
        data_viz_component.render()

        # Verify methods were called
        mock_plot_time_series.assert_called_once()
        mock_plot_distribution.assert_called_once()


def test_data_viz_component_integration() -> None:
    """Integration test for DataVizComponent using Streamlit's testing module"""
    # Create a simple test app that uses the DataVizComponent
    test_app_code = """
import streamlit as st
from src.components.data_viz import DataVizComponent

def main():
    st.set_page_config(
        page_title="Test Dashboard", page_icon="📊", layout="wide"
    )
    
    viz_app = DataVizComponent()
    viz_app.render()

if __name__ == "__main__":
    main()

main()
"""

    # Initialize and run the test app
    at = AppTest.from_string(test_app_code).run()

    # Verify that the title is rendered correctly
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

    # Verify that dataframes are rendered
    assert len(at.dataframe) >= 2  # At least 2 dataframes (stats and raw data)

    # Test interaction with category filter
    # Select only category A
    at.sidebar.multiselect[0].set_value(["A"]).run()

    # Verify that the dataframes are updated
    # This is a basic check - in a real test you might want to verify the actual data
    assert len(at.dataframe) >= 2
