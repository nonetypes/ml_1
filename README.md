## Description
An attempt to use machine learning to predict stock direction and prices. Currently, the model cannot predict into the future and is oriented for immediate testing of the accuracy of its predictions. This model is not intended to be used as an aid to purchase stocks and is not guaranteed in any way to reduce the inherent risk of investing. Use at your own risk.

The input data used includes thousands of stocks up to 11-10-2017.

https://www.kaggle.com/borismarjanovic/price-volume-data-for-all-us-stocks-etfs

## Approach
A benchmark of 90 prediction days was used. Polynomial regression is used to model the price predictions. First, on a portion of the data which is initially limited by the amount of desired prediction days, a wide range of training day ranges and polynomial degrees are tried and predicted with the given data set. These predictions are tested against the most recent data which is equal in range to the prediction days. Once the parameters with the lowest mean absolute error is found, predictions are then made on the non-limited data set with the best parameters.

## Results
In determining the accuracy of predictions, a mean relative accuracy of all predictions against the test data was applied.
Unexpectedly, accuracy results can vary widely due to the inherently unpredictable nature of stocks. However, for individual stocks, relative accuracies of >90% are not uncommon. Due to the nature of polynomial regression, predictions which veer wildly off track are not uncommon either. The results are heavily influenced by the number of predictions which are made — the greater the number, the lower the accuracy.

## Possible Applications
It was observed that the model does well in its predictions when there was a clear trend in the data. A possible application would be to find predictions made across thousands of stocks which have a positive angle of sufficient degrees. These could then be reviewed by a human to discover unfamiliar stocks with an upward trend.
