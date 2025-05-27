from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.entity.config_entity import DataIngestionConfig,TrainingPipelinConfig,DataValidationConfig,DataTransformationConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact

import sys

if __name__ == '__main__':
    try:
        training_pipline = TrainingPipelinConfig()
        dataingestionconfig = DataIngestionConfig(training_pipline)
        dataingestion = DataIngestion(dataingestionconfig)

        logging.info("Initiate the data ingestion")
        data_ingestion_artifact = dataingestion.initiate_data_ingestion()
        logging.info("Data initiation Completed")

        print("Data Ingestion:",data_ingestion_artifact,"\n")

        data_validation_config = DataValidationConfig(training_pipline)
        data_validatiion = DataValidation(data_ingestion_artifact,data_validation_config)

        logging.info("initiate the data validation config")

        data_validation_artifact = data_validatiion.initiate_data_validation()

        logging.info("Data validation completed")

        print("Data Validation",data_validation_artifact,"\n")

        data_transformation_config = DataTransformationConfig(training_pipline)

        data_transformation = DataTransformation(data_validation_artifact,data_transformation_config)

        data_transformation_artifact = data_transformation.initiate_data_transformation()
        
        logging.info("Data Transformation is completed")

        print("Data Transformation",data_transformation_artifact,"\n")

    except Exception as e:
        raise NetworkSecurityException(e, sys)