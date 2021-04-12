# -*- coding: utf-8 -*-
"""
Created on Sat Jan  9 23:15:29 2021

@author: User
"""

import math
import pandas as pd
import time
import copy

# min heap
class MinHeap:
    def __init__(self):
        self.heap = []
        self.size = 0
        self.time = 0
        
    def parent(self, i):
        return (i-1) // 2
    def leftChild(self, i):
        return 2 * i + 1
    def rightChild(self, i):
        return 2 * i + 2
    def isLeaf(self, i):
        if i >= self.size // 2 and i <= self.size:
            return True
        return False
    def swap(self, first, second):
        self.heap[first], self.heap[second] = self.heap[second], self.heap[first]
    
    def insert(self, process):
        self.size += 1
        self.heap.append(process)
        self.heapifyUp(self.size)
    
    def heapifyUp(self, n):
        current = n - 1
        while current > 0 and self.heap[current][1] < self.heap[self.parent(current)][1]:
            self.swap(current, self.parent(current))
            current = self.parent(current)
    
    def deleteSRPT(self):
        job = self.heap[0][0]
        complete = self.time
        self.swap(0, self.size-1)
        del self.heap[self.size-1]
        self.size -= 1
        self.heapifyDown(0)
        return [job, complete]
    
    def deleteFS(self):
        job = self.heap[0][0]
        complete = self.heap[0][1]
        try:
            result = [job, complete, self.heap[0][2], self.heap[0][3]]    # time, value
        except:
            pass
        self.swap(0, self.size-1)
        del self.heap[self.size-1]
        self.size -= 1
        self.heapifyDown(0)
        try:
            return result
        except:
            return [job, complete]
    
    def heapifyDown(self, i):
        # 若不為 leaf 則繼續向下調整
        if not self.isLeaf(i):
            # 若右子樹為空 (只有左子樹)
            if self.rightChild(i) > self.size-1:
                if (self.heap[i][1] > self.heap[self.leftChild(i)][1]):
                    self.swap(i, self.leftChild(i))
            # 若有左右子樹
            else:
                if (self.heap[i][1] > self.heap[self.leftChild(i)][1] or self.heap[i][1] > self.heap[self.rightChild(i)][1]):
                    if self.heap[self.leftChild(i)][1] < self.heap[self.rightChild(i)][1]: 
                        self.swap(i, self.leftChild(i))
                        self.heapifyDown(self.leftChild(i))
                    else:
                        self.swap(i, self.rightChild(i))
                        self.heapifyDown(self.rightChild(i))


#%%

def SRPT(jobsList, time, value):
    jobs = copy.deepcopy(jobsList)
    minHeap = MinHeap()
    minHeap.time = time
    
    completeList = []
    
    # 若還有 process 未完成或時間未到達，則重複執行迴圈
    while (len(jobs) != 0) or minHeap.size != 0:
        # 若有到達的 process，將到達的 process insert 到 heap 中
        while len(jobs) != 0 and jobs[0][1] <= minHeap.time:
            minHeap.insert([jobs[0][0], jobs[0][2]])
            jobs.remove(jobs[0])
        
        # 當還有 process 未到達但 heap 已空的情形發生
        if len(jobs) != 0 and minHeap.size == 0:
            minHeap.time += 1
            continue
        # heap 不為空 (最短 process 執行)
        else:
            minHeap.heap[0][1] -= 1
            minHeap.time += 1
            # 當 process 做完，則將其從 heap 中 delete 掉 (記錄到 completeList)
            if minHeap.heap[0][1] == 0:
                completeList.append(minHeap.deleteSRPT())
    
    for j in range(len(completeList)):
        value += completeList[j][1]
    # print('completeList: ', completeList)
    # print('total units: ', completeList[-1][1])
    # print('the objective value: ', value)
    return completeList, value



#%% 
# def SJF(jobs):
#     value = 0
#     time = 0
#     # if len(jobs) >= 1:
#     for i in range(len(jobs)):
#         # 計算 time, objective value
#         if jobs[i][1] > time:
#             time = jobs[i][1] + jobs[i][2]
#         else:
#             time = time + jobs[i][2]
#         value += time
#     return [time, value]

#%%

