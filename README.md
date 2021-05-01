## Description
An attempt to use machine learning to predict stock direction and prices. Currently, the model cannot predict into the future and is oriented for immediate testing of the accuracy of its predictions. This model is not intended to be used as an aid to purchase stocks and is not guaranteed in any way to reduce the inherent risk of investing. Use at your own risk.

The input data used includes thousands of stocks up to 11-10-2017.

https://www.kaggle.com/borismarjanovic/price-volume-data-for-all-us-stocks-etfs

ml_test.py is used to manually input specific prediction days, training day ranges, and polynomial degrees for a specific stock in order to view charted, immediate results.

ml_single.py is used for predictions of a single stock where ideal parameter finding is automated and then used in its prediction.

ml_many.py is used to run on multiple, randomly chosen stocks for evaluating the overall accuracy of the model. Results are saved to /output/output.txt, and charts of stocks with potentially upward trends are saved to /output/charts.


## Approach
Polynomial regression is used to model the price predictions. First, on a portion of the data which is initially limited by the amount of desired prediction days, a wide range of training day ranges and polynomial degrees are tried and predicted with the given data set. These predictions are tested against the most recent data which is equal in range to the prediction days. Once the parameters with the lowest mean absolute error is found, predictions are then made on the non-limited data set with the best parameters.

## Results
A benchmark of 90 prediction days was used. In determining the accuracy of predictions, a mean relative accuracy of all predictions against the test data was applied.
Unexpectedly, accuracy results can vary widely due to the inherently unpredictable nature of stocks. However, for individual stocks, relative accuracies of >90% are not uncommon. Due to the nature of polynomial regression, predictions which veer wildly off track are not uncommon either. The results are heavily influenced by the number of predictions which are made — the greater the number, the lower the accuracy.

Across 855 randomly chosen stocks, there was an average mean relative accuracy of 52.42%, and 38% of the stocks had a mean relative accuracy of obove 90%. Of the 855 stocks, 337 were identified by the model as having predictions with a sufficient postive degree, indicating a potential positive trend. Of those 337, 47% were confirmed by the test data to have a positive gain in price at the end of the 90 days. While these results are not impressive, the model may still have potential and improvements could yet be made.

## Possible Applications
It was observed that the model does well in its predictions when there was a clear trend in the data. A possible application would be to find predictions made across thousands of stocks which have a positive angle of sufficient degrees. These could then be reviewed by a human to discover unfamiliar stocks with an upward trend.

## Concerns
The impact of algorithms on the stock market is a growing concern. Machine learning can lend an unfair advantage in favor of those who possess robust data sets and resources to dedicate to algorithmic trading. But, if such tools are widely available to the general trading public, applications such as this one could help to level the playing field. However, the consequences of widespread applications of machine learning to stock market speculation is ultimately unknown and potentially catastrophic.
