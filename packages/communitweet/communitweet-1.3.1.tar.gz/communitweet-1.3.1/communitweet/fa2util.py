# This file allows separating the most CPU intensive routines from the
# main code.  This allows them to be optimized with Cython.  If you
# don't have Cython, this will run normally.  However, if you use
# Cython, you'll get speed boosts from 10-100x automatically.
#
# The only catch is that IF YOU MODIFY THIS FILE, YOU MUST ALSO MODIFY
# fa2util.pyd TO REFLECT ANY CHANGES IN FUNCTION DEFINITIONS!
#
# Copyright 2016 Max Shinn <mws41@cam.ac.uk>
#
# Available under the GPLv3

"""
Author: Max Shinn 2016
Modified on 20.4.17, Lenz Baumann
E-Mail: lnzbmnn@gmail.com
"""

from math import sqrt
from math import log


# This will substitute for the nLayout object
class Node:
    def __init__(self):
        self.mass = 0
        self.old_dx = 0
        self.old_dy = 0
        self.dx = 0
        self.dy = 0
        self.x = 0
        self.y = 0
        self.size = 0


# This is not in the original java code, but it makes it easier to
# deal with edges.
class Edge:
    def __init__(self):
        self.node1 = -1
        self.node2 = -1
        self.weight = 0


class Region:
    def __init__(self, nodes):
        self.mass = 0
        self.mass_center_x = 0
        self.mass_center_y = 0
        self.nodes = (Node)
        nodes
        self.subregions = []
        self.size = 0
        self.update_mass_and_geometry()

    def update_mass_and_geometry(self):
        if len(self.nodes) > 1:
            mass = 0
            mass_sum_y = 0
            mass_sum_x = 0
            for node in self.nodes:
                mass += node.mass
                mass_sum_x += node.x * node.mass
                mass_sum_y += node.y * node.mass

            mass_center_x = mass_sum_x / mass
            mass_center_y = mass_sum_y / mass

            for node in self.nodes:
                distance = sqrt((node.x - mass_center_x) * (node.x - mass_center_x) +
                                (node.y - mass_center_y) * (node.y - mass_center_y))
                size = max(size, 2 * distance)

    def build_subregions(self):
        if len(self.nodes) > 1:
            left_nodes = []
            right_nodes = []

            for node in self.nodes:
                if node.x < self.mass_center_x:
                    left_nodes.append(node)
                else:
                    right_nodes.append(node)

            top_left_nodes = []
            bottom_left_nodes = []
            for node in left_nodes:
                if node.y < self.mass_center_y:
                    top_left_nodes.append(node)
                else:
                    bottom_left_nodes.append(node)

            top_right_nodes = []
            bottom_right_nodes = []
            for node in right_nodes:
                if node.y < self.mass_center_y:
                    top_right_nodes.append(node)
                else:
                    bottom_right_nodes.append(node)


            if len(top_left_nodes) > 0:
                if len(top_right_nodes) < len(self.nodes):
                    self.subregions.append(Region(top_left_nodes))
                else:
                    for node in top_left_nodes:
                        one_node_list = []
                        one_node_list.append(node)
                        self.subregions.append(Region(one_node_list))
            if len(bottom_left_nodes) > 0:
                if len(bottom_left_nodes) < len(self.nodes):
                    self.subregions.append(Region(bottom_left_nodes))
                else:
                    for node in bottom_left_nodes:
                        one_node_list = []
                        one_node_list.append(node)
                        self.subregions.append(Region(one_node_list))
            if len(top_right_nodes) > 0:
                if len(top_right_nodes) < len(self.nodes):
                    self.subregions.append(Region(top_right_nodes))
                else:
                    for node in top_right_nodes:
                        one_node_list = []
                        one_node_list.append(node)
                        self.subregions.append(Region(one_node_list))
            if len(bottom_right_nodes) > 0:
                if len(bottom_right_nodes) < len(self.nodes):
                    self.subregions.append(Region(bottom_right_nodes))
                else:
                    for node in bottom_right_nodes:
                        one_node_list = []
                        one_node_list.append(node)
                        self.subregions.append(Region(one_node_list))

            for region in self.subregions:
                region.build_subregions()





