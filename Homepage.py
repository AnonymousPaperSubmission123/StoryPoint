"""
This is the Homepage of the Data Story Authoring Tool

Author: Anonymous

The `style` function in this code snippet is responsible for applying custom
CSS styles to the page and removing specific
elements from the sidebar. It provides a visually appealing and consistent 
layout for the Data Story Authoring Tool's
homepage.

The function begins by removing whitespace from the top of the page and
sidebar. It sets up CSS styles for various
elements, such as `h1`, `.custom-div`, `.block-container`, `.blue-text`
, and `.normal-text`, allowing for customized
appearance and formatting.

Next, the function hides the footer by setting its visibility to 'hidden'.
It also removes the sidebar pages by using
CSS selectors to hide the list items within the sidebar.

Additionally, the function adds custom CSS for a sticky header, ensuring 
that it remains fixed at the top of the page
while scrolling. This CSS is applied to specific div elements and defines 
their position, background color, and z-index.

Overall, the `style` function enhances the visual presentation and user 
experience of the Data Story Authoring Tool's
homepage.
"""

# streamlit packages
import streamlit as st
from streamlit_extras.badges import badge  # for git
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.app_logo import add_logo
from streamlit_option_menu import option_menu
from streamlit.components.v1 import html

# for deployment
import path
import sys

# dataframe handling
import pandas as pd  # read csv, df manipulation

# reusable functions, outsourced into another file
from helper_functions import GPTHelper

# instanciate gptHelperFunctions
gpt_helper = GPTHelper()


# set the path in deployment
dir = path.Path(__file__).abspath()
sys.path.append(dir.parent.parent)

# configure the page
st.set_page_config(
    page_title="Conversational Dashboard",
    page_icon="✅",
    layout="wide",
    initial_sidebar_state="expanded",
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
            .bold {
            font-weight: bold;
            }
            </style>""",
        unsafe_allow_html=True,
    )


def main():
    """
    Main function for the Data Story Authoring Tool - Homepage.

    This function sets up the sidebar, navigation bar, page title, and content
    for the homepage of the Data Story Authoring Tool.
    It includes the functionality to add a page logo to the sidebar, provide
    help information in a sidebar expander,
    hide the sidebar, and display a sticky header. The function also displays
    information about the scientific frameworks used,
    explains the tool, provides links to external resources, and includes a
    demonstration video.

    The function allows the user to choose options from the navigation bar,
    which triggers corresponding actions to switch pages
    or start a specific process. The chosen options include 'Data Explorer',
    'Layout Maker', 'Visualization Creator',
    and 'Data Story'. When 'Build a Data Story!' button is clicked, it switches
    to the 'exploratory data analysis' page.

    Note: The helper functions module is explained in the helper functions file

    Returns:
        None
    """
    # initialize a session state for the adjust mode in the data story
    st.session_state["adjust_mode"] = False
    st.session_state["page_1_title"] = "Page 1"
    st.session_state["page_2_title"] = "Page 2"
    st.session_state["page_3_title"] = "Page 3"


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
            default_index=0,
            key="homepage-menu",
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
        # delete the other session states so when we navigate back to the
        # respective pages, we dont get endless loops
        if "story-menu" in st.session_state:
            del st.session_state["story-menu"]
        if "exploration-menu" in st.session_state:
            del st.session_state["exploration-menu"]
        if "layout-menu" in st.session_state:
            del st.session_state["layout-menu"]
        if "visualization-menu" in st.session_state:
            del st.session_state["visualization-menu"]
        # handle the option that got chosen in the navigation bar
        if choose == "Data Exploration":
            switch_page("Exploratory Data Analysis")
        elif choose == "Story Composition":
            switch_page("Layout Creation")
        elif choose == "Story Narration":
            switch_page("Create Visualizations")
        elif choose == "Data Story":
            switch_page("Data Story 1")
        st.write("""<div class='fixed-header'/>""", unsafe_allow_html=True)

    # page title
    st.title("Data Story Authoring Tool - Homepage")

    # write down my thoughts about all the scientific frameworks that we use
    st.markdown(
        """<p>This is StoryPoint, an Authoring Tool to help you build no-Code \
             data stories with the help of natural language prompts.\
        The tool will guide you through three different stages before you complete \
        your data story:</p>
            <ul>
        <li><span class="bold">Data Exploration</span> - Select the dataset that you want to work with and view the Exploratory Data Analysis</li>
        <li><span class="bold">Story Composition</span> - Choose the number of pages and the layout for each page</li>
        <li><span class="bold">Story Narration</span> - Create the visualizations and two types of explanation text: (1) A story purpose
        that will be displayed on the top of the page and (2) Chart explanations for each visualization</li>
    </ul>
    <p>After these steps, you can view the finished Data Story. See below for an example story:</p>
    """,
        unsafe_allow_html=True,
    )

    st.image("static/img/Story_Explanation/Folie1.png")

    # switch to the layout configurator page
    start_process = st.button("Build a Data Story!")
    if start_process:
        switch_page("exploratory data analysis")

    # Javascript code to log click events on the screen
    my_js = """
    // Function to handle the mouse click event
    function handleClick(event) {
    // Get the x and y coordinates of the mouse click
    var x = event.clientX;
    var y = event.clientY;

    // Log the coordinates in the console
    console.log('Mouse click at coordinates (x:', x, ', y:', y, ')');
    }

    // Attach the click event listener to the document
    window.parent.document.addEventListener('click', handleClick);

    """

    # Wrap the javascript as html code
    my_html = f"<script>{my_js}</script>"

    # activate the functionality
    html(my_html, height=0)

    with st.sidebar:
        st.write(
            """<p>This Feedback button is displayed on every page of the tool and can\
                  be used to give your opinion on specific features.\
                 How to use it:</p>
                 <ol>
                 <li>Click the Story Evaluation Button</li>
                 <li>Click next to the element that you want to provide feedback for</li>
                 <li>Fill out the feedback form and click submit</li>
                 </ol>
                 """,
            unsafe_allow_html=True,
        )
        gpt_helper.feedback(page=choose)


if __name__ == "__main__":
    main()
