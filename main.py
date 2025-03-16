import streamlit as st

from src.components.data_viz import DataVizComponent


def main():
    st.set_page_config(
        page_title="Data Analysis Dashboard", page_icon="📊", layout="wide"
    )

    viz_app = DataVizComponent()
    viz_app.render()


if __name__ == "__main__":
    main()
