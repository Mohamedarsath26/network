from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.entity.config_entity import DataIngestionConfig,TrainingPipelinConfig,DataValidationConfig
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

        data_validation_config = DataValidationConfig(training_pipline)
        data_validatiion = DataValidation(data_ingestion_artifact,data_validation_config)

        logging.info("initiate the data validation config")

        data_validation_artifact = data_validatiion.initiate_data_validation()

        logging.info("Data validation completed")

        print(data_validation_artifact)
        

    except Exception as e:
        raise NetworkSecurityException(e, sys)