# Deployment URL

####
```
https://testprayag.z1.web.core.windows.net/
```

## About Us

Welcome to Prediction Models!

Discover the power of data-driven predictions.

Here, you can easily forecast the number of days late of your delivery using the key parameters like suppliers, quantity number, and more. Our platform not only provides accurate predictions but also allows you to compare multiple machine learning models and analyze their performance. For even greater confidence, you can view the average results from all models to make well-informed decisions.

Start exploring now and see how predictive insights and model comparisons can transform your operations.

Your success, powered by foresight. 🚀

## About our Model

#### 1. Ensemble learning 
This was our first approach towards improving the base ML model. The result was an aerage prediction from 3 different models- RandomForest, XGB and A Linear regression model
#### 2. GridSearch CV on a Neural Network 
Performing GridSearch on a neural network helped us to find optimal hyperparamters. This proved helped us tackle the overfitting problem associated with using less features for an Artificial Neural Network. we then fitted an ANN with dropout layers, learning rate and epochs as hyperparamters suggested from GridSearchCV

## Prediction
https://github.com/user-attachments/assets/07a61b05-da52-4de0-97d4-74a49a83163c

# Run Frontend and Backend

## Start frontend
inside folder frontend

```sh
yarn install
yarn dev --host
```

## Start backend
inside folder backend

```sh
func start
```



