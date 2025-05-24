import yaml
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import os,sys
import numpy as np
import dill
import pickle 

def read_yaml_file(filepath: str) -> dict:
    try:
        with open(filepath,"rb") as yaml_file:
            return yaml.safe_dump(yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