def DFSValue(jobsPermu, jobs, time, value):
    global minValue_global
    global valueList
    global minSolution_global
    global solutionList
    global countLB
    global updateUB
    global roundList
    
    # print('jobsPermu: ', jobsPermu)
    if len(jobs) <= 1:
        if jobs[0][1] > time:
            timeNext = jobs[0][1] + jobs[0][2]
        else:
            timeNext = time + jobs[0][2]
        valueNext = value + timeNext
        valueList.append(valueNext)
        jobsPermu.append(jobs[0])
        # print('solution: ', valueNext)
        solutionList.append(jobsPermu)
        
        # 記錄最小 objective value
        if valueNext < minValue_global:
            minValue_global = valueNext
            minSolution_global = [jobsPermu]
            # print('minValue: ', valueNext, 'minSolution: ', jobsPermu)
            updateUB += 1
        elif valueNext == minValue_global:
            minSolution_global.append(jobsPermu)
            # print('minValueAppend: ', valueNext, 'minSolution: ', jobsPermu)
            updateUB += 1
        return
    
    jobsHeap = MinHeap()
    
    # 計算每個 job 為首的 LB
    for i in range(len(jobs)):
        jobsTemp = jobsPermu + [jobs[i]]
        # print('jobsTemp: ', jobsTemp)
        jobsNext = jobs[:i] + jobs[i+1:]
        if jobs[i][1] > time:
            timeTemp = jobs[i][1] + jobs[i][2]
        else:
            timeTemp = time + jobs[i][2]
        valueTemp = value + timeTemp
        # print('jobsNext: ', jobsNext)
        LB = SRPT(jobsNext, timeTemp, valueTemp)[1]
        countLB += 1
        if LB > minValue_global:
            # print('cut')
            continue
        jobsHeap.insert([jobsTemp, LB])
        # print('insert: ', [jobsTemp, LB])
    
    # 以最小者往下發展，直到 heap 為空
    while (jobsHeap.size != 0):
        roundBest = jobsHeap.deleteFS()
        # print('roundBest: ', roundBest)
        
        # 下一遞迴更新
        jobsNew = roundBest[0]
        # print('jobsNew: ', jobsNew)
        jobsNext = list(filter(lambda x: x not in jobsNew, jobs))
        # print('jobsNext: ', jobsNext)
        if jobsNew[-1][1] > time:
            timeNext = jobsNew[-1][1] + jobsNew[-1][2]
        else:
            timeNext = time + jobsNew[-1][2]
        valueNext = value + timeNext
        
        DFSValue(jobsNew, jobsNext, timeNext, valueNext)
    return

#%%

def BFSValue(jobs):
    minValue = math.inf    # 最小 objective value
    valueList = []    # 每個 permutation 的 objective value
    minSolution = []
    solutionList = []
    countLB = 0
    jobsHeap = MinHeap()    # 每層間的 LB 相互比較，取最小值
    time = 0
    value = 0
    updateUB = 0
    
    # 計算每個 job 為首的 LB
    for i in range(len(jobs)):
        jobsTemp = jobs[:i] + jobs[i+1:]
        if jobs[i][1] > time:
            timeTemp = jobs[i][1] + jobs[i][2]
        else:
            timeTemp = time + jobs[i][2]
        valueTemp = value + timeTemp
        LB = SRPT(jobsTemp, timeTemp, valueTemp)[1]
        jobsHeap.insert([[jobs[i]], LB, timeTemp, valueTemp])
        # print('insert: ', [[jobs[i]], LB, timeTemp, valueTemp])
    
    # 以 LB 最小者往下發展，直到 heap 為空
    while (jobsHeap.size != 0) and (jobsHeap.heap[0][1] <= minValue):
        roundBest = jobsHeap.deleteFS()
        # print('roundBest: ', roundBest)
        
        # 下一計算最小 LB
        time = roundBest[2]
        value = roundBest[3]
        jobsNew = roundBest[0]
        # print('jobsNew: ', jobsNew)
        jobsNext = list(filter(lambda x: x not in jobsNew, jobs))
        # print('jobsNext: ', jobsNext)
        
        if len(jobsNext) <= 1:
            jobsNew.append(jobsNext[0])
            if jobsNext[0][1] > time:
                timeNext = jobsNext[0][1] + jobsNext[0][2]
            else:
                timeNext = time + jobsNext[0][2]
            valueNext = value + timeNext
            
            valueList.append(valueNext)
            # print('solution: ', value)
            solutionList.append(jobsNew)
            
            # 記錄最小 objective value
            if valueNext < minValue:
                minValue = valueNext
                minSolution = [jobsNew]
                # print('minValue: ', valueNext, 'minSolution: ', jobsNew)
                updateUB += 1
            elif valueNext == minValue:
                minSolution.append(jobsNew)
                # print('minValueAppend: ', valueNext, 'minSolution: ', jobsNew)
                updateUB += 1
            
        else:
            # 計算加入各個 job 的 LB
            for i in range(len(jobsNext)):
                jobsPermu = jobsNew + [jobsNext[i]]
                # print('jobsPermu: ', jobsPermu)
                jobsTemp = jobsNext[:i] + jobsNext[i+1:]
                # print('jobsTemp: ', jobsTemp)
                if jobsNext[i][1] > time:
                    timeNext = jobsNext[i][1] + jobsNext[i][2]
                else:
                    timeNext = time + jobsNext[i][2]
                valueNext = value + timeNext
                LB = SRPT(jobsTemp, timeNext, valueNext)[1]
                countLB += 1
                # bounding
                if LB > minValue:
                    # print('cut  ')
                    # print('not insert: ', [jobsPermu, LB])
                    continue
                jobsHeap.insert([jobsPermu, LB, timeNext, valueNext])
                # print('LB: ', LB, 'minValue: ', minValue)
                # print('insert: ', [jobsPermu, LB, timeNext, valueNext])
    
    return minValue, minSolution, countLB, updateUB

#%%   test_instance

