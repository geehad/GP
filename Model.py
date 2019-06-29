# -*- coding: utf-8 -*-
"""
@author: Berlnty
"""
import numpy as np
import math


class Model:
    matrix = np.zeros((0, 0, 0))
    least_p = []
    max_p = []
    dx = 0
    dy = 0
    dz = 0
    shape = 0
    freepixels = 0
    h_y = None
    inner_o_p = [-1, -1, -1]
    inner_m_p = [-1, -1, -1]

    def __init__(self, x, y, z, mat, h):

        self.dx = x - 1
        self.dy = y - 1
        self.dz = z - 1
        self.shape = self.dx * self.dy * self.dz
        self.max_p = [self.dx, self.dy, self.dz]
        self.least_p = [0, 0, 0]
        self.matrix = mat
        self.h_y = h
        self.calc_freespace()

    def update_terminals(self, x, y, z):
        self.least_p = [x, y, z]
        self.max_p = [self.dx + x, self.dy + y, self.dz + z]

    def calc_freespace(self):
        for i in range(0, self.dx):
            for k in range(0, self.dy):
                for e in range(0, self.dz):
                    if (self.matrix[i][k][e] == 0): self.freepixels += 1

    def get_inner_dim(self):

        centre = [int(math.ceil(self.dx / 2)), int(math.ceil(self.dy / 2)), int(math.ceil(self.dz / 2))]

        for x in range(centre[0], self.dx):
            if (self.matrix[x][centre[1]][centre[2]] == 0):
                self.inner_m_p[0] = x
            else:
                break

        for x in reversed(range(centre[0])):
            if (self.matrix[x][centre[1]][centre[2]] == 0):
                self.inner_o_p[0] = x
            else:
                break

        for y in range(centre[1], self.dy):
            if (self.matrix[centre[0]][y][centre[2]] == 0):
                self.inner_m_p[1] = y
            else:
                break

        for y in reversed(range(centre[1])):
            if (self.matrix[centre[0]][y][centre[2]] == 0):
                self.inner_o_p[1] = y
            else:
                break

        for z in range(centre[1], self.dz):
            if (self.matrix[centre[0]][centre[1]][z] == 0):
                self.inner_m_p[2] = z
            else:
                break

        for z in reversed(range(centre[2])):
            if (self.matrix[centre[0]][centre[1]][z] == 0):
                self.inner_o_p[2] = z
            else:
                break


class object:
    name = None
    model = None
    left = []
    right = []
    front = []
    back = []
    base = None
    setteled = 0
    tx = 0
    tz = 0

    def __init__(self, n):
        self.name = n
        self.left = []
        self.right = []
        self.front = []
        self.back = []
        return