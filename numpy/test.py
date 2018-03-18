#encoding=utf-8

import numpy as np

def main():
    lst = [[1,2,3],[4,5,6]]
    print(type(lst)) #列表数据类型
    np_lst = np.array(lst)
    print(np_lst) #打印数组
    print(type(np_lst)) #经过numpy处理后的数组类型(矩阵)
    print(np_lst.shape) #打印数组各个维度的长度
    print(np_lst.ndim) #打印数组的维度
    print(np_lst.dtype) #打印数组元素的类型
    print(np_lst.itemsize) #打印每个字节长度
    print(np_lst.size) #打印数组长度
    print(np.array(lst, dtype=complex))

if __name__ == "__main__":
    main()