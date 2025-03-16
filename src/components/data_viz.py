from datetime import date

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st


class DataVizComponent:
    """Component for basic data visualization and analysis"""

    def __init__(self):
        """Initialize the component with sample data"""
        # Generate sample data
        np.random.seed(42)
        dates = pd.date_range(start="2024-01-01", end="2024-12-31", freq="D")
        values = np.random.normal(loc=100, scale=15, size=len(dates))
        seasonal = 20 * np.sin(2 * np.pi * np.arange(len(dates)) / 365)

        self.data = pd.DataFrame(
            {
                "date": dates,
                "value": values + seasonal,
                "category": np.random.choice(["A", "B", "C"], size=len(dates)),
            }
        )

    def plot_time_series(self, data: pd.DataFrame) -> None:
        """Create a time series plot"""
        fig = px.line(
            data,
            x="date",
            y="value",
            title="Time Series Analysis",
            labels={"date": "Date", "value": "Value"},
        )
        st.plotly_chart(fig, use_container_width=True)

    def plot_distribution(self, data: pd.DataFrame) -> None:
        """Create a distribution plot"""
        fig = px.histogram(
            data,
            x="value",
            color="category",
            title="Value Distribution by Category",
            labels={"value": "Value", "count": "Frequency"},
        )
        st.plotly_chart(fig, use_container_width=True)

    def calculate_statistics(self, data: pd.DataFrame) -> pd.DataFrame:
        """Calculate basic statistics by category"""
        # 明示的にDataFrameを返すようにする
        result = pd.DataFrame(
            data.groupby("category")["value"]
            .agg(
                Mean="mean",
                Median="median",
                StdDev="std",
                Min="min",
                Max="max",
            )
            .round(2)
        )
        return result

    def render(self) -> None:
        """Render the data visualization interface"""
        st.title("📊 Data Analysis Dashboard")

        # Sidebar controls
        st.sidebar.header("Data Filters")

        # Date range selector
        start_date = self.data["date"].dt.date.min()
        end_date = self.data["date"].dt.date.max()

        # date_inputの戻り値を適切に処理
        date_input_result = st.sidebar.date_input(
            "Select Date Range",
            value=(start_date, end_date),
            min_value=start_date,
            max_value=end_date,
        )

        # date_inputの戻り値を安全に処理
        if isinstance(date_input_result, date):
            # 単一の日付が選択された場合
            start_date_selected = date_input_result
            end_date_selected = date_input_result
        else:
            # 日付範囲が選択された場合
            if len(date_input_result) >= 2:
                start_date_selected = date_input_result[0]
                end_date_selected = date_input_result[1]
            else:
                # 予期しない場合のフォールバック
                start_date_selected = start_date
                end_date_selected = end_date

        # Category selector
        all_categories = sorted(self.data["category"].unique())
        categories = st.sidebar.multiselect(
            "Select Categories",
            options=all_categories,
            default=all_categories,
        )

        # Filter data based on user selection
        mask = (
            (self.data["date"].dt.date >= start_date_selected)
            & (self.data["date"].dt.date <= end_date_selected)
            & (self.data["category"].isin(categories))
        )
        # 明示的にDataFrameとして扱う
        filtered_data = pd.DataFrame(self.data[mask].copy())

        # Display basic statistics
        st.header("Summary Statistics")
        stats_df = self.calculate_statistics(filtered_data)
        st.dataframe(stats_df, use_container_width=True)

        # Display visualizations
        st.header("Time Series Analysis")
        self.plot_time_series(filtered_data)

        st.header("Distribution Analysis")
        self.plot_distribution(filtered_data)

        # Display raw data
        st.header("Raw Data")
        display_data = pd.DataFrame(filtered_data.sort_values("date", ascending=False))
        st.dataframe(display_data, use_container_width=True)
