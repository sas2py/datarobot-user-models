import pickle
import pandas as pd
import numpy as np

from datarobot_drum.drum.common import (
    PythonArtifacts,
    REGRESSION_PRED_COLUMN,
    TargetType,
    extra_deps,
    SupportedFrameworks,
)
from datarobot_drum.drum.exceptions import DrumCommonException
from datarobot_drum.drum.artifact_predictors.artifact_predictor import ArtifactPredictor


class SAS2PYPredictor(ArtifactPredictor):
    def __init__(self):
        super(SAS2PYPredictor, self).__init__(
            SupportedFrameworks.SAS2PY, PythonArtifacts.PKL_EXTENSION
        )

    def framework_requirements(self):
        return extra_deps[SupportedFrameworks.SAS2PY]

    def is_framework_present(self):
        try:
            from sklearn.base import BaseEstimator

            return True
        except ImportError as e:
            return False

    def can_load_artifact(self, artifact_path):
        return self.is_artifact_supported(artifact_path)

    def load_model_from_artifact(self, artifact_path):
        with open(artifact_path, "rb") as picklefile:
            try:
                model = pickle.load(picklefile, encoding="latin1")
            except TypeError:
                model = pickle.load(picklefile)
            return model

    def can_use_model(self, model):
        if not self.is_framework_present():
            return False
        print('hello')
        # from sklearn.base import BaseEstimator
        print(model)
        try:
            is_sas2py = model['framework'] == 'sas2py'
        except:
            is_sas2py = False

        if type(model) is dict and is_sas2py:
            return True
        else:
            return False

    def predict(self, data, model, **kwargs):
        # checking if positive/negative class labels were provided
        # done in the base class
        super(SAS2PYPredictor, self).predict(data, model, **kwargs)

        predictions = data[data.columns[:1]]
        for col in predictions.columns:
            predictions[col] = predictions[col].apply(lambda x: x * 0)
        predictions.columns = ['Predictions']
        return predictions

        # if self.target_type.value in TargetType.CLASSIFICATION.value:
        #     if hasattr(model, "classes_"):
        #         if set(str(label) for label in model.classes_) != set(
        #             str(label) for label in self.class_labels
        #         ):
        #             error_message = "Wrong class labels {}. Use class labels detected by SAS2PY model: {}".format(
        #                 self.class_labels, model.classes_
        #             )
        #             raise DrumCommonException(error_message)
        #         labels_to_use = model.classes_
        #     else:
        #         labels_to_use = self.class_labels
        #     predictions = model.predict_proba(data)
        #     if predictions.shape[1] == 1:
        #         if self.target_type == TargetType.MULTICLASS:
        #             raise DrumCommonException(
        #                 "Target type '{}' predictions must return the "
        #                 "probability distribution for all class labels".format(self.target_type)
        #             )
        #         predictions = np.concatenate((1 - predictions, predictions), axis=1)
        #     if predictions.shape[1] != len(labels_to_use):
        #         raise DrumCommonException(
        #             "Target type '{}' predictions must return the "
        #             "probability distribution for all class labels. "
        #             "Expected {} columns, but recieved {}".format(
        #                 self.target_type, len(labels_to_use), predictions.shape[1]
        #             )
        #         )
        #     predictions = pd.DataFrame(predictions, columns=labels_to_use)
        # elif self.target_type in [TargetType.REGRESSION, TargetType.ANOMALY]:
        #     predictions = pd.DataFrame(
        #         [float(prediction) for prediction in model.predict(data)],
        #         columns=[REGRESSION_PRED_COLUMN],
        #     )
        # else:
        #     raise DrumCommonException(
        #         "Target type '{}' is not supported by '{}' predictor".format(
        #             self.target_type.value, self.__class__.__name__
        #         )
        #     )
        # for col in predictions.columns:
        #     predictions[col] = predictions[col].apply(lambda x: x * 0)
        
        # return predictions