# Here are some functions from ForceFactor.java
# =============================================

# Repulsion function.  `n1` and `n2` should be nodes.  This will
# adjust the dx and dy values of `n1` (and optionally `n2`).  It does
# not return anything.
def linRepulsion(n1, n2, coefficient):
    xDist = n1.x - n2.x
    yDist = n1.y - n2.y
    distance = xDist * xDist + yDist * yDist  # Distance squared

    if distance > 0:
        factor = coefficient * n1.mass * n2.mass / distance
        n1.dx += xDist * factor
        n1.dy += yDist * factor
        n2.dx -= xDist * factor
        n2.dy -= yDist * factor


def linRepulsion_anticollision(n1, n2, coefficient):
    xDist = n1.x - n2.x
    yDist = n1.y - n2.y
    # distance = sqrt(xDist * xDist + yDist * yDist)
    # distance2 = distance - n1.size - n2.size
    distance = sqrt(xDist * xDist + yDist * yDist) - n1.size - n2.size


    if distance > 0:
        factor = coefficient * n1.mass * n2.mass / (distance * distance)
        n1.dx += xDist * factor
        n1.dy += yDist * factor
        n2.dx -= xDist * factor
        n2.dy -= yDist * factor
    elif distance < 0:
        factor = 1 * coefficient * n1.mass * n2.mass
        n1.dx += xDist * factor
        n1.dy += yDist * factor
        n2.dx -= xDist * factor
        n2.dy -= yDist * factor


# Gravity repulsion function.  For some reason, gravity was included
# within the linRepulsion function in the original gephi java code,
# which doesn't make any sense (considering a. gravity is unrelated to
# nodes repelling each other, and b. gravity is actually an
# attraction).
def linGravity(n, g, coefficient):
    xDist = n.x
    yDist = n.y
    distance = sqrt(xDist * xDist + yDist * yDist)

    if distance > 0:
        factor = coefficient * n.mass * g / distance
        n.dx -= xDist * factor
        n.dy -= yDist * factor


def linGravity_anticollision(n, g, coefficient):
    xDist = n.x
    yDist = n.y
    distance = sqrt(xDist * xDist + yDist * yDist)

    if distance > 0:
        factor = coefficient * n.mass * g / distance
        n.dx -= xDist * factor
        n.dy -= yDist * factor


# Strong gravity force function.  `n` should be a node, and `g`
# should be a constant by which to apply the force.
def strongGravity(n, g, coefficient):
    xDist = n.x
    yDist = n.y

    if xDist != 0 and yDist != 0:
        factor = coefficient * n.mass * g
        n.dx -= xDist * factor
        n.dy -= yDist * factor


# Attraction function.  `n1` and `n2` should be nodes.  This will
# adjust the dx and dy values of `n1` (and optionally `n2`).  It does
# not return anything.
def linAttraction(n1, n2, e, coefficient):
    xDist = n1.x - n2.x
    yDist = n1.y - n2.y
    factor = -coefficient * e
    n1.dx += xDist * factor
    n1.dy += yDist * factor
    n2.dx -= xDist * factor
    n2.dy -= yDist * factor


def linAttraction_anticollision(n1, n2, e, coefficient):
    xDist = n1.x - n2.x
    yDist = n1.y - n2.y
    distance = sqrt(xDist * xDist + yDist * yDist) - n1.size - n2.size

    if (distance > 0):
        factor = -coefficient * e
        n1.dx += xDist * factor
        n1.dy += yDist * factor
        n2.dx -= xDist * factor
        n2.dy -= yDist * factor

def logAttraction(n1, n2, e, coefficient):
    xDist = n1.x - n2.x
    yDist = n1.y - n2.y
    distance = sqrt(xDist * xDist + yDist * yDist)

    if (distance > 0):
        factor = -coefficient * e * log(1 + distance) / distance
        n1.dx += xDist * factor
        n1.dy += yDist * factor
        n2.dx -= xDist * factor
        n2.dy -= yDist * factor


