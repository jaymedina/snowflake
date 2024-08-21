import os

import numpy as np
import streamlit as st
from toolkit.queries import (
    query_annual_project_downloads,
    query_annual_unique_users,
    query_annual_downloads,
    query_annual_cost,
    query_monthly_download_trends,
    query_top_annotations,
    query_entity_distribution,
    dummy_get_download_access
)
from toolkit.utils import get_data_from_snowflake
from toolkit.widgets import plot_download_sizes, plot_unique_users_trend

# Configure the layout of the Streamlit app page
st.set_page_config(layout="wide",
                   page_title="Program Analytics",
                   page_icon=":bar_chart:",
                   initial_sidebar_state="expanded")

# Custom CSS for styling
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Setting up the sidebar and interactive user interface
with st.sidebar:
    # Load the sage logo
    logo_path = f"{os.path.dirname(__file__)}/resources/sage-bio-logo.png"

    # Display the sage logo
    st.sidebar.image(logo_path, use_column_width=True)
    st.title("Sage Internal Data Catalog")
    
    program_list = ["HTAN", "NF"]
    selected_program = st.selectbox("Select a program to view metrics for...", program_list)

    year_list = [2024, 2023, 2022]
    selected_year = st.selectbox("Select a year to view metrics for...", year_list)

    if selected_program == "HTAN":
        program_id = 20446927
    elif selected_program == "NF":
        program_id = 16858331

    st.write("For questions or comments, please contact jenny.medina@sagebase.org.")

def main(selected_year, program_id):

    # center_col, side_col = st.columns((4., 2), gap='medium')

    with st.expander("**README** :book:"):
        st.write("""
        - This Streamlit app displays metrics showing data usage, governance statistics, data impact in the form of citations, and human records
      supporting the data over the course of a year for a given DCC.
    - Several of the widgets in this app were created with dummy data for the sake of demonstration. These widgets are:
        - The download access dataframe in the **Data Usage** and governance section
        - The **Data Impact** section
        - The **About the Data** section
        - The overview cards corresponding to the last two sections
    
                 
        The rest was pulled in from Snowflake and represents real-time data for the given DCC.
    - This application is designed to be interactive to help with analysis. Here are some ways you can interact with the widgets:
        - Use the dropdown menus on the sidebar to select a program and year.
        - Hover over the charts to see tooltips and more information about the project.
        - Click on the legend to filter the line chart.
        - Click the columns in the dataframes to sort the rows according to your preference.
        - Drag the edges of the columns in the dataframes to adjust their width.
        """)

    # with center_col:
    # --------------- Row 1: Overview Cards -------------------------

    st.markdown("## Overview")

    # Data retrieval:
    annual_project_downloads_df = get_data_from_snowflake(query_annual_project_downloads(selected_year, program_id))
    annual_unique_users_df = get_data_from_snowflake(query_annual_unique_users(selected_year, program_id))
    annual_downloads_df = get_data_from_snowflake(query_annual_downloads(selected_year, program_id))
    annual_cost_df = get_data_from_snowflake(query_annual_cost(program_id))

    # Data transformation:
    total_data_size = round(sum(annual_project_downloads_df['TOTAL_PROJECT_SIZE_IN_TIB']), 2)

    # Data visualization:
    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
    col1.metric("Total Storage Occupied", f"{total_data_size} TiB")
    col2.metric("Annual Unique Users", f"{annual_unique_users_df['ANNUAL_UNIQUE_USERS'][0]}")
    col3.metric("Annual Downloads", f"{round(annual_downloads_df['ANNUAL_DOWNLOADS_IN_TIB'][0], 2)} TiB")
    col4.metric("Num. of Citations", "1265")
    col5.metric("Num. of Records", "7813")

    # ---------------- Row 3: Unique Users Trends -------------------------
    
    st.markdown("## Data Usage & Governance")
    
    row1_1, row1_2 = st.columns([1.7,1])

    with row1_1:
        # Data retrieval:
        unique_users_df = get_data_from_snowflake(query_monthly_download_trends(selected_year, program_id))
        
        # Data visualization:
        st.plotly_chart(plot_unique_users_trend(unique_users_df))
    with row1_2:
        # Data retrieval:
        top_annotations_df = get_data_from_snowflake(query_top_annotations(selected_year, program_id))

        # Data visualization:
        st.dataframe(top_annotations_df,
                 column_order=("COMPONENT_NAME", "OCCURRENCES", "NUMBER_OF_UNIQUE_DOWNLOADS"),
                 hide_index=True,
                 width=None,
                 column_config={
                    "COMPONENT_NAME": st.column_config.TextColumn(
                        "Annotation Component",
                    ),
                    "OCCURRENCES": st.column_config.ProgressColumn(
                        "Occurence",
                        format="%f",
                        min_value=0,
                        max_value=max(top_annotations_df["OCCURRENCES"]),
                     ),
                    "NUMBER_OF_UNIQUE_DOWNLOADS": st.column_config.ProgressColumn(
                        "Unique Downloads",
                        format="%f",
                        min_value=0,
                        max_value=max(top_annotations_df["NUMBER_OF_UNIQUE_DOWNLOADS"]),
                     )}
                 )

    # --------------- Row 2: Project Sizes and Downloads -----------------

    row2_1, row2_2 = st.columns([1.7,1])
    with row2_1:
        # Data visualization:
        st.plotly_chart(plot_download_sizes(annual_project_downloads_df))

        
    with row2_2:
        # --------------- Row 2: Entity Distribution -------------------------
        print(annual_project_downloads_df)
        download_access_df = dummy_get_download_access(annual_project_downloads_df["PROJECT_ID"], annual_project_downloads_df["NAME"])

        st.dataframe(download_access_df,
                     hide_index=True,
                     width=600,
                     column_config={
                        "PROJECT_ID": st.column_config.TextColumn(
                            "Project ID",
                        ),
                        "NAME": st.column_config.TextColumn(
                            "Project Name"
                        ),
                        "DOWNLOAD_ACCESS_COUNT": st.column_config.TextColumn(
                            "Users with Download Access",
                        ),}
                     )
        

    st.markdown("## Data Impact")
    st.markdown("## About The Data")


if __name__ == "__main__":
    main(selected_year, program_id)
