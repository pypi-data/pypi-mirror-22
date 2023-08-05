#!/usr/bin/env python
# -*- coding:utf-8 -*-

import matplotlib
from matplotlib import pyplot as plt
import numpy as np
from numpy import linalg as LA
import cv2
import math
import os

import plotly
from plotly.graph_objs import *
from plotly.offline import download_plotlyjs, init_notebook_mode, iplot
from plotly import tools

plotly.offline.init_notebook_mode()

import time
import collections as col
from collections import OrderedDict
import ast

from ndreg import *
import ndio.remote.neurodata as neurodata
import nibabel as nib
import networkx as nx
import re
import pandas as pd

import requests
import json

import seaborn as sns

import csv, gc

from sklearn.manifold import spectral_embedding as se

import scipy.sparse as sp


def get_raw_brain(inToken, save=False, output_path=None):
    inImg = imgDownload(inToken, resolution=5)
    # Saving raw image
    if output_path == None:
        output_path = inToken + "_raw.nii"
    if save:
        imgWrite(inImg, str(output_path))

    return inImg


def get_atlas(save=False, output_path=None):
    refToken = "ara_ccf2"
    refImg = imgDownload(refToken)
    # Saving annotations
    if output_path == None:
        output_path = "ara_ccf2.nii"
    if save:
        imgWrite(refImg, str(output_path))
    return refImg


def register(token, orientation, resolution=5, raw_im=None, atlas=None):
    """
    Saves fully registered brain as token + '_regis.nii' and annotated atlas as '_anno.nii'.
    :param token: The token for the brain of interest.
    :param orientation: The orientation of the brain (e.g. LSA, RPS).
    :param resolution: Desired resolution of the image (1 - 5).
    :return:
    """
    refToken = "ara_ccf2"
    refImg = imgDownload(refToken)

    if atlas == None:
        refAnnoImg = imgDownload(refToken, channel="annotation")

    if raw_im == None:
        inImg = imgDownload(token, resolution=resolution)

    # resampling CLARITY image
    inImg = imgResample(inImg, spacing=refImg.GetSpacing())

    # reorienting CLARITY image
    inImg = imgReorient(inImg, orientation, "RSA")

    # Thresholding
    (values, bins) = np.histogram(sitk.GetArrayFromImage(inImg), bins=100, range=(0, 500))

    counts = np.bincount(values)
    maximum = np.argmax(bins)
    # print(maximum)
    # print(counts)

    lowerThreshold = maximum
    upperThreshold = sitk.GetArrayFromImage(inImg).max() + 1

    # print(lowerThreshold)
    # print(upperThreshold)

    inImg = sitk.Threshold(inImg, lowerThreshold, upperThreshold, lowerThreshold) - lowerThreshold

    # Generating CLARITY mask
    (values, bins) = np.histogram(sitk.GetArrayFromImage(inImg), bins=1000)
    cumValues = np.cumsum(values).astype(float)
    cumValues = (cumValues - cumValues.min()) / cumValues.ptp()

    maxIndex = np.argmax(cumValues > 0.95) - 1
    threshold = bins[maxIndex]

    inMask = sitk.BinaryThreshold(inImg, 0, threshold, 1, 0)

    # Affine Transformation
    spacing = [0.25, 0.25, 0.25]
    refImg_ds = imgResample(refImg, spacing=spacing)

    inImg_ds = imgResample(inImg, spacing=spacing)

    inMask_ds = imgResample(inMask, spacing=spacing, useNearest=True)

    affine = imgAffineComposite(inImg_ds, refImg_ds, inMask=inMask_ds, iterations=100, useMI=True, verbose=True)

    inImg_affine = imgApplyAffine(inImg, affine, size=refImg.GetSize())

    inMask_affine = imgApplyAffine(inMask, affine, size=refImg.GetSize(), useNearest=True)

    # LDDMM Registration
    inImg_ds = imgResample(inImg_affine, spacing=spacing)
    inMask_ds = imgResample(inMask_affine, spacing=spacing, useNearest=True)
    (field, invField) = imgMetamorphosisComposite(inImg_ds, refImg_ds, inMask=inMask_ds, alphaList=[0.05, 0.02, 0.01],
                                                  useMI=True, iterations=100, verbose=True)
    inImg_lddmm = imgApplyField(inImg_affine, field, size=refImg.GetSize())
    inMask_lddmm = imgApplyField(inMask_affine, field, size=refImg.GetSize(), useNearest=True)

    # Saving registered image
    location = "img/" + token + "_regis.nii"
    imgWrite(inImg_lddmm, str(location))

    # Saving annotations
    location = "img/" + token + "_anno.nii"
    imgWrite(refAnnoImg, str(location))

    return inImg_lddmm, refAnnoImg


