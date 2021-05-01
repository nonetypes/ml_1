# ml_single.py by nonetypes
# Last revised on 04/30/2021
# Predict price trends for a single stock for an x amount of days.

from functions import accuracy, make_predictions, plot_predictions
import pandas as pd


def predict_stock(symbol, prediction_days, verbose=False, show_graph=False, save_graph=False):
    """Predict price trends for a single stock for an x amount of days.

    Use polynomial regression to predict prices and trends.

    A wide variety of training day ranges and polynomial degrees are tested in an attempt to find
    parameters which are most suitable to stock.
    """
    directory = 'input/Stocks/'
    stock = pd.read_csv(f'{directory}{symbol.lower()}.us.txt')[:-prediction_days]

    # Polynomial degrees to try. Including 2-9
    degrees = [x for x in range(2, 10)]

    # Create increasingly larger day ranges for the training data.
    # Day ranges will start with prediciton_days and then double until the maximum is reached for the stock.
    history = []
    x = prediction_days
    while x <= len(stock) - prediction_days:
        history.append(x)
        x = x * 2
    history.append(len(stock) - prediction_days)
    stock_results = {}

    # Find best training day range for stock.
    for hist_days in history:
        if verbose:
            print(hist_days)
        # Split data
        train_data, test_data = stock[:-prediction_days][-hist_days:], stock[-prediction_days:]
        # Get closing prices.
        train_data, test_data = train_data['Close'].values, test_data['Close'].values\

        stock_results[hist_days] = []

        # Find best polynomial regression degree for data.
        for degree in degrees:
            predictions = make_predictions(prediction_days, train_data, degree)

            # Track results.
            stats = accuracy(predictions, test_data)
            stock_results[hist_days].append(stats[0])
            if verbose:
                print(f'{degree}: {stats}')

    # Find the lowest average absolute error across all predictions and get its paramaters (hist_days, degree).
    best_results = {}
    for hist_days, vals in stock_results.items():
        best_results[hist_days] = vals[vals.index(min(vals))]

    best_index = list(best_results.values()).index(min(best_results.values()))
    lowest_error = best_results[history[best_index]]
    hist_days = history[best_index]
    degree = degrees[stock_results[hist_days].index(lowest_error)]

    if verbose:
        print(f'Best parameters: {hist_days} historic days with a polynomial regression degree of {degree}.')

    # hist_days = hist_days + prediction_days

    # Remove limitation on stock range and get new predictions with the best parameters.
    stock = pd.read_csv(f'{directory}{symbol}.us.txt')
    train_data, test_data = stock[:-prediction_days][-hist_days:], stock[-prediction_days:]
    # For plotting on graph.
    train_dates, test_dates = train_data['Date'], test_data['Date']
    # Get closing prices.
    train_data, test_data = train_data['Close'].values, test_data['Close'].values

    # Get new predictions with the "best" parameters.
    predictions = make_predictions(prediction_days, train_data, degree)

    stats = accuracy(predictions, test_data)
    if verbose:
        print(stats)
        print(f'Predictions have an average of {round(stats[1]*100, 2)}% relative accuracy compared to actual prices.')

    if show_graph or save_graph:
        plot_predictions(symbol, prediction_days, hist_days, degree, predictions, stats,
                         train_dates, train_data, test_dates, test_data, show=show_graph, save=save_graph)

    return hist_days, degree, predictions, stats


if __name__ == '__main__':
    predict_stock('bcor', 90, True, True)
