"""
This is the Layout Creation Page
of the Data Story Authoring Tool

Author: Anonymous
"""

# streamlit packages
import streamlit as st
from st_click_detector import click_detector
from streamlit_extras.switch_page_button import switch_page
from streamlit_modal import Modal
from streamlit_extras.app_logo import add_logo
from streamlit_option_menu import option_menu
from streamlit.components.v1 import html

# dataframe handling
import pandas as pd  # read csv, df manipulation

# reusable functions, outsourced into another file
from helper_functions import GPTHelper

# other
import base64


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


def handle_pages_confirmed(number):
    # add the info, whether the button has been clicked
    st.session_state["num_pages_button_clicked"] = True
    st.session_state["num_pages_data_story"] = number


def main():
    """
    Main function for the Data Story Authoring Tool - Homepage.
    Returns:
        None
    """

    # call the style function to apply the styles
    style()

    # add page logo to sidebar
    with st.sidebar:
        add_logo("static/img/chi_logo.png", height=30)

    # create a container to place in sticky header content
    header = st.container()
    with header:
        # top page navigation bar
        choose = option_menu(
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
            menu_icon="app-indicator",
            default_index=2,
            key="layout-menu",
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
        if "exploration-menu" in st.session_state:
            del st.session_state["exploration-menu"]
        if "homepage-menu" in st.session_state:
            del st.session_state["homepage-menu"]
        if "visualization-menu" in st.session_state:
            del st.session_state["visualization-menu"]
        # handle the option that got chosen in the navigation bar
        if choose == "Data Exploration":
            switch_page("Exploratory Data Analysis")
        elif choose == "Homepage":
            switch_page("Homepage")
        elif choose == "Story Narration":
            switch_page("Create Visualizations")
        elif choose == "Data Story":
            switch_page("Data Story 1")
        st.write("""<div class='fixed-header'/>""", unsafe_allow_html=True)

    with st.sidebar:
        gpt_helper.feedback(page=choose)

    # page title
    st.title("Data Story Authoring Tool - Layout")

    # page instructions
    st.write(
        "This is the Layout Creation Page of the Story Authoring Tool. Here you will first\
             choose how many pages the data story will have. Then you will decide the layout\
              of the respective pages."
    )
    st.write("***")

    # how many pages should the data story have
    st.subheader("1️⃣Number of Pages")
    if "num_pages_data_story" in st.session_state:
        number = st.number_input(
            label="Choose the number of pages.",
            min_value=1,
            max_value=3,
            step=1,
            value=st.session_state["num_pages_data_story"],
            help="Choose the number of pages for your data story. This number can later still be\
                modified on the following page.",
        )
    else:
        number = st.number_input(
            label="Choose the number of pages.",
            min_value=1,
            max_value=3,
            step=1,
            value=1,
            help="Choose the number of pages for your data story. This number can later still be\
            modified on the following page.",
        )

    pages_confirmed_button = st.button(
        "Enter",
        key="pages_confirmed",
        on_click=handle_pages_confirmed,
        args=(number,),
    )

    if "num_pages_button_clicked" in st.session_state:
        # st.success(
        #     "The data story will have"
        #     f" {st.session_state['num_pages_data_story']} pages",
        #     icon="✅",
        # )

        st.subheader("2️⃣Choose the Layouts of the respective pages.")
        # style for an image that gets selected
        st.markdown(
            """<style>
                    .image-with-border {
                        border: 2px solid blue;
                        padding: 5px;
                    }
            </style>""",
            unsafe_allow_html=True,
        )
        # let the user choose the layout for each page --> add more layout
        # possibilities in the future create a counter variable to give the
        # layouts a dynamic key
        for page, counter in enumerate(
            range(st.session_state["num_pages_data_story"])
        ):
            # initialize with image one or previous session state
            if (
                f"page_layout_{counter}" not in st.session_state
                or st.session_state[f"page_layout_{counter}"] == None
            ):
                st.session_state[f"page_layout_{counter}"] = "Image 1"

            clicked = False
            st.write(f"Choose the Layout for page {page+1}:")
            images = []
            for file in [
                "./static/img/example_dashboard_1.png",
                "./static/img/example_dashboard_2.png",
            ]:
                with open(file, "rb") as image:
                    encoded = base64.b64encode(image.read()).decode()
                    images.append(f"data:image/png;base64,{encoded}")

            if st.session_state[f"page_layout_{counter}"] == "Image 1":
                content = (
                    """
                    <style>
                        .image-with-border {
                            border: 2px solid blue;
                            padding: 5px;
                        }
                    </style>
                """
                    + f"""
                    <a  id='Image 1'><img width='30%' src="{images[0]}" class="image-with-border"></a>
                    <a  id='Image 2'><img width='30%' src="{images[1]}"></a>
                    """
                )
                clicked = click_detector(content, key=f"page_layout_{counter}")
            elif st.session_state[f"page_layout_{counter}"] == "Image 2":
                content = (
                    """
                    <style>
                        .image-with-border {
                            border: 2px solid blue;
                            padding: 5px;
                        }
                    </style>
                """
                    + f"""
                    <a  id='Image 1'><img width='30%' src="{images[0]}"></a>
                    <a  id='Image 2'><img width='30%' src="{images[1]}" class="image-with-border"></a>
                    """
                )
                clicked = click_detector(content, key=f"page_layout_{counter}")

        layouts_confirmed_button = st.button(
            "Confirm Layout", key=f"layouts_confirmed"
        )
        if layouts_confirmed_button:
            # check whether all layouts have been chose
            for i in range(st.session_state["num_pages_data_story"]):
                st.session_state[
                    f"page_layout_{i}_entered"
                ] = st.session_state[f"page_layout_{i}"]
                assert st.session_state[f"page_layout_{i}"] != None
                if st.session_state[f"page_layout_{i}_entered"] == "Image 1":
                    # create the layouts
                    gpt_helper.create_story_layout_type_1(
                        file_name=f"pages/0{3+i}_data_story_{i+1}.py",
                        story_page=i + 1,
                    )
                elif st.session_state[f"page_layout_{i}_entered"] == "Image 2":
                    # create the layouts
                    gpt_helper.create_story_layout_type_2(
                        file_name=f"pages/0{3+i}_data_story_{i+1}.py",
                        story_page=i + 1,
                    )
            switch_page("create visualizations")
            # except Exception as e:
            #     st.write(e)
            #     modal = Modal(key="Demo Key", title="Oops", max_width=200)
            #     with modal.container():
            #         st.write(
            #             "Please select the Layouts for every page by clicking on an"
            #             " image in every row before continuing."
            #         )
            # st.write(st.session_state)


if __name__ == "__main__":
    main()
