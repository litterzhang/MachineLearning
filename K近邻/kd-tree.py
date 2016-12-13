# -*- coding:utf-8 -*-

'k-d树'

__author__='litterzhang'

import copy

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
		return (self.l==None and self.r==None)

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

if __name__=='__main__':
	global history
	history = list()

	ds = [[(2, 3), ], [(5, 4), ], [(9, 6), ], [(4, 7), ], [(8, 1), ], [(7, 2), ]]

	r = init_kd(ds, 2)

	for sq in history:
		print(sq)





