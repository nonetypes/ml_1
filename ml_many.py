# ml_many.py by nonetypes
# Last revised on 04/30/2021
# Predict price trends for many random stocks to test overall accuracy of model.
# Predictions which have an upward trend will be saved in chart form to be reviewed by a human.
# Results are saved to /output

from functions import accuracy, make_predictions, prediction_angle, plot_predictions
from ml_single import predict_stock
from os import listdir, getcwd
from random import shuffle
import pandas as pd


num_of_stocks = 3
prediction_days = 90

directory = 'input/Stocks/'
# Get random symbols from stocks in stock directory.
stocks = [x[:-7] for x in listdir(directory)]
shuffle(stocks)
stocks = stocks[:num_of_stocks]
print(stocks)
results = {}
# Save stats for each stock to /output/output.txt
output = ''

# Get the length of the longest stock symbol for padding in output.
max_len = max([len(x) for x in stocks])

# Filter out stocks which have too few entries, or stock.txt files which are empty
filtered_stocks = []
for symbol in stocks:
    try:
        stock = pd.read_csv(f'{directory}{symbol.lower()}.us.txt')[:-prediction_days]
    # Pass over empty stock.txt files.
    except Exception:
        pass
    else:
        # Stock must end up with at least 2 training days.
        if len(stock) - (2 * prediction_days) >= 2:
            filtered_stocks.append(symbol)


for symbol in filtered_stocks:

    # Attempt to get the best parameters for the stock.
    hist_days, degree, predictions, stats = predict_stock(symbol, prediction_days)

    # Remove limitation on stock range and get new predictions with the best parameters.
    stock = pd.read_csv(f'{directory}{symbol}.us.txt')
    train_data, test_data = stock[:-prediction_days][-hist_days:], stock[-prediction_days:]
    # For plotting on graph.
    train_dates, test_dates = train_data['Date'], test_data['Date']
    # Get closing prices.
    train_data, test_data = train_data['Close'].values, test_data['Close'].values

    # Get new predictions with the "best" parameters.
    predictions = make_predictions(prediction_days, train_data, degree)
    # Print and track stats to be saved to /output/output.txt
    stats = accuracy(predictions, test_data)
    results[symbol] = stats
    pad = max_len - len(symbol)
    result = f'{symbol.upper()}:{" "*pad} {round(stats[1]*100, 2)}%, {hist_days}, {degree}'
    print(f'{result}, {round(prediction_angle(predictions))}')
    output += f'{result}\n'

    # If the prediction angle is above 30 degrees and the last prediction is not 1.5 times higher than highest price,
    # then save the chart to /output/charts
    if prediction_angle(predictions) >= 30 and predictions[-1] < (max(train_data) * 1.5):
        plot_predictions(symbol, prediction_days, hist_days, degree, predictions, stats,
                         train_dates, train_data, test_dates, test_data, False, True)

# Print and track overall stats.
total_accuracy = [x[1] for x in results.values()]
mean_accuracy = round((sum(total_accuracy) / len(total_accuracy)) * 100, 2)
total = f'{mean_accuracy}% accurate across {len(total_accuracy)} stocks.'
print(total)
good_predictions = [x for x in total_accuracy if x >= .9]
perc_of_good_predictions = round(len(good_predictions) / len(total_accuracy) * 100)
good_predictions = f'{perc_of_good_predictions}% are 90% or higher.'
print(good_predictions)


with open(f'{getcwd()}/output/output.txt', 'w') as stream:
    stream.write(total+'\n'+good_predictions+'\n\n'+output)
