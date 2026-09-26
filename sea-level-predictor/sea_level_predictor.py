import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress

def draw_plot():
    df = pd.read_csv("epa-sea-level.csv")

    # Scatter plot
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(df['Year'], df['CSIRO Adjusted Sea Level'])

    # First line of best fit (all data)
    slope, intercept, r, p, std_err = linregress(
        df['Year'], df['CSIRO Adjusted Sea Level']
    )

    years = range(df['Year'].min(), 2051)
    ax.plot(
        years,
        intercept + slope * years,
        'r',
        label='All data'
    )

    # Second line (from year 2000 onward)
    df_2000 = df[df['Year'] >= 2000]

    slope2, intercept2, r2, p2, std_err2 = linregress(
        df_2000['Year'], df_2000['CSIRO Adjusted Sea Level']
    )

    years_2000 = range(2000, 2051)
    ax.plot(
        years_2000,
        intercept2 + slope2 * years_2000,
        'g',
        label='2000+ data'
    )

    # Labels and title
    ax.set_xlabel("Year")
    ax.set_ylabel("Sea Level (inches)")
    ax.set_title("Rise in Sea Level")

    return fig
