# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 16:01:24 2020

@author: User
"""

import pandas as pd
import time

def findIndex(unionList, element):
    for union in unionList:
        try:
            if element in union:
                return unionList.index(union)
        except:
            pass
    return None

def kruskal(data):
    dataList = data.values.tolist()
    edgeList = []
    
    # 上三角
    for i in range(len(dataList)):
        for j in range(i+1, len(dataList)):
            if dataList[i][j] != 0:    # 將兩點之間權重為 0 的移除
                edgeList.append([[i+1, j+1], dataList[i][j]])
    edgeList = sorted(edgeList, key=lambda x: x[1])
    
    # 下三角
    # for j in range(len(dataList)):
    #     for i in range(j+1, len(dataList)):
    #         # if dataList[i][j] != 0:    # 將兩點之間權重為 0 的移除
    #             edgeList.append([[i+1, j+1], dataList[i][j]])
    # edgeList = sorted(edgeList, key=lambda x: x[1])
    
    unionList = []
    edgeMST = []
    minCost = 0
    for edge in edgeList:
        # print('edge: ', edge, end='  ')
        firstIndex = findIndex(unionList, edge[0][0])
        secondIndex = findIndex(unionList, edge[0][1])
        if firstIndex == secondIndex == None:
            unionList.append(set(edge[0]))
        elif firstIndex == None:
            unionList[secondIndex].update(edge[0])
        elif secondIndex == None:
            unionList[firstIndex].update(edge[0])
        elif firstIndex != secondIndex:
            unionList[firstIndex] |= (unionList[secondIndex])
            unionList.remove(unionList[secondIndex])
        else: 
            # print('cycle')
            continue
        edgeMST.append(edge)
        minCost += edge[1]
        # print('unionList: ', unionList)
        if  len(edgeMST) == len(dataList)-1:
            # print('edgeMST: ', edgeMST)
            # print('final unionList: ', unionList)
            # print('minCost: ', minCost)
            return minCost


#%%

data = pd.read_excel('MST data.xlsx', header = 0, index_col = 0)

resultKruskal = []
for k in [10, 20, 30, 40, 50]:
    start = time.time()
    newData = data.iloc[:k, :k]
    minCost = kruskal(newData)
    resultKruskal.append(minCost)
    end = time.time()
    print('minCost for kruskal (k={}): '.format(k), minCost)
    print('The elapsed run time (k=' + str(k) + '): ', round(end - start, 3), 'seconds', end='\n\n')


#%%

def prim(data, startVertex):
    dataList = data.values.tolist()
    edgeList = []
    
    # 上三角
    for j in range(len(dataList)):
        for i in range(j+1, len(dataList)):
            # if dataList[i][j] != 0:    # 將兩點之間權重為 0 的移除
                edgeList.append(tuple([tuple([i+1, j+1]), dataList[i][j]]))
    
    # 下三角
    # for i in range(len(dataList)):
    #     for j in range(i+1, len(dataList)):
    #         if dataList[i][j] != 0:    # 將兩點之間權重為 0 的移除
    #             edgeList.append([[i+1, j+1], dataList[i][j]])
    # edgeList = sorted(edgeList, key=lambda x: x[1])
    
    vertexSet = set()
    unSelectSet = set([i for i in range(1, len(dataList)+1)])
    edgeMST = []
    minCost = 0
    tempSet = set()
    tempList = [edge for edge in edgeList if (startVertex in edge[0])]
    tempSet.update(tempList)
    sortList = sorted(tempSet, key=lambda x: x[1])
    vertexSet.add(startVertex)
    unSelectSet.remove(startVertex)
    
    while len(vertexSet) < len(dataList):
        edge = sortList[0]
        if ((edge[0][0] in vertexSet and edge[0][1] in unSelectSet) or 
            (edge[0][1] in vertexSet and edge[0][0] in unSelectSet)):
            # print('edge: ', edge)
            edgeMST.append(edge)
            minCost += edge[1]
            nextVertex = list(set(edge[0]).difference(vertexSet))[0]
            # print('nextVertex: ', nextVertex)
            tempList = [edge for edge in edgeList if (nextVertex in edge[0])]
            tempSet.update(tempList)
            
            vertexSet.add(nextVertex)
            unSelectSet.remove(nextVertex)
        # else: 
        #     print('cycle: ', edge)
        tempSet.remove(edge)
        sortList = sorted(tempSet, key=lambda x: x[1])
    
    # print('edgeMST: ', edgeMST)
    # print('minCost: ', minCost)
    return minCost

#%%

data = pd.read_excel('MST data.xlsx', header = 0, index_col = 0)

resultPrim = []
for k in [10, 20, 30, 40, 50]:
    start = time.time()
    newData = data.iloc[:k, :k]
    minCost = prim(newData, 2)
    resultPrim.append(minCost)
    end = time.time()
    print('minCost for prim (k={}): '.format(k), minCost)
    print('The elapsed run time (k=' + str(k) + '): ', round(end - start, 3), 'seconds', end='\n\n')


