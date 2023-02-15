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

# Let's try to create pairplots with seaborn
@st.cache_data
def load_pairplot_data():
    df = pd.DataFrame(
        {
            "x": np.arange(10),
            "y": np.arange(10),
            "一": np.arange(10),
            "四": np.arange(10),
            "label": ["あ", "い", "う", "え", "お", "か", "き", "く", "け", "こ"],
        }
    )
    return df


# In the case of sns.pairplot, you don’t just have one matplotlib.figure.Figure object returned. It’s non-trivial.
# The issue with the missing Japanese characters in the seaborn pairplot is caused by the fact that the pairplot method in seaborn creates multiple subplots,
# each with its own set of tick labels, axis labels, and legend. Therefore, to get the Japanese characters to display correctly in the pairplot, you need to
# set the font properties for each subplot separately. You can achieve this by iterating through the subplots and setting the font properties for each one.
# The pairplot function returns a PairGrid object that can be used to access the individual subplots.
# Note: When corner=True in sns.pairplot, the subplots of the pairplot are organized differently than when corner=False. In the case of corner=True,
# the diagonal plots are displayed separately and share a common y-axis. The off-diagonal plots are displayed in the upper-right triangle of the grid,
# while the lower-left triangle is left empty.
# i.e. sns.pairplot returns a PairGrid object when corner=False, but returns a SubplotGrid object when corner=True. The PairGrid object has a g.axes attribute
# that is a 2D array of the subplots, whereas the SubplotGrid object does not have an axes attribute.
# To handle both cases, we need to first check whether g has an axes attribute. If it does, we can iterate over g.axes.flat. If it does not, we can iterate over
# the g object directly, using the g.diag_axes and g.map_upper methods to access the diagonal and off-diagonal plots, respectively.
# This code uses try and except statements to handle the NoneType errors that occur when subplots do not have xlabels or ylabels. If an AttributeError occurs
# while setting the font properties of a subplot, the code simply moves on to the next subplot, ignoring the one that caused the error:


def create_pairplot(g):
    if g.axes is not None:
        axes = g.axes.flat
    else:
        axes = np.concatenate([g.diag_axes, g.map_upper().flat])
    for ax in axes:
        try:
            if ax.get_xlabel() is not None:
                ax.set_xlabel(ax.get_xlabel(), fontproperties=prop)
            if ax.get_xticklabels():
                ax.set_xticklabels(ax.get_xticklabels(), fontproperties=prop)
            if ax.get_ylabel() is not None:
                ax.set_ylabel(ax.get_ylabel(), fontproperties=prop)
            if ax.get_yticklabels():
                ax.set_yticklabels(ax.get_yticklabels(), fontproperties=prop)
            if ax.get_title() is not None:
                ax.set_title(ax.get_title(), fontproperties=prop)
        except AttributeError:
            pass

    return g


df = load_pairplot_data()

col1, col2 = st.columns(2)
plot1 = create_pairplot(sns.pairplot(df, corner=False))
plot2 = create_pairplot(sns.pairplot(df, corner=True))
col1.pyplot(plot1.fig)
col2.pyplot(plot2.fig)
