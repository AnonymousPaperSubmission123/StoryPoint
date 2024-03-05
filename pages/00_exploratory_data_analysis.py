"""
This is the EDA page of the Data Story Authoring Tool

Author: Anonymous
"""

# streamlit packages
import streamlit as st
from streamlit_pandas_profiling import st_profile_report
from helper_functions import GPTHelper
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.app_logo import add_logo
from streamlit_option_menu import option_menu

# dataframe and EDA handling
import pandas as pd
from pandas_profiling import ProfileReport

# reusable functions, outsourced into another file
from helper_functions import GPTHelper

# multivision and threading
from multivision.multivision import Recommender

# threading
from threading import Thread
from streamlit.runtime.scriptrunner import add_script_run_ctx

# instanciate gptHelperFunctions
gpt_helper = GPTHelper()

# configure the page
st.set_page_config(
    page_title="Conversational Dashboard",
    page_icon="✅",
    layout="wide"
    # initial_sidebar_state="collapsed"
)
# feedback counter so that the form doesn't reopen on rerun
if not "feedback_counter" in st.session_state:
    st.session_state["feedback_counter"] = 0


def choose_dataset_handler(dataset, data_path):
    # add the chosen dataset to session state
    st.session_state["dataset"] = dataset

    # add the info, whether the button has been clicked
    st.session_state["data_set_chosen"] = True

    # get the graph recommendations within a background task
    # use the adjusted multivision paper package
    if f"multivision_specs_{dataset}" not in st.session_state:
        # the thread stores the created vega lite specifications in a
        # session state variable called multivision_specs_{dataset}
        recommender_thread = Recommender(
            num_rec=12, data_path=data_path, dataset=dataset
        )
        recommender_thread.run()


def style():
    """
    Apply custom styles to the page, remove sidebar elements, and add custom
    CSS for the sticky header.

    This function applies custom CSS styles to the page, including removing
    whitespace from the top of the page and sidebar.
    It defines CSS classes for styling specific elements, such as custom-div,
    block-container, blue-text, and normal-text.
    The function also hides the footer, removes the sidebar pages, and adds
    custom CSS for the sticky header.

    Returns:
        None
    """

    # Remove whitespace from the top of the page and sidebar
    st.markdown(
        """
            <style>
                .custom-div {
                    width: 30vw;
                    height: 280px;
                    overflow: hidden;
                    overflow-wrap: break-word;
                    }

                .block-container {
                        padding-top: 0vh;
                    }
                    .blue-text {
                    color: blue;
                    font-family: Arial, sans-serif;
                    font-size: 20px;
                    }

                    .normal-text {
                    color: black;
                    font-family: Arial, sans-serif;
                    font-size: 20px;
                        }
                footer{
                visibility:hidden;
                }

            </style>
            """,
        unsafe_allow_html=True,
    )

    # remove the sidebar pages
    no_sidebar_style = """
        <style>
            div[data-testid="stSidebarNav"] li {display: none;}
        </style>
    """
    # hide the sidebar
    st.markdown(no_sidebar_style, unsafe_allow_html=True)

    ### Custom CSS for the sticky header
    st.markdown(
        """
    <style>
        div[data-testid="stVerticalBlock"] div:has(div.fixed-header) {
            position: sticky;
            top: 2.875rem;
            background-color: white;
            z-index: 999;
        }
        .fixed-header {
        }
    </style>
        """,
        unsafe_allow_html=True,
    )

    # fonts for the website
    st.markdown(
        """<style>/* Font */
            @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
            /* You can replace 'Roboto' with any other font of your choice */

            /* Title */
            h1 {
            font-family: 'Roboto', sans-serif;
            font-size: 32px;
            font-weight: 700;
            padding-top:0px;
            }

            /* Chapter Header */
            h2 {
            font-family: 'Roboto', sans-serif;
            font-size: 24px;
            font-weight: 700;
            }

            /* Chapter Subheader */
            h3 {
            font-family: 'Roboto', sans-serif;
            font-size: 20px;
            font-weight: 700;
            }

            /* Normal Text */
            p {
            font-family: 'Roboto', sans-serif;
            font-size: 16px;
            font-weight: 400;
            }
            </style>""",
        unsafe_allow_html=True,
    )


