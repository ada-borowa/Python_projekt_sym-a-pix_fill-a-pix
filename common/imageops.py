#!/usr/bin/env python3
""" Common image operations.
"""

import numpy as np
import math

import cv2

__author__ = 'Adriana Borowa'
__email__ = 'ada.borowa@gmail.com'

DEGREE_VERTICAL = 0          # 0 degrees
DEGREE_HORIZONTAL = 1.5708   # pi/2 degrees
EPS = 0.0001


def get_unique_lines(rhos):
    """
    Joins lines that are to close to each other.
    :param rhos: list of lines' positions
    :return: list without duplicates
    """
    rhos.sort()
    tmp = []
    it = 0
    while it < len(rhos) - 1:
        if rhos[it + 1] - rhos[it] < 10:
            tmp.append(int((rhos[it] + rhos[it+1])/2.0))
            it += 1
        else:
            tmp.append(int(rhos[it]))
        it += 1
    if rhos[-1] - tmp[-1] > 10:
        tmp.append(int(rhos[-1]))
    return tmp


def get_line_positions(img, sensitivity=100):
    """
    Using Hough transformation detects lines on image. Detects only vertical and horizontal lines.
    :param sensitivity: Hough transformation parameter
    :param img: Image
    :return: positions of horizontal and vertical lines
    """
    edges = cv2.Canny(img, 50, 150, apertureSize=3)
    lines = cv2.HoughLines(edges, 1, np.pi / 180, sensitivity)
    if lines is None:
        lines = cv2.HoughLines(edges, 1, np.pi / 180, int(sensitivity/2))

    rho_horizontal = []
    rho_vertical = []
    for row in lines:
        rho, theta = row[0]
        if math.fabs(theta - DEGREE_HORIZONTAL) < EPS:
            rho_horizontal.append(rho)
        elif math.fabs(theta - DEGREE_VERTICAL) < EPS:
            rho_vertical.append(rho)

    rho_horizontal = get_unique_lines(rho_horizontal)
    rho_vertical = get_unique_lines(rho_vertical)

    return rho_horizontal, rho_vertical
