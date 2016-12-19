# -*- coding:utf-8 -*-

'k-d树'

__author__='litterzhang'

from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib.patches import Rectangle

import copy
import random
import time

class Node:
	"""Summary
	"""
	def __init__(self, v, p=None, l=None, r=None):
		"""Summary
		
		Args:
			v (TYPE): Description
			p (None, optional): Description
			l (None, optional): Description
			r (None, optional): Description
		"""
		self.p_node = p
		self.l_node = l
		self.r_node = r

		self.value = v

	def isLeaf(self):
		"""Summary
		
		Returns:
			TYPE: Description
		"""
		return (self.l_node==None and self.r_node==None)

	def isRoot(self):
		"""Summary
		
		Returns:
			TYPE: Description
		"""
		return self.p==None

	def set_lchild(p, l):
		"""Summary
		
		Args:
			p (TYPE): Description
			l (TYPE): Description
		
		Returns:
			TYPE: Description
		"""
		p.l_node = l
		l.p_node = p

	def set_rchild(p, r):
		"""Summary
		
		Args:
			p (TYPE): Description
			r (TYPE): Description
		
		Returns:
			TYPE: Description
		"""
		p.r_node = r
		r.p_node = p

	def __str__(self):
		return 'Value: %s' % self.value

class Square:
	"""Summary
	"""
	def __init__(self, p_tl, p_br):
		self.p_tl = copy.deepcopy(p_tl)
		self.p_br = copy.deepcopy(p_br)
		self.p_tr = [p_br[0], p_tl[1]]
		self.p_bl = [p_tl[0], p_br[1]]

	def __str__(self):
		return 'Top Left: %s ; Bottom Right: %s.' % (self.p_tl, self.p_br)

	@property
	def x(self):
		return self.p_br[0]-self.p_bl[0]

	@property
	def y(self):
		return self.p_tl[1]-self.p_bl[1]

def init_kd(ds, k):
	"""构造k-d树
	
	Args:
		ds (list): 数据集
		k (int): 数据的维度
	
	Returns:
		Node: 根节点
	"""

	global history

	dep = 0
	dss = [ds, ]
	nodes_l = list()

	root = None

	while len(dss):
		d = dep%k

		dssn = list()
		nodes_ln = list()

		for i in range(len(dss)):
			dsn = dss[i]

			dsn_sorted = sorted(dsn, key=lambda x:x[0][d])
			mid = (len(dsn_sorted)-1)//2+(len(dsn_sorted)-1)%2

			if len(dsn_sorted[:mid]):
				dssn.append(dsn_sorted[:mid])
			if len(dsn_sorted[mid+1:]):
				dssn.append(dsn_sorted[mid+1:])

			# 生成节点
			node_n = Node(dsn_sorted[mid])
			nodes_ln.append(node_n)

			if not root:
				root = node_n
			else:
				node_p = nodes_l[i//2]
				if i%2==0:
					Node.set_lchild(node_p, node_n)
				else:
					Node.set_rchild(node_p, node_n)
			
			# 绘制矩形
			sq_p_i = 2**dep+i-2
			sq_p = Square([0, 10], [10, 0])
			if sq_p_i>=0:
				sq_p = history[sq_p_i]

			if not d:
				history.append(Square(sq_p.p_tl, [node_n.value[0][d], sq_p.p_br[1]]))
				history.append(Square([node_n.value[0][d], sq_p.p_tl[1]], sq_p.p_br))
			else:
				history.append(Square([sq_p.p_tl[0], node_n.value[0][d]], sq_p.p_br))
				history.append(Square(sq_p.p_tl, [sq_p.p_br[0], node_n.value[0][d]]))
		dss = dssn
		nodes_l = nodes_ln
		dep += 1

	return root

def print_kd(r):
	"""打印k-d树
	
	Args:
		r (Node): 根节点
	"""
	nodes_n = [r, ]

	while len(nodes_n):
		nodes_nn = list()

		for node in nodes_n:
			if node:
				print(node.value)
				nodes_nn.append(node.l_node)
				nodes_nn.append(node.r_node)
		nodes_n = nodes_nn
		print('\n')

def calc_dis(a, b, k):
	dis = 0
	for i in range(k):
		dis += (a[i]-b[i])**2
	dis **= 0.5
	return dis

def search_kd(r, k, p):
	"""Summary
	
	Args:
		r (TYPE): Description
		k (TYPE): Description
		p (TYPE): Description
	
	Returns:
		TYPE: Description
	"""
	
	# 查找叶子节点
	dep = 0
	while r and not r.isLeaf():
		d = dep%k

		if p[d]<r.value[0][d] and r.l_node:
			r = r.l_node
		elif p[d]>=r.value[0][d] and r.r_node:
			r = r.r_node
		else:
			break

		dep += 1

	if not r:
		return None

	def update_best(n, node_min, dis_min):
		if not n: return node_min, dis_min

		dis = calc_dis(n.value[0], p, k)

		if dis<dis_min:
			dis_min = dis
			node_min = n

		return node_min, dis_min

	node_min = r
	dis_min = calc_dis(r.value[0], p, k)

	# 向上回溯
	while r.p_node:
		node_min, dis_min = update_best(r.p_node.l_node, node_min, dis_min)

		node_min, dis_min = update_best(r.p_node.r_node, node_min, dis_min)

		r = r.p_node

	return node_min, dis_min

def draw_point(ds):
	X, Y = [], []
	for p in ds:
		X.append(p[0][0])
		Y.append(p[0][1])
	plt.plot(X, Y, 'bo')
	
# initialization function: plot the background of each frame
def init():
	global ds

	plt.axis([0, 10, 0, 10])
	plt.grid(True)
	plt.xlabel('x')
	plt.ylabel('y')
	
	draw_point(ds)

def color_random():
	r = random.randint(0, 255)
	g = random.randint(0, 255)
	b = random.randint(0, 255)

	return '#%02X%02X%02X' % (r, g, b) 

# animation function.  this is called sequentially
def animate(i):
	global history, currentAxis, colors

	sq_f = history[i]
	currentAxis.add_patch(Rectangle(sq_f.p_bl, sq_f.x, sq_f.y, color=color_random()))

def draw():
	global history, currentAxis, colors

	# first set up the figure, the axis, and the plot element we want to animate
	fig = plt.figure('K-D Tree')
	ax = plt.axes(xlim=(0, 2), ylim=(-2, 2))
	line, = ax.plot([], [], 'g', lw=2)
	label = ax.text([], [], '')

	currentAxis = plt.gca()

	anim = animation.FuncAnimation(fig, animate, init_func=init, frames=len(history), interval=2, repeat=False, blit=False)
	plt.show()

	anim.save('kd_tree-build.gif', fps=2, writer='imagemagick')

if __name__=='__main__':
	global history, ds
	history = list()

	ds = list()
	for i in range(3000):
		x = round(random.random()*10, 3)
		y = round(random.random()*10, 3)
		ds.append([(x, y), ])

	r = init_kd(ds, 2)

	draw()

	# 测试搜索效率
	t_s = time.time()

	for i in range(100):
		p, p_dis = search_kd(r, 2, [4, 4])
	t_e = time.time()

	print('KD Time : %s' % (t_e-t_s))

	# 测试搜索效率
	t_s = time.time()

	for i in range(100):
		node_min = ds[0]
		dis_min = 10000.0
		for j in range(len(ds)):
			dis = calc_dis(ds[j][0], [4, 4], 2)
			if dis<dis_min:
				dis_min = dis
				node_min = ds[j]
	t_e = time.time()

	print('Time : %s' % (t_e-t_s))


