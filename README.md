# Zillow Prize: Zillow’s Home Value Prediction (Zestimate)
## Machine Learning Engineer Nanodegree Capstone Project

“Zestimates” are estimated home values based on 7.5 million statistical and machine learning models that analyze hundreds of data points on each property. And, by continually improving the median margin of error (from 14% at the onset to 5% today), Zillow has since become established as one of the largest, most trusted marketplaces for real estate information in the U.S. and a leading example of impactful machine learning.

Zillow Prize, a competition with a one million dollar grand prize, is challenging the data science community to help push the accuracy of the Zestimate even further. Winning algorithms stand to impact the home values of 110M homes across the U.S.

## Usage
- Proposal PDF contains the Project Proposal for Udacity
- Analysis Notebook contians Data Analysis for the project
- Run `code/main.py` and `code/test.py`

## Installation
- Download the dataset from [Here](https://www.kaggle.com/c/zillow-prize-1/data)
- Update the correct data link for the files `code/main.py` `code/test.py`
- To run using NN run code/test.py
- To run using Catboost run code/main.py

## Requirements 

- Keras `$ pip install keras`
- Catboost `$ pip install catboost`
- Sklearn `$ pip install scikit-learn`
- Numpy
- Matplotlib
- Seaborn
- Python 3.6

## Results 
- Catboost gave a score of 0.0651283
- MLP gave a score of 0.0654378
![](https://i.gyazo.com/df9b52436d465412dafd5b87470f409e.png)
