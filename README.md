# StoryPoint
This repo contains the source code for the work **StoryPoint: A Data Story Authoring Tool for Enterprises**.

In today’s data-driven world, enterprises are confronted with an exponential increase in data, requiring employees skilled in data
visualization. Simultaneously, data storytelling as an effective means of communicating data-driven insights is on the rise. However,
current data visualization tools offer little assistance in crafting compelling data stories, underscoring the need for innovative authoring
tools. This paper introduces StoryPoint, a data story authoring tool tailored for domain experts in enterprises. By empowering
domain experts with the ability to intuitively visualize data through natural language inputs alongside pre-calculated charts and
narrative elements, the bridge between data visualization and its interpretation can be narrowed. To design StoryPoint, we followed a
user-centered and literature-supported approach. A formative evaluation involving eight domain experts reveals StoryPoint’s efficacy
in rapid data story prototyping. A summative evaluation with three additional domain experts, encompassing real-world industry data
visualization cases, underscores StoryPoint’s utility.

## How to Install
The code uses python 3.9.13 and Streamlit 1.23.1. The full dependency can be found and installed via requirements.txt.

After that, follow the installation from [this Readme](https://github.com/DenizD/Streamlit-Image-Carousel) and navigate to the frontend directory to initialize npm and subsequently install the node modules.

## Live Demo
A running live demo can be found here.
Due to the deployment process there might be two problems that don't occur when running the porject localy:
- problem with MultiVision package: we noticed that unconventional graphical representations may be generated
- problem with the API quota: Because the app is now public, we limited the API quota to 10$ per month. If the quota is exceeded, the LLM functions won't work anymore.

## Project Structure
    .
    ├── data                    # csv files of the provided sample datasets
    ├── feedback                # json files containing user feedback collected by the feedback button 
    ├── feedback_component      # the implementation for the feedback button component 
    ├── frontend                # contains the [Streamlit Image Carousel](https://github.com/DenizD/Streamlit-Image-Carousel)
    ├── multivision             # Automatically generated Charts from the [MultiVision Paper](https://github.com/wowjyu/MultiVision)
    ├── pages                   # The content of the app containing the streamlit web pages
    │   ├── 00_exploratory_data_analysis.py              # Data Exploration
    │   ├── 01_layout_creation.py                        # Story Composition
    │   ├── 02_create_visualizations.py                  # Story Narration
    │   ├── 03_data_story.py                             # Final Data Story (dynamically generated inside of helper_functions.py)
    ├── homepage.py             # Homepage that explains how the tool works 
    ├── README.md 
    ├── requirements.txt

# How to Use
Navigate into the root folder of the app and inside the terminal type streamlit run .\homepage.py. Now the app should open up in your localhost.

The app guides you through the creation of a data story and offers the following features:

- Choose your Dataset
- Perform an Exploratory Data Analysis (EDA) to become familiar with the data and to get inspired for possible visualizations
- Choose the data story layout
- Create the visualizations using a **no code NL2VIS Interface** with OpenAIs Large Language Models (LLM)
- Adjust the visualizations until they suit you
- Get inspired by the automatically generated narrative elements that will correspond to the respective visualizations
- View and Explore your finished data story with interactive filters, the AskData feature and the option for the viewer to provide Feedback

## Example
![Using the provided superstore sales dataset](/static/img/example_dashboard_1.png)