test_instance = pd.read_excel('test instance.xlsx', header = None, index_col = 0)
test_instance = test_instance.T
test_instance['job'] = test_instance.index
test_instance = test_instance[['job', 'r_j', 'p_j']]
testList = test_instance.values.tolist()

#%%   DFS, test_instance

k = 50
newList = copy.deepcopy(testList)[:k]

# global value 
minValue_global = math.inf    # 最小 objective value
valueList = []    # 每個 permutation 的 objective value
minSolution_global = []
solutionList = []
jobsPermu = []
countLB = 0
updateUB = 0

start = time.time()
DFSValue(jobsPermu, newList, 0, 0)

print('DFSValue: ')
print('Mininal objective value: ', minValue_global)
print('Optimal permutation(DFS): ' + '\n', minSolution_global)
print('countLB: ', countLB)
print('updateUB: ', updateUB)
print('numOfSolution: ', len(minSolution_global))

end = time.time()
print('The elapsed run time (k=' + str(k) + '): ', round(end - start, 3), 'seconds', end='\n\n')

#%%

print('DFSValue: ')

for k in [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 35, 40, 45, 50]:#range(8, 50):
    newList = copy.deepcopy(testList)[:k]
    
    # global value 
    minValue_global = math.inf    # 最小 objective value
    valueList = []    # 每個 permutation 的 objective value
    minSolution_global = []
    solutionList = []
    jobsPermu = []
    countLB = 0
    updateUB = 0
    
    start = time.time()
    DFSValue(jobsPermu, newList, 0, 0)
    
    print('Mininal objective value: ', minValue_global)
    print('Optimal permutation(DFS): ' + '\n', minSolution_global)
    print('countLB: ', countLB)
    print('updateUB: ', updateUB)
    print('numOfSolution: ', len(minSolution_global))
    end = time.time()
    print('The elapsed run time (k=' + str(k) + '): ', round(end - start, 3), 'seconds', end='\n\n')


#%%   BFS, test_instance

k = 50
newList = copy.deepcopy(testList)[:k]

start = time.time()
minValue, minSolution, countLB, updateUB = BFSValue(newList)

print('BFSValue: ')
print('Mininal objective value: ', minValue)
print('Optimal permutation(BFS): ' + '\n', minSolution)
print('countLB: ', countLB)
print('updateUB: ', updateUB)
print('numOfSolution: ', len(minSolution))
end = time.time()
print('The elapsed run time (k=' + str(k) + '): ', round(end - start, 3), 'seconds', end='\n\n')

#%%

print('BFSValue: ')

for k in [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 35, 40, 45, 50]:#range(8, 50):
    newList = copy.deepcopy(testList)[:k]
    
    start = time.time()
    minValue, minSolution, countLB, updateUB = BFSValue(newList)
    
    print('Mininal objective value: ', minValue)
    print('Optimal permutation(BFS): ' + '\n', minSolution)
    print('countLB: ', countLB)
    print('updateUB: ', updateUB)
    print('numOfSolution: ', len(minSolution))
    end = time.time()
    print('The elapsed run time (k=' + str(k) + '): ', round(end - start, 3), 'seconds', end='\n\n')



#%%   DFS, test_instance

# jobsList = [[1, 0, 6], 
#             [2, 2, 2], 
#             [3, 2, 3], 
#             [4, 6, 2], 
#             [5, 7, 5], 
#             [6, 9, 2]]#,
#             # [7, 9, 3], 
#             # [8, 10, 4], 
#             # [9, 11, 2], 
#             # [10, 14, 5], 
#             # [11, 15, 3], 
#             # [12, 16, 4]]


# # global value 
# minValue_global = math.inf    # 最小 objective value
# valueList = []    # 每個 permutation 的 objective value
# minSolution_global = []
# solutionList = []
# countLB = 0
# updateUB = 0

# jobsPermu = []
# start = time.time()
# DFSValue(jobsPermu, jobsList, 0, 0)

# print('DFSValue: ')
# print('Mininal objective value: ', minValue_global)
# print('Optimal permutation(DFS): ' + '\n', minSolution_global)
# print('countLB: ', countLB)
# print('updateUB: ', updateUB)
# print('numOfSolution: ', len(minSolution_global))
# end = time.time()
# print('The elapsed run time : ', round(end - start, 3), 'seconds', end='\n\n')

#%%

# jobsList = [[1, 0, 6], 
#             [2, 2, 2], 
#             [3, 2, 3], 
#             [4, 6, 2], 
#             [5, 7, 5], 
#             [6, 9, 2]]#,
#             # [7, 9, 3], 

#             # [8, 10, 4], 
#             # [9, 11, 2], 
#             # [10, 14, 5], 
#             # [11, 15, 3], 
#             # [12, 16, 4]]

# start = time.time()

# minValue, minSolution, countLB, updateUB = BFSValue(jobsList)

# print('BFSValue: ')
# print('Mininal objective value: ', minValue)
# print('Optimal permutation(BFS): ' + '\n', minSolution)
# print('countLB: ', countLB)
# print('updateUB: ', updateUB)
# print('numOfSolution: ', len(minSolution))
# end = time.time()
# print('The elapsed run time : ', round(end - start, 3), 'seconds', end='\n\n')