def apply_clahe(input_path):
    """
    Applies clahe to the specified brain image.
    :param input_path: The path to the registered .nii file of the brain.
    :return: The clahe image array.
    """
    im = nib.load(input_path)
    im = im.get_data()

    x_value = im.shape[0]
    y_value = im.shape[1]
    z_value = im.shape[2]

    im_flat = im.reshape(-1)

    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))

    cl1 = clahe.apply(im_flat)

    im_clahe = cl1.reshape(x_value, y_value, z_value)

    return im_clahe


def downsample(im, num_points=10000, optimize=True):
    """
    Function to extract points data from a np array representing a brain (i.e. an object loaded
    from a .nii file).
    :param im: The image array.
    :param num_points: The desired number of points to be downsampled to.
    :param optimize:
    :return: The bright points in a np array.
    """
    # obtaining threshold
    percentile = 0.4
    (values, bins) = np.histogram(im, bins=1000)
    cumValues = np.cumsum(values).astype(float)
    cumValues = (cumValues - cumValues.min()) / cumValues.ptp()

    maxIndex = np.argmax(cumValues > percentile) - 1
    threshold = bins[maxIndex]
    print(threshold)

    total = im.shape[0] * im.shape[1] * im.shape[2]
    #     print("Coverting to points...\ntoken=%s\ntotal=%d\nmax=%f\nthreshold=%f\nnum_points=%d" \
    #           %(self._token,total,self._max,threshold,num_points))
    print("(This will take couple minutes)")
    # threshold
    im_max = np.max(im)
    filt = im > threshold
    # a is just a container to hold another value for ValueError: too many values to unpack
    # x, y, z, a = np.where(filt)
    t = np.where(filt)
    x = t[0]
    y = t[1]
    z = t[2]
    v = im[filt]
    #     if optimize:
    #         self.discardImg()
    #     v = np.int16(255 * (np.float32(v) / np.float32(self._max)))
    l = v.shape
    print("Above threshold=%d" % (l))
    # sample

    total_points = l[0]
    print('total points: %d' % total_points)

    if not 0 <= num_points <= total_points:
        raise ValueError("Number of points given should be at most equal to total points: %d" % total_points)
    fraction = num_points / float(total_points)

    if fraction < 1.0:
        # np.random.random returns random floats in the half-open interval [0.0, 1.0)
        filt = np.random.random(size=l) < fraction
        print('v.shape:')
        print(l)
        #         print('x.size before downsample: %d' % x.size)
        #         print('y.size before downsample: %d' % y.size)
        #         print('z.size before downsample: %d' % z.size)
        print('v.size before downsample: %d' % v.size)
        x = x[filt]
        y = y[filt]
        z = z[filt]
        v = v[filt]
        #         print('x.size after downsample: %d' % x.size)
        #         print('y.size after downsample: %d' % y.size)
        #         print('z.size after downsample: %d' % z.size)
        print('v.size after downsample: %d' % v.size)
    points = np.vstack([x, y, z, v])
    points = np.transpose(points)
    print("Output num points: %d" % (points.shape[0]))
    print("Finished")
    return points


def run_pipeline(token, orientation, resolution=5):
    register(token, orientation, resolution)
    path = "img/" + token + "_anno.nii"
    apply_clahe(path)
    downsample(im, num_points)


