import pandas as pd
import numpy as np
from sklearn.metrics import confusion_matrix, f1_score, cohen_kappa_score, accuracy_score


def calc_metrics(predictions: np.array, instance_labels: np.array, bag_labels_per_instance:np.array ,
                 bag_names_per_instance: np.array, model_name: str):

    confusion_mat = confusion_matrix(instance_labels, predictions)
    metrics = pd.DataFrame(index=['recall', 'precision', 'accuracy', 'f1_score', 'cohens_kappa'], columns=[model_name])

    metrics.loc['recall', model_name] = round(confusion_mat[0][0] / (confusion_mat[0][0] + confusion_mat[1][0]), 3)
    metrics.loc['precision', model_name] = round(confusion_mat[0][0] / (confusion_mat[0][0] + confusion_mat[0][1]), 3)
    metrics.loc['accuracy', model_name] = round((confusion_mat[0][0] + confusion_mat[1][1]) / (
                confusion_mat[0][0] + confusion_mat[1][0] + confusion_mat[0][1] +
                confusion_mat[1][1]), 3)
    metrics.loc['f1_score', model_name] = round(f1_score(instance_labels, predictions), 3)
    metrics.loc['cohens_kappa', model_name] = round(cohen_kappa_score(instance_labels, predictions), 3)

    # calculate bag level metrics
    bag_f1_score, bag_cohens_kappa, bag_accuracy = calc_bag_level_metrics(predictions, bag_labels_per_instance, bag_names_per_instance)
    metrics.loc['bag_accuracy', model_name] = round(bag_accuracy, 3)
    metrics.loc['bag_f1_score', model_name] = round(bag_f1_score, 3)
    metrics.loc['bag_cohens_kappa', model_name] = round(bag_cohens_kappa, 3)

    return metrics


def calc_bag_level_metrics(predictions: np.array, bag_labels_per_instance:np.array, bag_names_per_instance: np.array):
    bag_names = np.unique(bag_names_per_instance)

    bag_predictions = []
    bag_gt = []
    for bag_name in bag_names:
        bag_indices = (bag_names_per_instance == bag_name)
        bag_instance_predictions = predictions[bag_indices]
        bag_predicted_label = int(np.any(bag_instance_predictions > 0.5)) # positive if one pred positive

        bag_gt_label = np.unique(bag_labels_per_instance[bag_indices])
        assert len(bag_gt_label) == 1 # make sure all bag labels are the same for one bag

        bag_predictions.append(bag_predicted_label)
        bag_gt.append(bag_gt_label)

    bag_predictions = np.array(bag_predictions)
    bag_gt = np.array(bag_gt)

    bag_accuracy = accuracy_score(bag_gt, bag_predictions)
    bag_f1_score = f1_score(bag_gt, bag_predictions)
    bag_cohens_kappa = cohen_kappa_score(bag_gt, bag_predictions)

    return bag_f1_score, bag_cohens_kappa, bag_accuracy





