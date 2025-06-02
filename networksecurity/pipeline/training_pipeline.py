from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.entity.config_entity import (
    DataIngestionConfig,TrainingPipelinConfig,
    DataValidationConfig,DataTransformationConfig,
    ModelTrainerConfig
)
from networksecurity.entity.artifact_entity import (
    DataIngestionArtifact,DataValidationArtifact,
    DataTransformationArtifact,
    ModelTrainerArtifact
)

import sys


class TrainingPipeline:
    def __init__(self):
        self.traininig_pipeline_config = TrainingPipelinConfig()

    def start_data_ingestion(self):
        try:
            self.data_ingestion_config = DataIngestionConfig(training_pipeline_config=self.traininig_pipeline_config)
            logging.info("Data Ingestion Starts")
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info(f"data ingestion completed :{data_ingestion_artifact}")

            return data_ingestion_artifact

        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def start_data_validation(self,data_ingestion_artifact):
        try:
            self.data_validation_config = DataValidationConfig(training_pipeline_config=self.traininig_pipeline_config)
            logging.info("Data validation Starts")
            data_validation = DataValidation(data_ingestion_arifact=data_ingestion_artifact,data_validation_config=self.data_validation_config)
            data_validation_artifact = data_validation.initiate_data_validation()
            logging.info(f"Data validation completed:{data_validation_artifact}")
            return data_validation_artifact

        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def start_data_transfomration(self,data_validation_artifact):
        try:
            self.data_transformation_config = DataTransformationConfig(training_pipeline_config=self.traininig_pipeline_config)
            logging.info("Data transformation Starts")
            data_transformation = DataTransformation(data_validation_artifact=data_validation_artifact,data_transformation_config=self.data_transformation_config)
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            logging.info(f"Data validation completed:{data_transformation_artifact}")

            return data_transformation_artifact

        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def start_model_trainer(self,data_transformation_artifact):
        try:
            self.model_trainer_config = ModelTrainerConfig(training_pipeline_config=self.traininig_pipeline_config)
            logging.info("Model Trainer Starts")
            model_trainer = ModelTrainer(data_transformation_artifact=data_transformation_artifact,
                                         model_trainer_config= self.model_trainer_config)
            model_train_artifact =model_trainer.initiate_model_trainer()
            logging.info(f"Model Trainer completed:{model_train_artifact}")

            return model_train_artifact

        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transfomration(data_validation_artifact)
            model_trainer_artifact = self.start_model_trainer(data_transformation_artifact)
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    
        
    