def save_points(points, output_path):
    """
    Saves the points to a csv file.
    :param points:
    :param output_path:
    :return:
    """
    #     pathname = 'points/Fear199.csv"
    np.savetxt(output_path, points, fmt='%d', delimiter=',')


def generate_pointcloud(points_path, output_path, resolution):
    """
    Generates the plotly scatterplot html file from the csv file."
    :param points_path:
    :param output_path:
    :param resolution:
    :return:
    """
    # Type in the path to your csv file here
    thedata = None
    thedata = np.genfromtxt(points_path,
                            delimiter=',', dtype='int', usecols=(0, 1, 2), names=['a', 'b', 'c'])

    # Set tupleResolution to resolution input parameter
    tupleResolution = resolution;

    # EG: for Aut1367, the spacing is (0.01872, 0.01872, 0.005).
    xResolution = tupleResolution[0]
    yResolution = tupleResolution[1]
    zResolution = tupleResolution[2]
    # Now, to get the mm image size, we can multiply all x, y, z
    # to get the proper mm size when plotting.

    trace1 = Scatter3d(
        x=[x * xResolution for x in thedata['a']],
        y=[x * yResolution for x in thedata['b']],
        z=[x * zResolution for x in thedata['c']],
        mode='markers',
        marker=dict(
            size=1.2,
            color='cyan',  # set color to an array/list of desired values
            colorscale='Viridis',  # choose a colorscale
            opacity=0.15
        )
    )

    data = [trace1]
    layout = Layout(
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=0
        ),
        paper_bgcolor='rgb(0,0,0)',
        plot_bgcolor='rgb(0,0,0)'
    )

    fig = Figure(data=data, layout=layout)

    plotly.offline.plot(fig, filename=output_path)


#     plotly.offline.plot(fig, filename= 'output/' + self._token + "/" + self._token + "_brain_pointcloud.html")

def get_regions(points_path, anno_path, output_path):
    """
    Function for getting the array of points with region as the fifth column.
    :param points_path:
    :param anno_path:
    :param output_path:
    :return:
    """
    atlas = nib.load(anno_path)  # <- atlas .nii image
    atlas_data = atlas.get_data()

    points = np.genfromtxt(points_path, delimiter=',')

    locations = points[:, 0:3]

    # getting the region numbers
    regions = [atlas_data[l[0], l[1], l[2]] for l in locations]

    outfile = open(output_path, 'w')
    infile = open(points_path, 'r')
    for i, line in enumerate(infile):
        line = line.strip().split(',')
        outfile.write(",".join(line) + "," + str(
            regions[i]) + "\n")  # adding a 5th column to the original csv indicating its region (integer)
    infile.close()
    outfile.close()

    print
    len(regions)
    #     print regions[0:10]
    uniq = list(set(regions))
    numRegions = len(uniq)
    print('num unique regions: %d' % len(uniq))
    print
    uniq

    p = np.genfromtxt(output_path, delimiter=',')
    return p


def create_graph(points_path, radius=20, output_filename=None):
    """
    Function for creating networkx graph object using epsilon ball to find edges.
    Saves to a .graphml if output_filename is specified.
    :param points_path:
    :param radius:
    :param output_filename:
    :return:
    """
    points = np.genfromtxt(points_path, delimiter=',', dtype='int')

    g = nx.Graph()

    for i in range(len(points)):
        #         if i % 3000 == 0:
        #             print('ahhh: %d' % i)
        coordi = points[i][0:3]
        intensityi, regioni = points[i][3:5]
        # save node name as string because when loading from .graphml file, it's hard to load tuple names
        namei = str(list(coordi))
        g.add_node(namei)
        g.node[namei]['intensity'] = int(intensityi)
        g.node[namei]['region'] = int(regioni)
        g.node[namei]['coord'] = namei

        for j in range(i + 1, len(points)):
            #             if j % 3000 == 0:
            #                 print('ahhh: %d' % j)
            coordj = points[j][0:3]
            intensityj, regionj = points[j][3:5]
            namej = str(list(coordj))

            dist = np.linalg.norm(coordi - coordj)

            # if the distance is within the radius
            if dist < radius:
                g.add_node(namej)
                g.node[namej]['intensity'] = int(intensityj)
                g.node[namej]['region'] = int(regionj)
                g.node[namej]['coord'] = namej

                g.add_edge(namei, namej, weight=float(dist))

    print('finished creating graph, now about to save to graphml.')

    if output_filename != None:
        nx.write_graphml(g, output_filename)

    return g


