import xgboost
from catboost import CatBoostRegressor
from sklearn.ensemble import AdaBoostRegressor, RandomForestRegressor, ExtraTreesRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import ElasticNet, Lasso, Ridge
from sklearn.linear_model import SGDRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.svm import SVR
from sklearn.model_selection import GridSearchCV, KFold, train_test_split
from sklearn.metrics import fbeta_score, accuracy_score, log_loss, mean_absolute_error
import pandas as pd
import numpy as np
import pprint
import seaborn as sns
import matplotlib.pyplot as plt
from time import time
import random


class Model:
    def __init__(self, features, model_type, model_param):
        self.features = features
        self.model_type = model_type
        self.model_param = model_param
        if model_type in model_param:
            self.param = model_param[model_type]
        elif model_type + '_grid' in model_param:
            self.grid_param = model_param[model_type + '_grid']
        else:
            raise Exception('Model cannot be found in the file.')
        self.model = None

    def create_model(self, params=True):
        """
        Create model based on the model type class
        """
        if params:
            if self.model_type == 'xgb':
                self.model = xgboost.XGBRegressor(**self.param)
            elif self.model_type == 'cat':
                self.model = CatBoostRegressor(**self.param)
            elif self.model_type == 'adaboost':
                self.model = AdaBoostRegressor(**self.param)
            elif self.model_type == 'rf':
                self.model = RandomForestRegressor(**self.param)
            elif self.model_type == 'knn':
                self.model = KNeighborsRegressor(**self.param)
            elif self.model_type == 'svm':
                self.model = SVR(**self.param)
            elif self.model_type == 'sgd':
                self.model = SGDRegressor(**self.param)
            elif self.model_type == 'elas':
                self.model = ElasticNet(**self.param)
            elif self.model_type == 'mlp':
                self.model = MLPRegressor(**self.param)
            elif self.model_type == 'extra':
                self.model = ExtraTreesRegressor(**self.param)
            elif self.model_type == 'lasso':
                self.model = Lasso(**self.param)
            elif self.model_type == 'ridge':
                self.model = Ridge(**self.param)
        else:
            # used for grid_search
            if self.model_type == 'xgb':
                self.model = xgboost.XGBRegressor()
            elif self.model_type == 'adaboost':
                self.model = AdaBoostRegressor()
            elif self.model_type == 'rf':
                self.model = RandomForestRegressor()
            elif self.model_type == 'svm':
                self.model = SVR()
            elif self.model_type == 'lasso':
                self.model = Lasso()
            elif self.model_type == 'knn':
                self.model = KNeighborsRegressor()
            elif self.model_type == 'sgd':
                self.model = SGDRegressor()
            elif self.model_type == 'elas':
                self.model = ElasticNet()
            elif self.model_type == 'mlp':
                self.model = MLPRegressor()
            elif self.model_type == 'extra':
                self.model = ExtraTreesRegressor()
            elif self.model_type == 'lasso':
                self.model = Lasso()
            elif self.model_type == 'ridge':
                self.model = Ridge()

    def fit_model(self, x, y):
        """
        Fit model with input x and y
        """
        if self.model_type[:3] == 'xgb':
            self.model.fit(x, y, eval_metric='mae', verbose=True)
        else:
            def get_weight(x, weight):
                if x < 10:
                    return weight
                else:
                    return 1
            weights = x['month'].apply(lambda x: get_weight(x, 0.1)).as_matrix()
            self.model.fit(X=x, y=y, sample_weight=weights)
            # self.model.fit(x, y)

    def predict_model(self, x_test):
        """
        Regression
        """
        return self.model.predict(x_test)[:, np.newaxis]

    def run(self, x, y, x_test, y_test, metrics, params=True):
        """
        Wrap-up function for model create, fit and result report
        """
        self.create_model(params)
        self.fit_model(x, y)
        pred = self.predict_model(x_test)
        self.calc_metrics(metrics, y_test, pred)
        # if self.model_type == 'xgb':
        #     xgboost.plot_importance(self.model)
        #     plt.show()
        return pred

    def run_all(self, metrics, params=True):
        """
        Run function with the original data-set
        """
        return self.run(self.features.x_train,
                        self.features.y_train,
                        self.features.x_test,
                        self.features.y_test,
                        metrics,
                        params)

    def predict(self, x, y, x_test, params=True):
        """
        Wrap-up function for model create, fit and result report
        """
        self.create_model(params)
        self.fit_model(x, y)
        return self.predict_model(x_test)

    def predict_all(self, params=True):
        """
        Wrap-up function for model create, fit and result report
        """
        print('Start predicting test data set.')
        # return self.predict(self.features.train, self.features.target, self.features.test, params)
        return self.predict_model(self.features.test)

    def create_fit(self, params=True):
        self.create_model(params)
        self.fit_model(self.features.train, self.features.target)

    def cross_validation(self, x, y, metrics, k_fold, params=True):
        """
        k-fold cross-validation
        """
        test_pred = pd.DataFrame()
        kf = KFold(n_splits=k_fold, random_state=10)
        for train_index, test_index in kf.split(x):
            x_train, x_test = x.ix[train_index, :], x.ix[test_index, :]
            y_train, y_test = y[train_index], y[test_index]
            pred_fold = pd.DataFrame(self.run(x_train,
                                              y_train,
                                              x_test,
                                              y_test,
                                              metrics,
                                              params),
                                     index=test_index).add_suffix('_' + self.model_type)
            test_pred = test_pred.append(pred_fold)
        print('Overall performance:')
        self.calc_metrics(metrics, y, test_pred)
        test_pred.sort_index(inplace=True)
        return test_pred

    def cross_validation_all(self, metrics, k_fold, params=True):
        """
        k-fold cross-validation with original data-set
        """
        print('Start cross_validation for train data set.')
        return self.cross_validation(self.features.train,
                                     self.features.target,
                                     metrics,
                                     k_fold,
                                     params)

    def grid_search(self, x, y, metrics, k_fold, params):
        """
        Grid search for hyper-parameters
        """
        print('Start grid search for {}...'.format(self.model_type))
        start = time()
        grid_name = self.model_type + '_grid'
        if grid_name not in params:
            raise Exception('Parameters for grid search is not available in config.')
        self.grid_param = params[grid_name]
        pprint.pprint(self.grid_param)
        self.create_model(False)
        kf = KFold(n_splits=k_fold, random_state=10)
        grid_obj = GridSearchCV(self.model,
                                param_grid=self.grid_param,
                                scoring=metrics,
                                cv=kf.split(x))
        grid_fit = grid_obj.fit(x, y)
        print('Best parameters chosen is: {}'.format(grid_fit.best_params_))
        print('Best score is: {}'.format(grid_fit.best_score_))
        end = time()
        print('Time used for searching is {} min.'.format((end - start) / 60))
        res = pd.DataFrame(grid_obj.cv_results_)
        self.param = grid_fit.best_params_
        return res

    def grid_search_all(self, metrics, k_fold):
        """
        Grid search for original data-set
        """
        return self.grid_search(self.features.x_train,
                                self.features.y_train,
                                metrics,
                                k_fold,
                                self.model_param)

    def stacking_feature(self, metrics, k_fold):
        """
        Stack meta-features for model stacking
        """
        print('Start feature stacking for {}'.format(self.model_type))
        meta_feature_train = self.cross_validation_all(metrics, k_fold)
        meta_feature_test = self.predict_all()
        return meta_feature_train, meta_feature_test

    def calc_metrics(self, metrics, y_true, y_pred):
        """
        Model evaluation
        """
        if metrics == 'accuracy':
            print('accuracy: %f' % (accuracy_score(y_true, y_pred)))
        elif metrics == 'logloss':
            y_true_dummies = pd.get_dummies(y_true)
            print('logloss: %f' % (log_loss(y_true_dummies, y_pred)))
        elif metrics == 'mae':
            print('mean absolute error: %f' % (mean_absolute_error(y_true, y_pred)))

    def assign_df_month(self, month):
        """
        Assign month value
        """
        self.features.assign_test_month(month)

    @property
    def get_model_name(self):
        return self.model_type
