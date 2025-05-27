import sys
import os
import numpy as np
import pandas as pd

from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from networksecurity.constants.training_pipeline import TARGET_COLUMN,DATA_TRANSFORMATION_IMPUTER_PARAMETER
from networksecurity.entity.artifact_entity import (DataValidationArtifact,
            DataTransformationArtifact)
from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.utils.utils_main.utils import save_numpy_array_data,saveobj

class DataTransformation:
    def __init__(self,data_validation_artifact:DataValidationArtifact,
                 data_transformation_config:DataTransformationConfig):
        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    @staticmethod
    def read(filename:str)->pd.DataFrame:
        try:
            return pd.read_csv(filename)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def get_data_transformer_object(cls)->Pipeline:
        """
        initialize knn imputer
        """
        logging.info("Entered get_data_transformer_object method of Transformation class")
        try:
            ## imputer for missing value
            imputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMETER)

            logging.info(f"Initialize knn imputer with {DATA_TRANSFORMATION_IMPUTER_PARAMETER} parameters")

            processor:Pipeline = Pipeline([("imputer",imputer)])

            return processor

        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def initiate_data_transformation(self)->DataTransformationArtifact:
        logging.info("Entering into datatransformation of class of DataTransformation")
        try:
            logging.info("starting data transformation")
            train_df = DataTransformation.read(self.data_validation_artifact.valid_train_file_path)
            test_df = DataTransformation.read(self.data_validation_artifact.valid_test_file_path)

            input_train_df = train_df.drop(columns=[TARGET_COLUMN],axis=1)
            train_target_df = train_df[TARGET_COLUMN]
            train_target_df = train_target_df.replace(-1,0)

            input_test_df = test_df.drop(columns=[TARGET_COLUMN],axis=1)
            test_target_df = test_df[TARGET_COLUMN]
            test_target_df = test_target_df.replace(-1,0)

            preprocessor = self.get_data_transformer_object()

            preprocessor_obj = preprocessor.fit(input_train_df)
            transformed_input_train = preprocessor_obj.transform(input_train_df)
            transformed_input_test = preprocessor_obj.transform(input_test_df)

            train_arr = np.c_[transformed_input_train,np.array(train_target_df)]
            test_arr = np.c_[transformed_input_test,np.array(test_target_df)]

            #save numpy array

            save_numpy_array_data(self.data_transformation_config.data_transformed_train_file_path,train_arr)
            save_numpy_array_data(self.data_transformation_config.data_transformed_test_file_path,test_arr)

            ## save the object(preprocessr)

            saveobj(self.data_transformation_config.data_transformed_object_file_path,preprocessor_obj)


            ## artifacts

            data_transformation_artifact = DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.data_transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.data_transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.data_transformed_test_file_path,
            )

            return data_transformation_artifact
            

            
        except Exception as e:
            raise NetworkSecurityException(e,sys)

        