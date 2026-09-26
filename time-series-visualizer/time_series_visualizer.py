import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def draw_line_plot():
    df = pd.read_csv("fcc-forum-pageviews.csv")
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)

    # Clean data (2.5% filter)
    df = df[
        (df['value'] >= df['value'].quantile(0.025)) &
        (df['value'] <= df['value'].quantile(0.975))
    ]

    fig, ax = plt.subplots(figsize=(15, 5))
    ax.plot(df.index, df['value'], color='red')

    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")

    return fig


def draw_bar_plot():
    df = pd.read_csv("fcc-forum-pageviews.csv")
    df['date'] = pd.to_datetime(df['date'])

    # Clean
    df = df[
        (df['value'] >= df['value'].quantile(0.025)) &
        (df['value'] <= df['value'].quantile(0.975))
    ]

    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month

    df_grouped = df.groupby(['year', 'month'])['value'].mean().unstack()

    fig = df_grouped.plot(kind='bar').figure

    plt.xlabel("Years")
    plt.ylabel("Average Page Views")
    plt.legend(title="Months", labels=[
        "Jan","Feb","Mar","Apr","May","Jun",
        "Jul","Aug","Sep","Oct","Nov","Dec"
    ])

    return fig


def draw_box_plot():
    df = pd.read_csv("fcc-forum-pageviews.csv")
    df['date'] = pd.to_datetime(df['date'])

    # Clean
    df = df[
        (df['value'] >= df['value'].quantile(0.025)) &
        (df['value'] <= df['value'].quantile(0.975))
    ]

    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.strftime('%b')
    df['month_num'] = df['date'].dt.month

    df = df.sort_values('month_num')

    fig, axes = plt.subplots(1, 2, figsize=(20, 8))

    # Year-wise box plot
    sns.boxplot(x='year', y='value', data=df, ax=axes[0])
    axes[0].set_title("Year-wise Box Plot (Trend)")
    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("Page Views")

    # Month-wise box plot
    sns.boxplot(x='month', y='value', data=df, ax=axes[1])
    axes[1].set_title("Month-wise Box Plot (Seasonality)")
    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Page Views")

    return fig
