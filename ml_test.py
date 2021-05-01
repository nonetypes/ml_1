# ml_test.py by nonetypes
# Last revised on 04/30/2021
# Intended to be used to quickly produce stats and charts for specific stocks and parameters.

from functions import make_predictions, plot_predictions, prediction_angle, accuracy
import pandas as pd

symbol = 'bcor'
prediction_days = 90
hist_days = 1440
degree = 6

# hist_days = hist_days + prediction_days

directory = 'input/Stocks/'
# stock = pd.read_csv(f'{directory}{symbol.lower()}.us.txt')[:-prediction_days]
stock = pd.read_csv(f'{directory}{symbol.lower()}.us.txt')
# print(stock)

# Divide data for training and testing.
# Testing is the most x most recent data points. x = prediction_days
# Training is the y most recent data points before the testing data. y = hist_days
train_data, test_data = stock[:-prediction_days][-hist_days:], stock[-prediction_days:]
# For plotting on graph.
train_dates, test_dates = train_data['Date'], test_data['Date']
# Get closing prices.
train_data, test_data = train_data['Close'].values, test_data['Close'].values
print(len(stock))
print(len(train_data), len(test_data))

# Get predictions with best parameters.
predictions = make_predictions(prediction_days, train_data, degree)


stats = accuracy(predictions, test_data)
print(stats)
# print(f'Predictions have an average absolute error of {round(stats[0], 2)}.')
print(f'Predictions have an average of {round(stats[1]*100, 2)}% relative accuracy compared to actual prices.')
print(f'Predictions Angle: {prediction_angle(predictions)}')

# Show a matplotlib graph.
plot_predictions(symbol, prediction_days, hist_days, degree, predictions, stats,
                 train_dates, train_data, test_dates, test_data, show=True)