def plot_graphml3d(g, show=False, output_path=None):
    """
    Plotting networkx graph.  output_path should end in '.html'.
    """
    # grab the node positions from the graphML file
    V = nx.number_of_nodes(g)
    attributes = nx.get_node_attributes(g, 'coord')
    #     nodes = g.nodes()
    node_positions_3d = pd.DataFrame(columns=['x', 'y', 'z'], index=range(V))
    i = 0
    for key, val in enumerate(attributes):
        n = ast.literal_eval(val)
        node_positions_3d.loc[i] = [int(n[0]), int(n[1]), int(n[2])]
        i += 1

    # grab edge endpoints
    edge_x = []
    edge_y = []
    edge_z = []

    for e in g.edges():
        # Changing tuple to list
        source_pos = ast.literal_eval(g.node[e[0]]['coord'])
        target_pos = ast.literal_eval(g.node[e[1]]['coord'])

        edge_x += [source_pos[0], target_pos[0], None]
        edge_y += [source_pos[1], target_pos[1], None]
        edge_z += [source_pos[2], target_pos[2], None]

    # node style
    node_trace = Scatter3d(x=[x for x in node_positions_3d['x']],
                           y=[x for x in node_positions_3d['y']],
                           z=[x for x in node_positions_3d['z']],
                           mode='markers',
                           # name='regions',
                           marker=Marker(symbol='dot',
                                         size=6,
                                         opacity=0.5,
                                         color='purple'),
                           # text=[str(r) for r in range(V)],
                           # text=atlas_data['nodes'],
                           hoverinfo='text')

    # edge style
    edge_trace = Scatter3d(x=edge_x,
                           y=edge_y,
                           z=edge_z,
                           mode='lines',
                           line=Line(color='cyan', width=1),
                           hoverinfo='none')

    # axis style
    axis = dict(showbackground=False,
                showline=False,
                zeroline=False,
                showgrid=False,
                showticklabels=False)

    plot_title = 'graphml plot'
    # overall layout
    layout = Layout(title=plot_title,
                    width=800,
                    height=900,
                    showlegend=False,
                    scene=Scene(xaxis=XAxis(axis),
                                yaxis=YAxis(axis),
                                zaxis=ZAxis(axis)),
                    margin=Margin(t=50),
                    hovermode='closest',
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgb(255,255,255)')

    data = Data([node_trace, edge_trace])
    fig = Figure(data=data, layout=layout)
    if show:
        iplot(fig, validate=False)

    if output_path != None:
        plotly.offline.plot(fig, filename=output_path)


def generate_region_graph(token, points_path, output_path=None):
    """
    Creates a plotly scatterplot of the brain with traces of each region, and saves if
    output_path is specified
    :param token: The token (e.g. Aut1367)
    :param points_path: The path to the previously generated points csv with regions as the fifth column.
    :param output_path: The path to save the output plotly html file to.
    :return: The plotly figure.
    """
    font = {'weight': 'bold',
            'size': 18}

    matplotlib.rc('font', **font)

    #     points_path = 'Fear199_regions.csv'
    thedata = np.genfromtxt(points_path, dtype=int, delimiter=',')
    # deleting the brightness column
    thedata = np.delete(thedata, [3], axis=1)

    # Set tupleResolution to resolution input parameter
    #     tupleResolution = resolution;

    # EG: for Aut1367, the spacing is (0.01872, 0.01872, 0.005).
    #     xResolution = tupleResolution[0]
    #     yResolution = tupleResolution[1]
    #     zResolution = tupleResolution[2]
    # Now, to get the mm image size, we can multiply all x, y, z
    # to get the proper mm size when plotting.

    """Load the CSV of the ARA with CCF v2 (see here for docs:)"""
    ccf_txt = 'natureCCFOhedited.csv'

    ccf = {}
    with open(ccf_txt, 'rU') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            # row[0] is ccf atlas index, row[4] is string of full name
            ccf[row[0]] = row[4];
            # print row[0]
            # print row[4]
            # print ', '.join(row)

    """Save counts for each region into a separate CSV"""
    unique = [];

    for l in thedata:
        unique.append(l[3])

    uniqueNP = np.asarray(unique)
    allUnique = np.unique(uniqueNP)
    numRegionsA = len(allUnique)

    """
           First we download annotation ontology from Allen Brain Atlas API.
           It returns a JSON tree in which larger parent structures are divided into smaller children regions.
           For example the "corpus callosum" parent is has children "corpus callosum, anterior forceps", "genu of corpus callosum", "corpus callosum, body", etc
           """

    url = "http://api.brain-map.org/api/v2/structure_graph_download/1.json"
    jsonRaw = requests.get(url).content
    jsonDict = json.loads(jsonRaw)

    """
    Next we collect the names and ids of all of the regions.
    Since our json data is a tree we can walk through it in arecursive manner.
    Thus starting from the root...
    """
    root = jsonDict['msg'][0]
    """
    ...we define a recursive function ...
    """

    leafList = []

    def getChildrenNames(parent, childrenNames={}):
        if len(parent['children']) == 0:
            leafList.append(parent['id'])

        for childIndex in range(len(parent['children'])):
            child = parent['children'][childIndex]
            childrenNames[child['id']] = child['name']

            childrenNames = getChildrenNames(child, childrenNames)
        return childrenNames

    """
    ... and collect all of the region names in a dictionary with the "id" field as keys.
    """

    regionDict = getChildrenNames(root)

    ## Store most specific data
    specificRegions = [];

    for l in thedata:
        if l[3] in leafList:
            specificRegions.append(l)

    # Find all unique regions of brightest points (new)
    uniqueFromSpecific = [];

    for l in specificRegions:
        uniqueFromSpecific.append(l[3])

    uniqueSpecificNP = np.asarray(uniqueFromSpecific)
    allUniqueSpecific = np.unique(uniqueSpecificNP)
    numRegionsASpecific = len(allUniqueSpecific)

    #     print "All unique specific region ID's:"
    #     print allUniqueSpecific
    print
    "Total number of unique ID's:"
    print
    numRegionsASpecific  ## number of regions

    # Store and count the bright regions in each unique region (new)
    dictNumElementsRegionSpecific = {}
    num_points_by_region_dict = {}

    for i in range(numRegionsASpecific):
        counter = 0;
        for l in specificRegions:
            if l[3] == allUniqueSpecific[i]:
                counter = counter + 1;
                dictNumElementsRegionSpecific[ccf[str(l[3])]] = counter;
                num_points_by_region_dict[l[3]] = counter

    region_names = dictNumElementsRegionSpecific.keys()
    number_repetitions = dictNumElementsRegionSpecific.values()

    from itertools import izip

    with open(token + 'specific_counts.csv', 'wb') as write:
        writer = csv.writer(write)
        writer.writerows(izip(region_names, number_repetitions))

    specificRegionsNP = np.asarray(specificRegions)

    region_dict = OrderedDict()

    for l in specificRegionsNP:
        trace = ccf[str(l[3])]
        # trace = 'trace' + str(l[3])
        if trace not in region_dict:
            region_dict[trace] = np.array([[l[0], l[1], l[2], l[3]]])
            # print 'yay'
        else:
            tmp = np.array([[l[0], l[1], l[2], l[3]]])
            region_dict[trace] = np.concatenate((region_dict.get(trace, np.zeros((1, 4))), tmp), axis=0)
            # print 'nay'

    current_palette = sns.color_palette("husl", numRegionsA)
    # print current_palette

    data = []
    for i, key in enumerate(region_dict):
        trace = region_dict[key]
        tmp_col = current_palette[i]
        tmp_col_lit = 'rgb' + str(tmp_col)
        temp = str(np.unique(trace[:, 3])).replace("[", "")
        final = temp.replace("]", "")

        trace_scatter = Scatter3d(
            x=[x for x in trace[:, 0]],
            y=[x for x in trace[:, 1]],
            z=[x for x in trace[:, 2]],

            mode='markers',
            name=ccf[final],
            marker=dict(
                size=1.2,
                color=tmp_col_lit,  # 'purple',                # set color to an array/list of desired values
                colorscale='Viridis',  # choose a colorscale
                opacity=0.2
            )
        )

        data.append(trace_scatter)

    layout = Layout(
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=0
        ),
        paper_bgcolor='rgb(0,0,0)',
        plot_bgcolor='rgb(0,0,0)'
    )

    fig = Figure(data=data, layout=layout)

    if output_path != None:
        plotly.offline.plot(fig, filename=output_path)

    return fig, num_points_by_region_dict


