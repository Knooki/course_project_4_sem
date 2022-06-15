from django.shortcuts import render, redirect
from .models import LANGUAGES, Product, Course
from django.views.generic import DetailView

import numpy as np
import math

LANGUAGES = [
    'Python',
    'C#'
    'C\C++',
    'Frontend',
    'Java',
]
LOW_DEMAND = [
    1600,
    1700,
    2100,
    1500,
    1800,
]
AVERAGE_DEMAND = [
    1800,
    2300,
    2400,
    1700,
    2000,
]
HIGH_DEMAND = [
    2200,
    2500,
    3500,
    2000,
    2700,
]

RAW_MATRIX = [
    [ 1600,1800,2200],
    [1700, 2300, 2500],
    [2100, 2400, 3500],
    [1500, 1700, 2000],
    [1800, 2000, 2700],
]


def result_str(number_station, crit):
    return 'Технология {}.'.format(number_station)


def help_with_choice(request):
    context = {'wald':wald(), 'maximax':maximax(),'laplace':laplace(),'hurwitz_mod':hurwitz_mod()}
    return render(request, 'catalog/help_with_choice.html', context)


def wald():
    matrix = np.array(RAW_MATRIX)
    vector_of_mins = matrix.min(axis=1)
    number_tech = vector_of_mins.argmax() + 1
    crit = vector_of_mins.max()
    return result_str(number_tech, crit)


def maximax():
    matrix = np.array(RAW_MATRIX)
    vector_of_maxes = matrix.max(axis=1)
    number_station = vector_of_maxes.argmax() + 1
    crit = vector_of_maxes.max()
    return result_str(number_station, crit)


def laplace():
    matrix = np.array(RAW_MATRIX)
    vector_of_averages = matrix.mean(axis=1)
    number_station = vector_of_averages.argmax() + 1
    crit = vector_of_averages.max()
    return result_str(number_station    -1, crit)

def hurwitz_mod():
    matrix = np.array(RAW_MATRIX)
    vector_of_mins = matrix.min(axis=1)
    wald_crit = vector_of_mins.max()
    vector_of_averages = matrix.mean(axis=1)
    f_crit = wald_crit * 0.6 
    bool_vector_of_alternatives = vector_of_averages <= f_crit ### so we don't lose the numbering
    vector_of_averages[bool_vector_of_alternatives] = -math.inf ### 
    number_station = vector_of_averages.argmax() + 1
    crit = vector_of_averages.max()
    return result_str(number_station+1, crit)