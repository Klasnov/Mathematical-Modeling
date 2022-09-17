"""
使用层次分析法解决决策问题的程序
作者：邵彦铭
时间：2022年9月13日
编译器：Python 3.9
"""

import numpy as np


# 构造成对比较矩阵
def CompMatrix(n: int) -> np.ndarray:
    A = np.eye(n)
    for i in range(n):
        for j in range(i + 1, n):
            temp = input('请输入第%d个对象相对于第%d个对象的影响：' % (i + 1, j + 1))
            temp = eval(temp)
            A[i, j] = temp
            A[j, i] = 1 / temp
    return A

# 层次单排序一致性检验
def SingleSort(A: np.ndarray, n: int, isSingle: bool) -> list:
    # 随机一致性指标
    RI = np.array([0, 0, 0.52, 0.89, 1.12, 1.26, 1.36, 1.41, 1.46, 1.49, 1.52, 1.54, 1.56, 1.58, 1.59])
    # 相对权重向量
    w = np.ones(n)
    for i in range(n):
        s1 = 0
        for j in range(n):
            s2 = np.sum(A[:, j])
            s1 = s1 + A[i, j] / s2
        w[i] = s1 / n
    print("\n权向量w = ", w, '')
    # 最大特征根计算
    s1 = 0
    for i in range(n):
        s2 = 0
        for j in range(n):
            s2 = s2 + A[i, j] * w[j]
        s1 = s1 + s2 / w[i]
    lamda = s1 / n
    # 一致性检验
    CI = (lamda - n) / (n - 1)
    print("一致性指标CI = %.3f" % CI)
    CR = CI / RI[n - 1]
    print("一致性比率CR = %.3f" % CR)
    if isSingle:
        if CR > 0.1:
            print("!!! 未通过一致性检验，请重置成对比较矩阵 !!!\n")
            return [False, w, CI]
        else:
            return [True, w, CI]
    else:
        return [True, w, CI]


# 层次总排序一致性检验
def TotalSort(acsN: int, targN: int, wTol: np.ndarray) -> np.ndarray:
    # 随机一致性指标与数据结构
    RI = np.array([0, 0, 0.52, 0.89, 1.12, 1.26, 1.36, 1.41, 1.46, 1.49, 1.52, 1.54, 1.56, 1.58, 1.59])
    # 层次总排序一致性检验
    wEach = np.zeros([acsN, targN])
    CIs = np.zeros([acsN])
    isPassed = False
    while not isPassed:
        for i in range(acsN):
            print("\n# 构建第%d个总排序成对比较矩阵 #" % (i + 1))
            tempM = CompMatrix(targN)
            tempFlag, wEach[i], CIs[i] = SingleSort(tempM, targN, False)
        s1 = 0
        s2 = 0
        for i in range(acsN):
            s1 = s1 + wTol[i] * CIs[i]
            s2 = s2 + wTol[i] * RI[targN - 1]
        CR = s1 / s2
        if CR < 0.1:
            isPassed = True
        else:
            print("!!! 未通过一致性检验，请重置成对比较矩阵 !!!\n")
    return wEach

# 选择最优方案
def BestChoice(acsN: int, targN: int, wTol: np.ndarray, wEach: np.ndarray) -> list:
    score = np.zeros([targN])
    index = list()
    for i in range(targN):
        for j in range(acsN):
            score[i] = score[i] + wTol[j] * wEach[j][i]
    maxScore = np.max(score)
    for i in range(targN):
        if score[i] == maxScore:
            index.append(i + 1)
    return index


print("********** 数据初始化 **********")
acsNum = eval(input("请输入衡量指标的个数："))
targNum = eval(input("请输入备选方案的个数："))
print("\n********** 层次单排序一致性检验 **********")
print("# 构建单排序成对比较矩阵 #")
a = CompMatrix(acsNum)
print("# 输出层次单排序一致性检验结果 #")
flag, wtsTol = SingleSort(a, acsNum, True)
if flag:
    print("\n********** 层次总排序一致性检验 **********")
    wtsEach = TotalSort(acsNum, targNum, wtsTol)
    print("\n********** 最终方案决策 **********")
    choices = BestChoice(acsNum, targNum, wtsTol, wtsEach)
    print("应选择方案:", choices)
