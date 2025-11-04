
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from PIL import Image, ImageEnhance, ImageFilter, ImageOps


def main():
    #priceTrendGraph()
    #salesPlot()
    #cmapImagePlot()
    filterImagePlot()


def priceTrendGraph():
    

    """Data : Use the ‘wti-daily.csv’ and ‘brent-daily.csv’ files into a data frame
    in which the Date column is treated as a datetime value and is set to be
    the index.
    Q1. Plot the average price trend of oil from 1992-2002 from wti-
    daily.csv?
    Q2. Plot the average price trend of oil from 1992 -2002
    Q3. Compare the both the average prices of a barrel of oil from 1992-
    2002, indicate significant differences though markers. """

    brentDailyData = pd.read_csv('Assignment_1/Data/brent-daily.csv')
    wtiDailyData = pd.read_csv('Assignment_1/Data/wti-daily.csv')



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

def salesPlot():


    """ Data: Use the ‘ sales.xlsx ’ to answer the questions Q4 and Q5.
    Q4. Plot the city wise distribution of sales, which city has contributed
    maximum in the sales.
    Q5. Does payment methods have impact on sales, which payment
    method is contributing to the sales. """

    salesData = pd.read_excel('Assignment_1/Data/sales.xlsx')

    salesData.drop(['Invoice ID', 'Branch', 'Customer type', 'Gender',
       'Product Code', 'Unit price', 'Quantity', 'Tax 5%', 'Total', 'Date',
        'COGS', 'gross margin percentage', 'Rating'], axis=1, inplace=True)
    #print(salesData.head())
    #print (salesData.columns)

    salesData.rename(columns={'City': 'City', 'Payment': 'Payment Method', 'gross income': 'Gross Income'}, inplace=True)

    #print (salesData.isnull().sum())

    city_sales = salesData.groupby('City')['Gross Income'].sum().reset_index()
    payment_sales = salesData.groupby('Payment Method')['Gross Income'].sum().reset_index()

    plt.figure(figsize=(16, 9))
    plt.subplot(1, 2, 1)
    plt.bar(city_sales['City'], city_sales['Gross Income'], color=['blue', 'orange', 'green'])
    plt.ylim(city_sales['Gross Income'].min() * 0.95, city_sales['Gross Income'].max() * 1.05)
    plt.title('City-wise Sales Distribution')
    plt.ylabel('Gross Income')

    plt.subplot(1, 2, 2)
    plt.bar(payment_sales['Payment Method'], payment_sales['Gross Income'], color=['blue', 'orange', 'green'])
    plt.ylim(payment_sales['Gross Income'].min() * 0.95, payment_sales['Gross Income'].max() * 1.05)
    plt.title('Sales by Payment Method')
    plt.ylabel('Gross Income')

    plt.tight_layout()
    plt.show()


def cmapImagePlot():
    """ Data: Use ‘ 2.jpg ’ file to answer the questions Q6 and Q7.
    Q6. Read the image ‘2.jpg’ into a NumPy array, apply six different types
    of ‘cmaps’, and put these images six subplots."""

    img = Image.open('Assignment_1/Data/2.jpg')

    # Convert image to grayscale 
    img_gray = ImageOps.grayscale(img)

    # Create a NumPy array from the image
    img_array = np.array(img_gray)

    cmaps = ['gray', 'hot', 'viridis', 'plasma', 'cividis', 'magma']

    plt.figure(figsize=(16, 9))

    for i, cmap in enumerate(cmaps):
        plt.subplot(2, 3, i + 1)
        plt.imshow(img_array, cmap=cmap)
        plt.title(f'Cmap: {cmap}')
        plt.axis('off')

    plt.tight_layout()
    plt.show()


def filterImagePlot():

    """ Q7. Apply six basic filters on image ‘2.jpg’. Put these six images into
    two subplots of the following format as:
    - total number of the rows are 3
    - 3 subplots in the 1st row, one sublot in the 2nd row and two subplots in
    the 3rd row.  """

    img = Image.open('Assignment_1/Data/2.jpg')

    filters = [
        ('BLUR', img.filter(ImageFilter.BLUR)),
        ('CONTOUR', img.filter(ImageFilter.CONTOUR)),
        ('DETAIL', img.filter(ImageFilter.DETAIL)),
        ('EDGE_ENHANCE', img.filter(ImageFilter.EDGE_ENHANCE)),
        ('EMBOSS', img.filter(ImageFilter.EMBOSS)),
        ('SHARPEN', img.filter(ImageFilter.SHARPEN))
    ]

    plt.figure(figsize=(16, 9))


    for i, (filter_name, filtered_img) in enumerate(filters):
        if i < 3:
            plt.subplot(3, 3, i + 1)  # First row
        elif i == 3:
            plt.subplot(3, 3, 5)      # Second row
        else:
            plt.subplot(3, 3, i + 3)  # Third row

        plt.imshow(filtered_img)
        plt.title(filter_name)
        plt.axis('off')
    
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()