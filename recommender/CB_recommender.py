# -*- coding: utf-8 -*-
import numpy as np

def recommend_locations_CB(LLM, ULM, u, locations, k, num_recommendations, OUTPUT=False):
    """
    :param LLM: location-location matrix
    :param ULM: location-user matrix
    :param u: user to recommend for
    :param locations: list of location names
    :param k: number of k nearest neighbors
    :param num_recommendations: number of recommendations to give
    :param OUTPUT: boolean wich states whether there should be console output
    :return: list of indices of the recommended locations
    """

    loc_vec = ULM[u, :]
    loc_vec_non_zeros = np.nonzero(loc_vec)[0]

    # if user rated any places
    if(len(loc_vec_non_zeros)):
        # holds all nearest neighbors of the locations the user liked
        nearest_neighbors = []
        for location in loc_vec_non_zeros:
            location_sims = np.argsort(LLM[location, :])

            # k closest locations to the location
            k_locations = location_sims[-1-k:-1]
            nearest_neighbors.extend(k_locations)

        nearest_neighbors_unique = np.unique(nearest_neighbors)

        # calc sum of all similarity values, put them in one array and sort them
        sum_idx = LLM[loc_vec_non_zeros, :].sum(axis=0)

        # set all locations' sim to 0, if location is not in nn's
        for i in range(0, sum_idx.size):
            if i not in nearest_neighbors_unique:
                sum_idx[i] = 0
        sort_idx = np.argsort(sum_idx)

        highest_similarities = sort_idx[-num_recommendations:]

        if OUTPUT:
            locations_array = np.asarray(locations)
            print
            "Content Based Recommender - Names of the " + str(len(highest_similarities)) + " recommended locations: ", locations_array[
                highest_similarities]
        return highest_similarities

    else:
        # implement fallback
        return []