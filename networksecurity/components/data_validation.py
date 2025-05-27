import os
from networksecurity.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.constants.training_pipeline import SCHEMA_FILE_PATH

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.utils.utils_main.utils import read_yaml_file,write_yaml_file

## for data drift
from scipy.stats import ks_2samp

import pandas as pd
import sys


class DataValidation:
    def __init__(self,data_ingestion_arifact:DataIngestionArtifact,
                 data_validation_config:DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_arifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)

        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    @staticmethod
    def read_data(self,file_path:str)->pd.DataFrame:
        """
        Read the data from the given file path
        """
        try:
            dataframe = pd.read_csv(file_path)
            return dataframe
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def validate_number_of_columns(self,dataframe:pd.DataFrame)->bool:
        try:
            number_of_column = len(self._schema_config)
            logging.info(f"Required no of columns:{number_of_column}")
            logging.info(f"Datafram has:{len(dataframe.columns)}")
            if len(dataframe.columns)==number_of_column:
                return True
            else:
                return False
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def is_numerical_value_exist(self,dataframe:pd.DataFrame)->bool:
        if not dataframe.select_dtypes(include='number').empty:
            return True
        else:
            return False
        
    def detect_dataset_drift(self,base_df,current_df,threshold=0.05)->bool:
        try:
            status = True
            report = {}
            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]
                is_samp_dist=ks_2samp(d1,d2)
                if threshold<=is_samp_dist.pvalue:
                    is_found=False
                else:
                    is_found=True
                    status=False
                report.update(
                    {
                        column:{
                            "p_value":float(is_samp_dist.pvalue),
                            "drift_status":is_found
                        }
                    }

                )
            drift_report_path = self.data_validation_config.drif_report_file_path

            ##create directory
            dir_path = os.path.dirname(drift_report_path)
            os.makedirs(dir_path,exist_ok=True)
            
            write_yaml_file(drift_report_path,report)

            return status
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    

    def initiate_data_validation(self,)->DataValidationArtifact:
        try:
            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            ## read the data from train and test
            train_dataframe = DataValidation.read_data(self,train_file_path)
            test_dataframe = DataValidation.read_data(self,test_file_path)
            logging.info("Read train and test data successfully")

            ##validate number of columns
            status = self.validate_number_of_columns(train_dataframe)
            if not status:
                error_message = "Train dataframe does not contain all the columns \n"

            status = self.validate_number_of_columns(test_dataframe)
            if not status:
                error_message = " Test dataframe does not contain all the columns \n"

            status_num = self.is_numerical_value_exist(train_dataframe)
            if not status_num:
                error_message = "Train dataframe does not contain numerical value"

            status_num = self.is_numerical_value_exist(test_dataframe)
            if not status_num:
                error_message = "Test dataframe does not contain numerical value"

            ##lets check the datadrift
            status = self.detect_dataset_drift(train_dataframe,test_dataframe)

            train_dir = os.path.dirname(self.data_validation_config.valid_train_file_path)
            test_dir = os.path.dirname(self.data_validation_config.valid_test_file_path)

            os.makedirs(train_dir, exist_ok=True)
            os.makedirs(test_dir, exist_ok=True)

            if not status:
                train_dataframe.to_csv(self.data_validation_config.valid_train_file_path)

                test_dataframe.to_csv(self.data_validation_config.valid_test_file_path)

            data_validation_artifact = DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_ingestion_artifact.trained_file_path,
                valid_test_file_path=self.data_ingestion_artifact.test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drif_report_file_path

            )

            return data_validation_artifact

            
        except Exception as e:
            raise NetworkSecurityException(e,sys)