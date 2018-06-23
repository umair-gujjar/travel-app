# -*- coding: utf-8 -*-
import numpy as np

def recommend_locations_CB(LLM, ULM, u, locations, k, num_recommendations, OUTPUT=False):
    """
    :param LLM: location-location matrix
    :param ULM: location-user matrix
    :param u: user to recommend for
    :param locations:
    :param k:
    :param num_recommendations:
    :param OUTPUT:
    :return:
    """

    loc_vec = ULM[u, :]
    loc_vec_non_zeros = np.nonzero(loc_vec)[0]

    # if user rated any places
    if(len(loc_vec_non_zeros)):
        # recommend
    else:
        # implement fallback
        return []