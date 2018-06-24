import json
import numpy as np
from sklearn import cross_validation
import CB_recommender as CB

def evaluate_recommender(Rec_name, NF, ULM, LLM, locations, u, k, num_recommendations_array, OUTPUT=False):
    """
    :param Rec_name: Recommender name as String
    :param NF: number of folds to do in cross validation
    :param ULM: user-location matrix
    :param LLM: location-location matrix
    :param locations:
    :param u: user to recommend for
    :param users:
    :param k:
    :param num_recommendations_array:
    :param OUTPUT:
    :return:
    """
    max_number_of_recommendations = max(num_recommendations_array)

    # idx of locations the user liked
    u_location_idx = np.nonzero(ULM[u, :])[0]

    # average precision and recall for this user
    average_rec_prec = {'recall': [], 'precision': []}

    # # if the user liked too less locations
    # if len(u_location_idx) < 10:
    #     for num_recommendations in num_recommendations_array:
    #         # return 100 for precision and recall, by definition
    #         average_rec_prec[num_recommendations] = np.array([100.0, 100.0])
    #     return average_rec_prec


    # split locations into train and test for cross-fold
    kf = cross_validation.KFold(len(u_location_idx), n_folds=NF)

    fold_averages = {'recall': [], 'precision': []}

    # for each fold
    for _, relevants in kf:
        copy_ULM = ULM.copy()
        location_idx_test = u_location_idx[relevants]

        copy_ULM[u, location_idx_test] = 0.0
        recommended_locations_idx = []

        if Rec_name == "CB":
            recommended_locations_idx = CB.recommend_locations_CB(LLM, copy_ULM, u, locations, k, max_number_of_recommendations, OUTPUT=False)
        elif Rec_name == "CF":
            recommended_locations_idx = []

        single_values = {'recall': [], 'precision': []}

        # for each number of requested recommendations
        for num_recommendations in num_recommendations_array:
            recommendations = recommended_locations_idx[-num_recommendations:]
            TP_values = np.intersect1d(u_location_idx[relevants], recommendations)
            TP = len(TP_values)

            # calculate precision and recall per fold
            if len(recommendations) == 0:
                single_precision = 100.0
            else:
                single_precision = 100.0 * TP / len(recommendations)

            if len(relevants) == 0:
                single_recall = 100.0
            else:
                single_recall = 100.0 * TP / len(relevants)

            single_values['recall'] += [single_recall]
            single_values['precision'] += [single_precision]

        fold_averages['recall'] += [sum([v for v in single_values['recall']])/max_number_of_recommendations]
        fold_averages['precision'] += [sum([v for v in single_values['precision']])/max_number_of_recommendations]


    # divide by number of folds to get average
    average_rec_prec['recall'] = sum([f for f in fold_averages['recall']])/NF
    average_rec_prec['precision'] = sum([f for f in fold_averages['precision']])/NF

    if OUTPUT:
        print('TP: ', TP, ' | Recall: ' + str(average_rec_prec['recall']) + ' | Precision: ' + str(average_rec_prec['precision']))

    return average_rec_prec



#### testing the evaluation
if __name__ == '__main__':

    NF = 5
    LLM = CB.load_matrix('data/LLM')
    locations = []
    with open('data/test_json.txt', encoding='utf-8') as json_file:
        data = json.load(json_file)
        for l in data['results']:
            locations += [l['name']]
    ULM = np.ones(shape=(15, 8), dtype=np.float32)
    u = 1
    k = 3
    num_recommendations_array = range(0,5)

    evaluate_recommender('CB', NF, ULM, LLM, locations, u, k, num_recommendations_array, OUTPUT=True)