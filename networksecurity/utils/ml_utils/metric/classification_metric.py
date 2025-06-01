from sklearn.metrics import f1_score,precision_score,recall_score
from networksecurity.entity.artifact_entity import ClassificationMetricArtifact
from networksecurity.exception.exception import NetworkSecurityException

import sys

def get_classification_report(y_pred,y_test)->ClassificationMetricArtifact:
    try:
        model_f1_score = f1_score(y_pred,y_test)
        model_precission_score = precision_score(y_pred,y_test)
        model_recall_score = recall_score(y_pred,y_test)

        classification_metric = ClassificationMetricArtifact(
            model_f1_score,
            model_precission_score,
            model_recall_score
        )

        return classification_metric

    except Exception as e:
        raise NetworkSecurityException(e,sys)