def generate_density_graph(graph_path, output_path=None, plot_title=""):
    """
    Creates a plotly scatterplot of the brain with each node colored according to how many edges it has,
    and saves if output_path is specified, and saves a heatmap as well.
    :param graph_path: The path to a graphml file.
    :param output_path: The path to save the output plotly html file to.
    :param plot_title: The title of the plot.
    :return: The plotly figure and the heatmap
    """
    sortedList = None
    maxEdges = 0
    scaledEdges = 0
    heatmapbrain = None

    ## This finds the maximum number of edges and the densest node.
    G = nx.read_graphml(graph_path)

    max_edges = 0
    densestNode = ""

    for node in G.nodes():
        num_edges = len(G.edges(node))
        if (num_edges > max_edges):
            max_edges = num_edges
            densestNode = node

    x_list = []
    y_list = []
    z_list = []
    color_list = []

    for node in G.nodes():
        coord = ast.literal_eval(G.node[node]['coord'])
        x_list.append(coord[0])
        y_list.append(coord[1])
        z_list.append(coord[2])
        num_edges = len(G.edges(node))
        percentile = float(num_edges) / max_edges
        percentile = round(percentile, 1)
        color_list.append(percentile)

    ## Number of colors is maxEdges
    numColors = max_edges;

    # scaledEdges = [float(numberEdges[i])/float(upperLimit) for i in range(len(numberEdges))]
    scaledEdges = [float(numberEdges[i]) / float(max_edges) for i in range(len(numberEdges))]

    ##Tweak this to change the heat map scaling for the points.  Remove outliers.

    ##Tweak this to change the heat map scaling for the points.  Remove outliers.
    ##False coloration heatmap below.  I've commented it out in this version b/c the rainbows
    ##are difficult to interpret.  I've included a newer red version.

    # Let null values (0.0) have color rgb(0, 0, 0)
    heatMapBrain = [
        # Let null values (0.0) have color rgb(0, 0, 0)
        [0, 'rgb(0, 0, 0)'],  # black

        [0.1, '#7f0000'],
        [0.2, '#7f0000'],

        [0.2, '#b30000'],
        [0.3, '#b30000'],

        [0.3, '#d7301f'],
        [0.4, '#d7301f'],

        [0.4, '#ef6548'],
        [0.5, '#ef6548'],

        [0.5, '#fc8d59'],
        [0.6, '#fc8d59'],

        [0.6, '#fdbb84'],
        [0.7, '#fdbb84'],

        [0.7, '#fdd49e'],
        [0.8, '#fdd49e'],

        [0.8, '#fee8c8'],
        [0.9, '#fee8c8'],

        [0.9, '#fff7ec'],
        [1.0, '#fff7ec']
    ]

    g = G

    #     # grab the node positions from the graphML file
    #     V = nx.number_of_nodes(g)
    #     attributes = nx.get_node_attributes(g, 'coord')
    #     node_positions_3d = pd.DataFrame(columns=['x', 'y', 'z'], index=range(V))
    #     for n in g.nodes_iter():
    #         node_positions_3d.loc[n] = [int((re.findall('\d+', str(attributes[n])))[0]), int((re.findall('\d+', str(attributes[n])))[1]), int((re.findall('\d+', str(attributes[n])))[2])]

    # grab edge endpoints
    edge_x = []
    edge_y = []
    edge_z = []

    for e in g.edges():
        # Changing tuple to list
        source_pos = ast.literal_eval(g.node[e[0]]['coord'])
        target_pos = ast.literal_eval(g.node[e[1]]['coord'])

        edge_x += [source_pos[0], target_pos[0], None]
        edge_y += [source_pos[1], target_pos[1], None]
        edge_z += [source_pos[2], target_pos[2], None]

    # node style
    node_trace = Scatter3d(x=x_list,
                           y=y_list,
                           z=z_list,
                           mode='markers',
                           # name='regions',
                           marker=Marker(symbol='dot',
                                         size=6,
                                         opacity=0,
                                         color=color_list,
                                         colorscale=heatMapBrain),
                           # text=[str(r) for r in range(V)],
                           # text=atlas_data['nodes'],
                           hoverinfo='text')
    # edge style
    '''edge_trace = Scatter3d(x=edge_x,
                           y=edge_y,
                           z=edge_z,
                           mode='lines',
                           line=Line(color='cyan', width=1),
                           hoverinfo='none')'''

    # axis style
    axis = dict(showbackground=False,
                showline=False,
                zeroline=False,
                showgrid=False,
                showticklabels=False)

    # overall layout
    layout = Layout(title=plot_title,
                    width=800,
                    height=900,
                    showlegend=False,
                    scene=Scene(xaxis=XAxis(axis),
                                yaxis=YAxis(axis),
                                zaxis=ZAxis(axis)),
                    margin=Margin(t=50),
                    hovermode='closest',
                    paper_bgcolor='rgba(1,1,1,1)',
                    plot_bgcolor='rgb(1,1,1)')

    data = Data([node_trace])
    fig = Figure(data=data, layout=layout)

    if output_path != None:
        plotly.offline.plot(fig, filename=output_path)

    # Get list of all possible number of edges, in order
    #     setOfAllPossibleNumEdges = set(sortedList)
    #     listOfAllPossibleNumEdges = list(setOfAllPossibleNumEdges)
    #     #listOfAllScaledEdgeValues = [listOfAllPossibleNumEdges[i]/upperLimit for i in range(len(listOfAllPossibleNumEdges))]
    #     listOfAllScaledEdgeValues = [listOfAllPossibleNumEdges[i]/float(maxEdges) for i in range(len(listOfAllPossibleNumEdges))]


    # heatMapBrain

    data = Data([
        Scatter(
            y=color_list,
            marker=Marker(
                size=16,
                color=color_list,
                colorbar=ColorBar(
                    title='Colorbar'
                ),
                colorscale=heatMapBrain,
            ),
            mode='markers')
    ])

    layout = Layout(title='false coloration scheme',
                    width=800,
                    height=900,
                    showlegend=False,
                    margin=Margin(t=50),
                    hovermode='closest',
                    xaxis=dict(
                        title='Number of Unique Colors',
                        titlefont=dict(
                            family='Courier New, monospace',
                            size=18,
                            color='#000000')
                    ),
                    yaxis=dict(
                        title='Number of Edges',
                        titlefont=dict(
                            family='Courier New, monospace',
                            size=18,
                            color='#000000')
                    ),
                    paper_bgcolor='rgba(255,255,255,255)',
                    plot_bgcolor='rgb(255,255,255)')

    mapping = Figure(data=data, layout=layout)
    # iplot(mapping, validate=False)

    if output_path != None:
        plotly.offline.plot(mapping, filename=output_path.split('.')[0] + '_heatmap.html')

    # plotly.offline.plot(mapping, filename = self._token + '/' + self._token + 'heatmap' + '.html')
    return fig, mapping