from networksecurity.components.data_ingestion import DataIngestion

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.entity.config_entity import DataIngestionConfig,TrainingPipelinConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact

import sys

if __name__ == '__main__':
    try:
        training_pipline = TrainingPipelinConfig()
        dataingestionconfig = DataIngestionConfig(training_pipline)
        dataingestion = DataIngestion(dataingestionconfig)

        logging.info("Initiate the data ingestion")

        data_ingestion_artifact = dataingestion.initiate_data_ingestion()

        print(data_ingestion_artifact)

    except Exception as e:
        raise NetworkSecurityException(e, sys)