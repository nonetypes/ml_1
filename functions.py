# Functions to be used for ml_many.py, ml_single.py, and ml_test.py
# polynomial_regression, make_predictions, accuracy, plot_predictions, prediction_angle

import numpy as np
from math import atan2, pi
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_absolute_percentage_error
import matplotlib.pyplot as plt
from os import getcwd


def polynomial_regression(values, degree):
    """Polynomial regression.
    """
    X = [i for i in range(len(values))]

    X = np.array(X).reshape(-1, 1)
    Y = np.array(values)

    X = PolynomialFeatures(degree=degree, include_bias=False).fit_transform(X)
    Y_pred = LinearRegression().fit(X, Y).predict(X)

    return Y_pred


def make_predictions(prediction_num, train_data, degree):
    """Uses polynomial_regression to create x number of predictions.
    """

    predictions = []
    # Model will start with training data and built with predictions.
    model = list(train_data)
    model.append(polynomial_regression(model, degree)[-1])
    for i in range(prediction_num):
        # Get last data point from regression, add it to predictions and the model.
        ypred = polynomial_regression(model, degree)[-1]
        predictions.append(ypred)
        model.append(ypred)

    return predictions


def accuracy(y_pred, y_test):
    """Return the mean absolute errors, mean relative accuracy, and mean absolute percentage error
    of two data sets in tuple form.
    """

    abs_errors = []
    # relative_acc = []
    for i in range(len(y_test)):
        abs_error = abs(y_test[i] - y_pred[i])
        abs_errors.append(abs_error)
        # relative_acc.append((y_test[i] - abs(y_test[i] - y_pred[i])) / y_test[i])

    avg_abs_errors = sum(abs_errors) / len(abs_errors)
    mape = mean_absolute_percentage_error(list(y_test), list(y_pred))
    # avg_relative_acc = sum(relative_acc) / len(relative_acc)
    avg_relative_acc = 1-mape

    return (avg_abs_errors, avg_relative_acc, mape)


def plot_predictions(symbol, prediction_days, hist_days, degree, predictions, stats,
                     train_dates, train_data, test_dates, test_data, show=False, save=False):
    """Plot predictions on a graph.
    """

    # Get regressions for both the training data and all the data.
    all_dates, all_data = list(train_dates)+list(test_dates), list(train_data)+list(test_data)
    all_regression = polynomial_regression(all_data, degree)
    training_regression = polynomial_regression(train_data, degree)

    # figsize is in inches -- the dimensions of the graph.
    fig, ax = plt.subplots(figsize=[20, 11.25])
    plt.plot(all_dates, all_data, color='mediumblue', label='Historic Prices')
    plt.plot(all_dates, all_regression, color='seagreen', linestyle='--', label='Historic Regression')
    plt.plot(train_dates, training_regression, color='tomato', linestyle='--', label='Training Regression')
    plt.plot(test_dates, predictions, color='red', marker='o', linestyle='--', label='Predicted Prices', markersize=4)
    plt.title(f'{symbol.upper()} {prediction_days} Day Price Predictions\n{all_dates[0]} — {all_dates[-1]}',
              fontsize=17)
    plt.xlabel('Date', fontsize=14)
    plt.ylabel('Price', fontsize=16)
    if len(all_dates) > 80:
        # Limit the number of dates to display along the x axis.
        num_of_ticks = int(len(ax.get_xticks()) / 80)
        ax.set_xticks(ax.get_xticks()[::num_of_ticks])
    plt.xticks(rotation=70, fontsize=8)
    plt.gcf().text(.125, .89, f'Training Days: {hist_days}\nPolynomial Degree: {degree}',
                   fontsize=10, horizontalalignment='left')
    plt.gcf().text(.9, .89, f'Accuracy: {round(stats[1]*100, 2)}%', fontsize=10, horizontalalignment='right')

    plt.legend()
    if save:
        fig.savefig(f'{getcwd()}/output/charts/{symbol}.png', bbox_inches='tight')
    if show:
        plt.show()


def prediction_angle(predictions):
    """Get the angle of a line in degrees.

    https://stackoverflow.com/a/7586218
    """
    y_orig = predictions[0]
    y_land = predictions[-1]
    x_orig = 1
    x_land = 2
    # This needs revisiting. Output with below line is not making sense in many cases within model.
    # x_land = len(predictions)
    delta_y = y_land - y_orig
    delta_x = x_land - x_orig

    return (atan2(delta_y, delta_x) * 180) / pi


if __name__ == '__main__':
    predictions = [5, 5.46745, 5.73452, 6]
    print(prediction_angle(predictions))
    predictions = [1, 2, 3, 4, 5]
    print(prediction_angle(predictions))
