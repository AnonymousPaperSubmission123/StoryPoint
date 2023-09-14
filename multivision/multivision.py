import pandas as pd
import json
import numpy as np
import itertools
import sys
import re
import altair as alt
from threading import Thread
import torch
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence
from torch.autograd import Variable
import torch.nn.functional as nnf
import streamlit as st
from multivision.model.encodingModel import (
    ChartTypeNN,
    ChartTypeLSTM,
    ScoreNetLSTM,
)

# from utils.helper import softmax, get_data_feature_by_column, get_embed_feature_by_column, get_all_charts_scores, charts_to_features
from multivision.utils.ChartRecommender import ChartRecommender
from multivision.utils.VegaLiteRender import VegaLiteRender


class Recommender(Thread):
    def __init__(self, data_path, num_rec, dataset):
        self.vega_specs = None
        self.data_path = data_path
        self.num_rec = num_rec
        self.dataset = dataset

    def run(self):
        # Load pretrained word-embedding model
        word_embedding_model_path = "multivision/utils/en-50d-200000words.vec"

        word_embedding_dict = {}
        with open(word_embedding_model_path, encoding="utf8") as file_in:
            lines = []
            for idx, line in enumerate(file_in):
                if idx == 0:  ## line 0 is invalid
                    continue
                word, *features = line.split()
                word_embedding_dict[word] = np.array(features)

        # Load trained single-chart assessment model and chart type prediction model
        gpu = torch.device("cuda:0")

        column_score_model = ScoreNetLSTM(
            input_size=96, seq_length=4, batch_size=2, pack=True
        )  # .to(gpu)
        column_score_model.load_state_dict(
            torch.load(
                "multivision/trainedModel/singleChartModel.pt",
                map_location=torch.device("cpu"),
            )
        )
        column_score_model.eval()

        chart_type_model = ChartTypeLSTM(
            input_size=96,
            hidden_size=400,
            seq_length=4,
            num_class=9,
            bidirectional=True,
        )  # .to(gpu)
        chart_type_model.load_state_dict(
            torch.load(
                "multivision/trainedModel/chartType.pt",
                map_location=torch.device("cpu"),
            )
        )
        chart_type_model.eval()

        # load the df

        if st.session_state["dataset"] == "💶 Salaries":
            data_path = "data/ds_salaries.csv"
            df = pd.read_csv(data_path)
            df.work_year = df.work_year.apply(lambda x: str(x))
            st.session_state["dataset_index"] = 1
        elif st.session_state["dataset"] == "🎥 IMDB Movies":
            data_path = "data/imdb_top_1000.csv"
            df = pd.read_csv(data_path)
            st.session_state["dataset_index"] = 0
        elif st.session_state["dataset"] == "📈 Superstore Sales":
            data_path = "data/superstore.csv"
            df = pd.read_csv(data_path, encoding="windows-1252")
            df["Postal Code"] = df["Postal Code"].apply(lambda x: str(x) + "_")
            st.session_state["dataset_index"] = 2
        elif st.session_state["dataset"] == "😷 Covid Worldwide":
            data_path = "data/covid_worldwide.csv"
            df = pd.read_csv(data_path)
            st.session_state["dataset_index"] = 3
        elif st.session_state["dataset"] == "🗣️ Amazon Customer Behaviour":
            data_path = "data/Amazon Customer Behavior Survey.csv"
            df = pd.read_csv(data_path)
            st.session_state["dataset_index"] = 4
        elif st.session_state["dataset"] == "🧺 Food Prices":
            data_path = "data/Food Prices.csv"
            df = pd.read_csv(data_path)
            st.session_state["dataset_index"] = 5
        elif st.session_state["dataset"] == "🛌 Sleep, Health and Lifestyle":
            data_path = "data/Sleep_health_and_lifestyle_dataset.csv"
            df = pd.read_csv(data_path)
            st.session_state["dataset_index"] = 6
        elif st.session_state["dataset"] == "🎵 Spotify Song Attributes":
            data_path = "data/Spotify_Song_Attributes.csv"
            df = pd.read_csv(data_path)
            st.session_state["dataset_index"] = 7

        # Apply the custom function and convert date columns
        for col in df.columns:
            # check if a column name contains date substring
            if "date" in col.lower():
                df[col] = pd.to_datetime(df[col])
                # remove timestamp
                df[col] = df[col].dt.date
                try:
                    df[col] = df[col].apply(lambda x: x.strftime("%Y-%m-%d"))
                except:
                    print("Error in Date Parsing")
        # reset index
        df = df.reset_index(drop=True)

        # replace space with _ in column names
        cols_widget = df.columns
        cols = ", ".join(cols_widget)

        # initialize the model
        chartRecommender = ChartRecommender(
            df, word_embedding_dict, column_score_model, chart_type_model
        )

        # get recommendations
        recommended_charts = pd.DataFrame.from_records(
            chartRecommender.charts
        ).sort_values(by="final_score", ascending=False)

        # for each requested visualization, create a vegalite spec
        vega_specs = []
        for i in range(30):
            recommend_chart = recommended_charts.iloc[i]
            vr = VegaLiteRender(
                chart_type=recommend_chart["chart_type"],
                columns=recommend_chart["fields"],
            )
            # delete the column vega lite attribute because the size of the charts will be broken
            # Check if 'column' exists in the 'encoding' dictionary --> then we wont take that viz
            # if "column" in vr.vSpec["encoding"]:
            #     # Remove the 'column' key from the 'encoding' dictionary
            #     vr.vSpec["encoding"].pop("column")
            #     continue
            vega_specs.append(vr.vSpec)

        self.vega_specs = vega_specs
        st.session_state[f"multivision_specs_{self.dataset}"] = self.vega_specs
