import os

import sys
import os
import numpy as np
import pandas as pd

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import ModelTrainerConfig
from networksecurity.entity.artifact_entity import DataTransformationArtifact,ModelTrainerArtifact

from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from networksecurity.utils.ml_utils.metric.classification_metric import get_classification_report
from networksecurity.utils.utils_main.utils import saveobj,load_obj,load_numpy_array_data,evaluate


from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import(
AdaBoostClassifier,
GradientBoostingClassifier,
RandomForestClassifier
)

import mlflow
import sklearn

class ModelTrainer:
    def __init__(self,model_trainer_config:ModelTrainerConfig,data_transformation_artifact:DataTransformationArtifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact

        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def track_mlflow(self,best_model,classification_metric):
        with mlflow.start_run():
            f1_score = classification_metric.f1_score
            precission_score = classification_metric.precission_score
            recall_score = classification_metric.recall_score

            mlflow.log_metric("fl_score",f1_score)
            mlflow.log_metric("precission_score",precission_score)
            mlflow.log_metric("recall_score",recall_score)
            mlflow.sklearn.log_model(best_model,"model")

        
    def train_model(self,x_train,y_train,x_test,y_test):
        
        models = {
            "Random Forest" : RandomForestClassifier(verbose=1),
            "Decision Tree" : DecisionTreeClassifier(),
            "Gradient Boosting" : GradientBoostingClassifier(verbose=1),
            "Logistic Regression" : LogisticRegression(verbose=1),
            "AdaBoost" : AdaBoostClassifier()
        }

        params={
            "Decision Tree": {
                'criterion':['gini', 'entropy', 'log_loss'],
                # 'splitter':['best','random'],
                # 'max_features':['sqrt','log2'],
            },
            "Random Forest":{
                # 'criterion':['gini', 'entropy', 'log_loss'],
                
                # 'max_features':['sqrt','log2',None],
                'n_estimators': [8,16,32,128,256]
            },
            "Gradient Boosting":{
                # 'loss':['log_loss', 'exponential'],
                'learning_rate':[.1,.01,.05,.001],
                'subsample':[0.6,0.7,0.75,0.85,0.9],
                # 'criterion':['squared_error', 'friedman_mse'],
                # 'max_features':['auto','sqrt','log2'],
                'n_estimators': [8,16,32,64,128,256]
            },
            "Logistic Regression":{},
            "AdaBoost":{
                'learning_rate':[.1,.01,.001],
                'n_estimators': [8,16,32,64,128,256]
            }
            
        }

        model_report:dict = evaluate(x_train,y_train,x_test,y_test,models,params)

        best_model_score = max(sorted(model_report.values()))

        best_model = list(model_report.keys())[
            list(model_report.values()).index(best_model_score)]
        
        best_model = models[best_model]

        y_train_pred = best_model.predict(x_train)

        classification_train_metric = get_classification_report(y_train_pred,y_train)

        ## track the mlflow
        self.track_mlflow(best_model,classification_train_metric)

        y_test_pred = best_model.predict(x_test)

        classification_test_metric = get_classification_report(y_test_pred,y_test)

        ## track the mlfow

        self.track_mlflow(best_model,classification_test_metric)

        ## laod the preprocessor cause that also in the model trainer artifact

        preprocessor = load_obj(self.data_transformation_artifact.transformed_object_file_path)

        model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)

        os.makedirs(model_dir_path,exist_ok=True)

        Network_model = NetworkModel(preprocessor=preprocessor,model=best_model)

        saveobj(self.model_trainer_config.trained_model_file_path,obj=Network_model)

        model_trainer_artifact = ModelTrainerArtifact(trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                             train_metric_artifact=classification_train_metric,
                             test_metric_artifact=classification_test_metric)
        
        logging.info(f"Model Trainer artifact: {model_trainer_artifact}")

        return model_trainer_artifact
        
    def initiate_model_trainer(self)->ModelTrainerArtifact:
        try:
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path

            ##load train and test

            train_arr = load_numpy_array_data(train_file_path)
            test_arr = load_numpy_array_data(test_file_path)

            x_train,y_train,x_test,y_test = (
                train_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,:-1],
                test_arr[:,-1]
            )

            model_trainer_artifact = self.train_model(x_train,y_train,x_test,y_test)

            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        