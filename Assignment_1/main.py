
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl


def main():
    priceTrendGraph()


def priceTrendGraph():
    brentDailyData = pd.read_csv('Assignment_1/data/brent-daily.csv')
    wtiDailyData = pd.read_csv('Assignment_1/data/wti-daily.csv')



    """Data : Use the ‘wti-daily.csv’ and ‘brent-daily.csv’ files into a data frame
    in which the Date column is treated as a datetime value and is set to be
    the index.
    Q1. Plot the average price trend of oil from 1992-2002 from wti-
    daily.csv?
    Q2. Plot the average price trend of oil from 1992 -2002
    Q3. Compare the both the average prices of a barrel of oil from 1992-
    2002, indicate significant differences though markers. """

    brentDailyData['Date'] = pd.to_datetime(brentDailyData['Date'])
    wtiDailyData['Date'] = pd.to_datetime(wtiDailyData['Date'])
    brentDailyData.set_index('Date', inplace=True)
    wtiDailyData.set_index('Date', inplace=True)

    brent_1992_2002 = brentDailyData['1992-01-01':'2002-12-31']
    wti_1992_2002 = wtiDailyData['1992-01-01':'2002-12-31']

    brent_avg = brent_1992_2002['Price'].resample('ME').mean()
    wti_avg = wti_1992_2002['Price'].resample('ME').mean()

    price_diff = abs(brent_avg - wti_avg)

    threshold = 2.0
    significant_points = price_diff > threshold

    plt.figure(figsize=(16, 9))
    plt.plot(brent_avg.index, brent_avg.values, label='Brent Average Price', color='blue')
    plt.plot(wti_avg.index, wti_avg.values, label='WTI Average Price', color='orange')

    # probably need better way to show significant points
    plt.scatter(brent_avg.index[significant_points], 
                brent_avg[significant_points],
                color='red',
                label='Significant Difference', 
                zorder=2) # makes the markers appear on top

    plt.title('Average Oil Prices (1992-2002)')
    plt.xlabel('Year')
    plt.ylabel('Average Price (USD)')
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    main()