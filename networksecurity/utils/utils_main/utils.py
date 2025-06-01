import yaml
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import os,sys
import numpy as np
import dill
import pickle 
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score

def read_yaml_file(filepath: str) -> dict:
    try:
        with open(filepath,"rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    

def write_yaml_file(filepath:str,content:object,replace:bool=False)->None:
    try:
        if replace:
            if os.path.exists(filepath):
                os.remove(filepath)
        os.makedirs(os.path.dirname(filepath),exist_ok=True)
        with open(filepath, "w") as file:
            yaml.dump(content, file)
        
    except Exception as e:
        raise NetworkSecurityException(sys,e)


def save_numpy_array_data(filepath:str,array:np.array):
    try:
        dirpath = os.path.dirname(filepath)
        os.makedirs(dirpath,exist_ok=True)
        with open(filepath,"wb") as file:
            np.save(file,array)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
def saveobj(filepath:str,obj:object):
    try:
        dirpath = os.path.dirname(filepath)
        os.makedirs(dirpath,exist_ok=True)
        with open(filepath,"wb") as file:
            pickle.dump(obj,file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
def load_obj(filepath:str)-> object:
    try:
        if not os.path.exists(filepath):
            raise Exception(f"{filepath} not exists")
        with open(filepath,"rb") as file:
            print(file)
            return pickle.load(file)

        
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
def load_numpy_array_data(filepath:str)->np.array:
    try:
        with open(filepath,"rb") as file:
            return np.load(file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    

def evaluate(X_train, y_train,X_test,y_test,models,param):
    try:
        report = {}

        for i in range(len(list(models))):
            model = list(models.values())[i]
            para=param[list(models.keys())[i]]

            gs = GridSearchCV(model,para,cv=3)
            gs.fit(X_train,y_train)

            model.set_params(**gs.best_params_)
            model.fit(X_train,y_train)

            #model.fit(X_train, y_train)  # Train model

            y_train_pred = model.predict(X_train)

            y_test_pred = model.predict(X_test)

            train_model_score = accuracy_score(y_train, y_train_pred)

            test_model_score = accuracy_score(y_test, y_test_pred)

            report[list(models.keys())[i]] = test_model_score

        return report

    except Exception as e:
        raise NetworkSecurityException(e, sys)
