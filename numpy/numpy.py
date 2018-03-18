# -*- coding: utf-8 -*-

import numpy;
import matplotlib.pyplot as plt
import pylab

print '使用列表生成一维数组'
data = [1,2,3,4,5,6]
x = numpy.array(data)
print x #打印数组
print x.dtype #打印数组元素的类型

print '使用列表生成二维数组'
data = [[1,2],[3,4],[5,6]]
x = numpy.array(data)
print x #打印数组
print x.ndim #打印数组的维度
print x.shape #打印数组各个维度的长度。shape是一个元组

print '使用zero/ones/empty创建数组:根据shape来创建'
x = numpy.zeros(6) #创建一维长度为6的，元素都是0一维数组
print x
x = numpy.zeros((2,3)) #创建一维长度为2，二维长度为3的二维0数组
print x
x = numpy.ones((2,3)) #创建一维长度为2，二维长度为3的二维1数组
print x
x = numpy.empty((3,3)) #创建一维长度为2，二维长度为3,未初始化的二维数组
print x

print '使用arrange生成连续元素'
print numpy.arange(6) # [0,1,2,3,4,5,] 开区间
print numpy.arange(0,6,2)  # [0, 2，4]

print '生成指定元素类型的数组:设置dtype属性'
x = numpy.array([1,2.6,3],dtype = numpy.int64)
print x # 元素类型为int64
print x.dtype
x = numpy.array([1,2,3],dtype = numpy.float64)
print x # 元素类型为float64
print x.dtype

print '使用astype复制数组，并转换类型'
x = numpy.array([1,2.6,3],dtype = numpy.float64)
y = x.astype(numpy.int32)
print y # [1 2 3]
print x # [ 1.   2.6  3. ]
z = y.astype(numpy.float64)
print z # [ 1.  2.  3.]

print '将字符串元素转换为数值元素'
x = numpy.array(['1','2','3'],dtype = numpy.string_)
y = x.astype(numpy.int32)
print x # ['1' '2' '3']
print y # [1 2 3] 若转换失败会抛出异常

print '使用其他数组的数据类型作为参数'
x = numpy.array([ 1., 2.6,3. ],dtype = numpy.float32);
y = numpy.arange(3,dtype=numpy.int32);
print y # [0 1 2]
print y.astype(x.dtype) # [ 0.  1.  2.]


print 'ndarray数组与标量/数组的运算'
x = numpy.array([1,2,3]) 
print x*2 # [2 4 6]
print x>2 # [False False  True]
y = numpy.array([3,4,5])
print x+y # [4 6 8]
print x>y # [False False False]

print 'ndarray的基本索引'
x = numpy.array([[1,2],[3,4],[5,6]])
print x[0] # [1,2]
print x[0][1] # 2,普通python数组的索引
print x[0,1] # 同x[0][1]，ndarray数组的索引
x = numpy.array([[[1, 2], [3,4]], [[5, 6], [7,8]]])
print x[0] # [[1 2],[3 4]]
y = x[0].copy() # 生成一个副本
z = x[0] # 未生成一个副本
print y #  [[1 2],[3 4]]
print y[0,0] # 1
y[0,0] = 0 
z[0,0] = -1
print y # [[0 2],[3 4]]
print x[0] # [[-1 2],[3 4]]
print z # [[-1 2],[3 4]]

print 'ndarray的切片'
x = numpy.array([1,2,3,4,5])
print x[1:3] # [2,3] 右边开区间
print x[:3] # [1,2,3] 左边默认为 0
print x[1:] # [2,3,4,5] 右边默认为元素个数
print x[0:4:2] # [1,3] 下标递增2
x = numpy.array([[1,2],[3,4],[5,6]])
print x[:2] # [[1 2],[3 4]]
print x[:2,:1] # [[1],[3]]
x[:2,:1] = 0 
print x # [[0,2],[0,4],[5,6]]
x[:2,:1] = [[8],[6]]
print x # [[8,2],[6,4],[5,6]]

print 'ndarray的布尔型索引'
x = numpy.array([3,2,3,1,3,0])
# 布尔型数组的长度必须跟被索引的轴长度一致
y = numpy.array([True,False,True,False,True,False]) 
print x[y] # [3,3,3] 
print x[y==False] # [2,1,0]
print x>=3 # [ True False  True False  True  False]
print x[~(x>=3)] # [2,1,0]
print (x==2)|(x==1) # [False  True False  True False False]
print x[(x==2)|(x==1)] # [2 1]
x[(x==2)|(x==1)] = 0
print x # [3 0 3 0 3 0]