def logAttraction_anticollision(n1, n2, e, coefficient):
    xDist = n1.x - n2.x
    yDist = n1.y - n2.y
    distance = sqrt(xDist * xDist + yDist * yDist) - n1.size - n2.size

    if (distance > 0):
        factor = -coefficient * e * log(1 + distance) / distance
        n1.dx += xDist * factor
        n1.dy += yDist * factor
        n2.dx -= xDist * factor
        n2.dy -= yDist * factor


# The following functions iterate through the nodes or edges and apply
# the forces directly to the node objects.  These iterations are here
# instead of the main file because Python is slow with loops.  Where
# relevant, they also contain the logic to select which version of the
# force function to use.
def apply_repulsion(nodes, coefficient, adjustSizes):
    if adjustSizes:
        for i in range(0, len(nodes)):
            for j in range(0, i):
                linRepulsion_anticollision(nodes[i], nodes[j], coefficient)
    else:
        for i in range(0, len(nodes)):
            for j in range(0, i):
                linRepulsion(nodes[i], nodes[j], coefficient)


def apply_gravity(nodes, gravity, scalingRatio, useStrongGravity, adjustSizes):
    if adjustSizes:
        if not useStrongGravity:
            for i in range(0, len(nodes)):
                linGravity_anticollision(nodes[i], gravity / scalingRatio, scalingRatio)
        else:
            for i in range(0, len(nodes)):
                strongGravity(nodes[i], gravity / scalingRatio, scalingRatio)
    else:
        if not useStrongGravity:
            for i in range(0, len(nodes)):
                linGravity(nodes[i], gravity / scalingRatio, scalingRatio)
        else:
            for i in range(0, len(nodes)):
                strongGravity(nodes[i], gravity / scalingRatio, scalingRatio)


def apply_attraction(nodes, edges, coefficient, edgeWeightInfluence, adjustSizes, linlogMode):
    if linlogMode:
        if adjustSizes:
            if edgeWeightInfluence == 0:
                for edge in edges:
                    logAttraction_anticollision(nodes[edge.node1], nodes[edge.node2], 1, coefficient)
            elif edgeWeightInfluence == 1:
                for edge in edges:
                    logAttraction_anticollision(nodes[edge.node1], nodes[edge.node2], edge.weight, coefficient)
            else:
                for edge in edges:
                    logAttraction_anticollision(nodes[edge.node1], nodes[edge.node2],
                                                pow(edge.weight, edgeWeightInfluence), coefficient)
        else:
            if edgeWeightInfluence == 0:
                for edge in edges:
                    logAttraction(nodes[edge.node1], nodes[edge.node2], 1, coefficient)
            elif edgeWeightInfluence == 1:
                for edge in edges:
                    logAttraction(nodes[edge.node1], nodes[edge.node2], edge.weight, coefficient)
            else:
                for edge in edges:
                    logAttraction(nodes[edge.node1], nodes[edge.node2], pow(edge.weight, edgeWeightInfluence),
                                  coefficient)
    else:
        if adjustSizes:
            if edgeWeightInfluence == 0:
                for edge in edges:
                    linAttraction_anticollision(nodes[edge.node1], nodes[edge.node2], 1, coefficient)
            elif edgeWeightInfluence == 1:
                for edge in edges:
                    linAttraction_anticollision(nodes[edge.node1], nodes[edge.node2], edge.weight, coefficient)
            else:
                for edge in edges:
                    linAttraction_anticollision(nodes[edge.node1], nodes[edge.node2],
                                                pow(edge.weight, edgeWeightInfluence), coefficient)
        else:
            if edgeWeightInfluence == 0:
                for edge in edges:
                    linAttraction(nodes[edge.node1], nodes[edge.node2], 1, coefficient)
            elif edgeWeightInfluence == 1:
                for edge in edges:
                    linAttraction(nodes[edge.node1], nodes[edge.node2], edge.weight, coefficient)
            else:
                for edge in edges:
                    linAttraction(nodes[edge.node1], nodes[edge.node2], pow(edge.weight, edgeWeightInfluence),
                                  coefficient)


# try:
#     import cython
#
#     if not cython.compiled:
#         print("Warning: uncompiled fa2util module.  Compile with cython for a 10-100x speed boost.")
# except:
#     print("No cython detected.  Install cython and compile the fa2util module for a 10-100x speed boost.")
