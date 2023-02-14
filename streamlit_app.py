import os

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st
from matplotlib import font_manager as fm

# Set the font path
fpath = os.path.join(os.getcwd(), "NOTO_SANS_JP/NotoSansJP-Regular.otf")
prop = fm.FontProperties(fname=fpath)


@st.cache_data
def load_data():
    # Create a dataframe containing japanese characters and plot it with pure matplotlib
    df = pd.DataFrame(
        {
            "x": np.arange(10),
            "y": ["一", "二", "三", "四", "五", "六", "七", "八", "九", "十"],
            "label": ["あ", "い", "う", "え", "お", "か", "き", "く", "け", "こ"],
        }
    )

    return df


@st.cache_data
def plot_data(df):
    # Plot the dataframe
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df["x"], df["y"], label=df["label"])
    ax.legend(prop=prop, loc="upper left")
    ax.set_title("日本語タイトル", fontproperties=prop)
    ax.set_xticks(df["x"])
    ax.set_xticklabels(df["label"], fontproperties=prop)
    ax.set_yticks(df["y"])
    ax.set_yticklabels(df["y"], fontproperties=prop)
    return fig


df = load_data()
fig = plot_data(df)
st.pyplot(fig)

# Now let's try to use seaborn to plot the same dataframe but as a scatter plot
@st.cache_data
def plot_data_seaborn(df):
    sns_fig, sns_ax = plt.subplots(figsize=(10, 6))
    sns.set(font=prop.get_name())
    sns.scatterplot(data=df, x="x", y="y", hue="label")
    handles, labels = sns_ax.get_legend_handles_labels()
    sns_ax.legend(handles, labels, prop=prop, loc="upper right")
    sns_ax.set_title("日本語タイトル", fontproperties=prop)
    sns_ax.set_xticks(df["x"])
    sns_ax.set_xticklabels(df["label"], fontproperties=prop)
    sns_ax.set_yticks(df["y"])
    sns_ax.set_yticklabels(df["y"], fontproperties=prop)
    return sns_fig


sns_fig = plot_data_seaborn(df)
st.pyplot(sns_fig)
