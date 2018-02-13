from functools import reduce


def subtract_vector(v1, v2):
    return (v1[0] - v2[0], v1[1] - v2[1])


def translate_vector(v1, v2):
    return (v1[0] + v2[0], v1[1] + v2[1])


def average_list_of_vectors(l):
    sum_vector = reduce(lambda x, y: translate_vector(x, y), l)
    return (int(sum_vector[0] / len(l)), int(sum_vector[1] / len(l)))