print 'ndarray的花式索引:使用整型数组作为索引'
x = numpy.array([1,2,3,4,5,6])
print x[[0,1,2]] # [1 2 3]
print x[[-1,-2,-3]] # [6,5,4]
x = numpy.array([[1,2],[3,4],[5,6]])
print x[[0,1]] # [[1,2],[3,4]]
print x[[0,1],[0,1]] # [1,4] 打印x[0][0]和x[1][1]
print x[[0,1]][:,[0,1]] # 打印01行的01列 [[1,2],[3,4]]
# 使用numpy.ix_()函数增强可读性
print x[numpy.ix_([0,1],[0,1])] #同上 打印01行的01列 [[1,2],[3,4]]
x[[0,1],[0,1]] = [0,0]
print x # [[0,2],[3,0],[5,6]]

print 'ndarray数组的转置和轴对换'
k = numpy.arange(9) #[0,1,....8]
m = k.reshape((3,3)) # 改变数组的shape复制生成2维的，每个维度长度为3的数组
print k # [0 1 2 3 4 5 6 7 8]
print m # [[0 1 2] [3 4 5] [6 7 8]]
# 转置(矩阵)数组：T属性 : mT[x][y] = m[y][x]
print m.T # [[0 3 6] [1 4 7] [2 5 8]]
# 计算矩阵的内积 xTx
print numpy.dot(m,m.T) # numpy.dot点乘
# 高维数组的轴对象
k = numpy.arange(8).reshape(2,2,2)
print k # [[[0 1],[2 3]],[[4 5],[6 7]]]
print k[1][0][0]
# 轴变换 transpose 
m = k.transpose((1,0,2)) # m[y][x][z] = k[x][y][z]
print m # [[[0 1],[4 5]],[[2 3],[6 7]]]
print m[0][1][0]
# 轴交换 swapaxes (axes：轴)
m = k.swapaxes(0,1) # 将第一个轴和第二个轴交换 m[y][x][z] = k[x][y][z]
print m # [[[0 1],[4 5]],[[2 3],[6 7]]]
print m[0][1][0]
# 使用轴交换进行数组矩阵转置
m = numpy.arange(9).reshape((3,3))
print m # [[0 1 2] [3 4 5] [6 7 8]]
print m.swapaxes(1,0) # [[0 3 6] [1 4 7] [2 5 8]]

print '一元ufunc示例'
x = numpy.arange(6)
print x # [0 1 2 3 4 5]
print numpy.square(x) # [ 0  1  4  9 16 25]
x = numpy.array([1.5,1.6,1.7,1.8])
y,z = numpy.modf(x)
print y # [ 0.5  0.6  0.7  0.8]
print z # [ 1.  1.  1.  1.]

print '二元ufunc示例'
x = numpy.array([[1,4],[6,7]])
y = numpy.array([[2,3],[5,8]])
print numpy.maximum(x,y) # [[2,4],[6,8]]
print numpy.minimum(x,y) # [[1,3],[5,7]]

print 'where函数的使用'
cond = numpy.array([True,False,True,False])
x = numpy.where(cond,-2,2)
print x # [-2  2 -2  2]
cond = numpy.array([1,2,3,4])
x = numpy.where(cond>2,-2,2)
print x # [ 2  2 -2 -2]
y1 = numpy.array([-1,-2,-3,-4])
y2 = numpy.array([1,2,3,4])
x = numpy.where(cond>2,y1,y2) # 长度须匹配
print x # [1,2,-3,-4]
print 'where函数的嵌套使用'
y1 = numpy.array([-1,-2,-3,-4,-5,-6])
y2 = numpy.array([1,2,3,4,5,6])
y3 = numpy.zeros(6)
cond = numpy.array([1,2,3,4,5,6])
x = numpy.where(cond>5,y3,numpy.where(cond>2,y1,y2))
print x # [ 1.  2. -3. -4. -5.  0.]

print 'numpy的基本统计方法'
x = numpy.array([[1,2],[3,3],[1,2]]) #同一维度上的数组长度须一致
print x.mean() # 2
print x.mean(axis=1) # 对每一行的元素求平均
print x.mean(axis=0) # 对每一列的元素求平均
print x.sum() #同理 12
print x.sum(axis=1) # [3 6 3]
print x.max() # 3
print x.max(axis=1) # [2 3 2]
print x.cumsum() # [ 1  3  6  9 10 12]
print x.cumprod() # [ 1  2  6 18 18 36]
print '用于布尔数组的统计方法'
x = numpy.array([[True,False],[True,False]])
print x.sum() # 2
print x.sum(axis=1) # [1,1]
print x.any(axis=0) # [True,False]
print x.all(axis=1) # [False,False]
print '.sort的就地排序'
x = numpy.array([[1,6,2],[6,1,3],[1,5,2]])
x.sort(axis=1) 
print x # [[1 2 6] [1 3 6] [1 2 5]]
#非就地排序：numpy.sort()可产生数组的副本