def handle_dataset_selectbox():
    # delete, so that the pandas report must be reloaded
    if "data_set_chosen" in st.session_state:
        del st.session_state["data_set_chosen"]


def main():
    """
    Main function for the Data Story Authoring Tool - EDA.
    Renders the code for the EDA. Includes the automatic
    pandas profiling EDA creation package.
    """

    # call the style function to apply the styles
    style()


    # create a container to place in sticky header content
    header = st.container()
    with header:
        # top page navigation bar
        choose_exploration = option_menu(
            "StoryPoint",
            [
                "Homepage",
                "Data Exploration",
                "Story Composition",
                "Story Narration",
                "Data Story",
            ],
            icons=[
                "house",
                "clipboard-data",
                "list-check",
                "bar-chart",
                "award",
                "send-check",
            ],
            key="exploration-menu",
            menu_icon="app-indicator",
            default_index=1,
            orientation="horizontal",
            styles={
                "container": {
                    "padding": "0!important",
                    "background-color": "#FFFFFF",
                },
                "icon": {"color": "orange", "font-size": "16px"},
                "nav-link": {
                    "font-size": "16px",
                    "text-align": "left",
                    "margin": "0px",
                    "--hover-color": "#eee",
                },
                "nav-link-selected": {"background-color": "#1A84C7"},
            },
        )
        # delete the other session states so when we navigate back to the respective pages, we dont get endless loops
        if "story-menu" in st.session_state:
            del st.session_state["story-menu"]
        if "homepage-menu" in st.session_state:
            del st.session_state["homepage-menu"]
        if "layout-menu" in st.session_state:
            del st.session_state["layout-menu"]
        if "visualization-menu" in st.session_state:
            del st.session_state["visualization-menu"]
        # handle the option that got chosen in the navigation bar
        elif choose_exploration == "Story Composition":
            switch_page("Layout Creation")
        elif choose_exploration == "Story Narration":
            switch_page("Create Visualizations")
        elif choose_exploration == "Data Story":
            switch_page("Data Story 1")
        elif choose_exploration == "Homepage":
            switch_page("Homepage")
        st.write("""<div class='fixed-header'/>""", unsafe_allow_html=True)

    with st.sidebar:
        gpt_helper.feedback(page=choose_exploration)
    # page title
    st.title("Data Story Authoring Tool - EDA")

    # page instructions
    st.write(
        "This is the Exploratory Data Analysis Page of the Story Authoring Tool. \
             You can choose and view your favourite dataset from the dropdown menu. \
             After selecting the data that you want to work with, you can use the automatically\
             generated Exploratory Data Analysis to get familiar with the data and to get inspiration \
             for the plots that you later generate for your data story."
    )
    st.write("***")

    # which dataset are we going to use
    st.subheader("1️⃣Choose a Dataset")

    # so we have the right dataset preselected
    if "dataset" in st.session_state:
        # choose dataset option
        dataset = st.selectbox(
            label="Dataset",
            options=[
                "🎥 IMDB Movies",
                "💶 Salaries",
                "📈 Superstore Sales",
                "😷 Covid Worldwide",
                "🗣️ Amazon Customer Behaviour",
                "🧺 Food Prices",
                "🛌 Sleep, Health and Lifestyle",
                "🎵 Spotify Song Attributes",
            ],
            index=st.session_state["dataset_index"],
            on_change=handle_dataset_selectbox,
        )
    else:
        # choose dataset option
        dataset = st.selectbox(
            label="Dataset",
            options=[
                "🎥 IMDB Movies",
                "💶 Salaries",
                "📈 Superstore Sales",
                "😷 Covid Worldwide",
                "🗣️ Amazon Customer Behaviour",
                "🧺 Food Prices",
                "🛌 Sleep, Health and Lifestyle",
                "🎵 Spotify Song Attributes",
            ],
            on_change=handle_dataset_selectbox,
        )
    # display the dataset and its properties in the sidebar on this and on coming pages -->
    # show the datatype of the attributes
    # select attributes to use as a filter?!
    if dataset == "💶 Salaries":
        data_path = "data/ds_salaries.csv"
        df = pd.read_csv(data_path)
        st.session_state["dataset_index"] = 1
    elif dataset == "🎥 IMDB Movies":
        data_path = "data/imdb_top_1000.csv"
        df = pd.read_csv(data_path)
        st.session_state["dataset_index"] = 0
    elif dataset == "📈 Superstore Sales":
        data_path = "data/superstore.csv"
        df = pd.read_csv(data_path, encoding="windows-1252")
        st.session_state["dataset_index"] = 2
    elif dataset == "😷 Covid Worldwide":
        data_path = "data/covid_worldwide.csv"
        df = pd.read_csv(data_path)
        st.session_state["dataset_index"] = 3
    elif dataset == "🗣️ Amazon Customer Behaviour":
        data_path = "data/Amazon Customer Behavior Survey.csv"
        df = pd.read_csv(data_path)
        st.session_state["dataset_index"] = 4
    elif dataset == "🧺 Food Prices":
        data_path = "data/Food Prices.csv"
        df = pd.read_csv(data_path)
        st.session_state["dataset_index"] = 5
    elif dataset == "🛌 Sleep, Health and Lifestyle":
        data_path = "data/Sleep_health_and_lifestyle_dataset.csv"
        df = pd.read_csv(data_path)
        st.session_state["dataset_index"] = 6
    elif dataset == "🎵 Spotify Song Attributes":
        data_path = "data/Spotify_Song_Attributes.csv"
        df = pd.read_csv(data_path)
        st.session_state["dataset_index"] = 7

    # Apply the custom function and convert date columns
    for col in df.columns:
        # check if a column name contains date substring
        if "date" in col.lower():
            df[col] = pd.to_datetime(df[col])
            # remove timestamp
            # df[col] = df[col].dt.date
    # reset index
    df = df.reset_index(drop=True)

    # replace space with _ in column names
    cols = df.columns
    cols = ", ".join(cols)

    # display the dataframe with pagination
    # Number of entries per screen
    N = 5

    # A variable to keep track of which product we are currently displaying
    if "df_page_number" not in st.session_state:
        st.session_state["df_page_number"] = 0

    last_page = len(df) // N

    # Add a next button and a previous button
    df_placeholder = st.container()
    prev, _, next = st.columns([1, 8, 1])
    if next.button("Next"):
        if st.session_state["df_page_number"] + 1 > last_page:
            st.session_state["df_page_number"] = 0
        else:
            st.session_state["df_page_number"] += 1

    if prev.button("Previous"):
        if st.session_state["df_page_number"] - 1 < 0:
            st.session_state["df_page_number"] = last_page
        else:
            st.session_state["df_page_number"] -= 1

    # Get start and end indices of the next page of the dataframe
    start_idx = st.session_state["df_page_number"] * N
    end_idx = (1 + st.session_state["df_page_number"]) * N

    # Index into the sub dataframe
    sub_df = df.iloc[start_idx:end_idx]
    df_placeholder.dataframe(sub_df)

    choose_dataset = st.button(
        "Choose Dataset",
        key="dataset_confirmed",
        on_click=choose_dataset_handler,
        args=(dataset, data_path),
    )

    # when the dataset chosen button is clicked, we generate an automatic eda with
    # pandas profiling
    if "data_set_chosen" in st.session_state:
        # notify user that dataframe has been chosen succesfully
        st.success(f"You have chosen the {dataset} dataset", icon="✅")
        # how many pages should the data story have
        st.subheader("2️⃣Explore the Data")

        # cache the report so it doesnt reload when a button is clicked
        @st.cache_resource()
        def get_dataset_profile_report(df):
            return df.profile_report()

        # display the eda report
        profile = get_dataset_profile_report(df)
        st_profile_report(profile)

        eda_finished = st.button("EDA finished")
        if eda_finished:
            # check whether all layouts have been chose
            switch_page("layout creation")


if __name__ == "__main__":
    main()
