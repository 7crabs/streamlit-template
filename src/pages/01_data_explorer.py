import plotly.express as px
import streamlit as st

from src.utils.data_loader import load_sample_data


def main():
    st.title("Data Explorer")

    # Load sample data
    data = load_sample_data()

    # Sidebar filters
    st.sidebar.header("Filters")

    # Category filter
    categories = sorted(data["category"].unique())
    selected_categories = st.sidebar.multiselect(
        "Select Categories",
        options=categories,
        default=categories,
    )

    # Value range filter
    min_value = float(data["value"].min())
    max_value = float(data["value"].max())
    value_range = st.sidebar.slider(
        "Value Range",
        min_value=min_value,
        max_value=max_value,
        value=(min_value, max_value),
    )

    # Apply filters
    filtered_data = data[
        (data["category"].isin(selected_categories))
        & (data["value"] >= value_range[0])
        & (data["value"] <= value_range[1])
    ]

    # Display data summary
    st.header("Data Summary")
    st.metric("Number of Records", len(filtered_data))

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Average Value", f"{filtered_data['value'].mean():.2f}")
    with col2:
        st.metric("Minimum Value", f"{filtered_data['value'].min():.2f}")
    with col3:
        st.metric("Maximum Value", f"{filtered_data['value'].max():.2f}")

    # Display scatter plot
    st.header("Data Visualization")
    fig = px.scatter(
        filtered_data,
        x="date",
        y="value",
        color="category",
        title="Value by Date and Category",
    )
    st.plotly_chart(fig, use_container_width=True)

    # Display data table
    st.header("Data Table")
    st.dataframe(filtered_data, use_container_width=True)


if __name__ == "__main__":
    main()

main()