print 'ndarray的唯一化和集合运算'
x = numpy.array([[1,6,2],[6,1,3],[1,5,2]])
print numpy.unique(x) # [1,2,3,5,6]
y = numpy.array([1,6,5])
print numpy.in1d(x,y) # [ True  True False  True  True False  True  True False]
print numpy.setdiff1d(x,y) # [2 3]
print numpy.intersect1d(x,y) # [1 5 6]


print 'ndarray的存取'
x = numpy.array([[1,6,2],[6,1,3],[1,5,2]])
numpy.save('file1',x) #以二进制.npy保存
numpy.savetxt('filetxt',x,delimiter=',') # 以文本保存
y = numpy.load('file1.npy')
print y #  [[1 6 2] [6 1 3] [1 5 2]]
y = numpy.loadtxt('filetxt',delimiter=',') # delimiter为分隔符
print y #  [[1 6 2] [6 1 3] [1 5 2]]
# 压缩保存
numpy.savez('filezip',a=x,b=y)
print numpy.load('filezip.npz')['a'] # 按字典索引  [[1 6 2] [6 1 3] [1 5 2]]

print '线性代数'
import numpy.linalg as nla
print '矩阵点乘'
x = numpy.array([[1,2],[3,4]])
y = numpy.array([[1,3],[2,4]])
print x.dot(y) # [[ 5 11][11 25]]
print numpy.dot(x,y) # # [[ 5 11][11 25]]
print '矩阵求逆'
x = numpy.array([[1,1],[1,2]])
y = nla.inv(x) # 矩阵求逆（若矩阵的逆存在）
print x.dot(y) # 单位矩阵 [[ 1.  0.][ 0.  1.]]
print nla.det(x) # 求行列式

print 'numpy.random随机数生成'
import numpy.random as npr

x = npr.randint(0,2,size=100000) #抛硬币
print (x>0).sum() # 正面的结果
print npr.normal(size=(2,2)) #正态分布随机数数组 shape = (2,2)


print 'ndarray数组重塑'
x = numpy.arange(0,6) #[0 1 2 3 4]
print x #[0 1 2 3 4]
print x.reshape((2,3)) # [[0 1 2][3 4 5]]
print x #[0 1 2 3 4]
print x.reshape((2,3)).reshape((3,2)) # [[0 1][2 3][4 5]]
y = numpy.array([[1,1,1],[1,1,1]])
x = x.reshape(y.shape)
print x # [[0 1 2][3 4 5]]
print x.flatten() # [0 1 2 3 4 5]
x.flatten()[0] = -1 # flatten返回的是拷贝
print x # [[0 1 2][3 4 5]]
print x.ravel() # [0 1 2 3 4 5]
x.ravel()[0] = -1 # ravel返回的是视图（引用） 
print x # [[-1 1 2][3 4 5]]
print "维度大小自动推导"
arr = numpy.arange(15)
print arr.reshape((5, -1)) # 15 / 5 = 3

print '数组的合并与拆分'
x = numpy.array([[1, 2, 3], [4, 5, 6]])
y = numpy.array([[7, 8, 9], [10, 11, 12]])
print numpy.concatenate([x, y], axis = 0)  # 竖直组合 [[ 1  2  3][ 4  5  6][ 7  8  9][10 11 12]]
print numpy.concatenate([x, y], axis = 1)  # 水平组合 [[ 1  2  3  7  8  9][ 4  5  6 10 11 12]]
print '垂直stack与水平stack'
print numpy.vstack((x, y)) # 垂直堆叠:相对于垂直组合
print numpy.hstack((x, y)) # 水平堆叠：相对于水平组合
# dstack：按深度堆叠
print numpy.split(x,2,axis=0) # 按行分割 [array([[1, 2, 3]]), array([[4, 5, 6]])]
print numpy.split(x,3,axis=1) # 按列分割 [array([[1],[4]]), array([[2],[5]]), array([[3],[6]])]

print '数组的元素重复操作'
x = numpy.array([[1,2],[3,4]])
print x.repeat(2) # 按元素重复 [1 1 2 2 3 3 4 4]
print x.repeat(2,axis=0) # 按行重复 [[1 2][1 2][3 4][3 4]]
print x.repeat(2,axis=1) # 按列重复 [[1 1 2 2][3 3 4 4]]
x = numpy.array([1,2])
print numpy.tile(x,2)
print numpy.tile(x, (2, 2))  # 指定从低位到高位依次复制的次数。 