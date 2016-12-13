# -*- coding:utf-8 -*-

'感知机对偶模式'

__author__='litterzhang'

from matplotlib import pyplot as plt
from matplotlib import animation

# 计算w
def calc_w(training_set, n, alpha):
	m = len(training_set)

	w = [0 for i in range(n)]

	for i in range(n):
		for j in range(m):
			w[i] += training_set[j][1]*alpha[j]*training_set[j][0][i]
	return w[:]

# 初始化感知机参数
def init_param(training_set, n):
	m = len(training_set)

	alpha = [0 for i in range(m)]
	b = 0

	gram = [[0 for j in range(m)] for i in range(m)]

	for i in range(m):
		for j in range(m):
			res = 0
			for k in range(n):
				res += training_set[i][0][k]*training_set[j][0][k]
			gram[i][j] = res 

	global history
	w = calc_w(training_set, n, alpha)
	history.append((alpha[:], w, b))

	return alpha, b, gram

# 计算点到超平面的距离
def calc_dis(training_set, i, gram, alpha, b):
	m = len(training_set)

	dis = 0
	for j in range(m):
		dis += gram[i][j]*alpha[j]*training_set[j][1]
	dis += b
	dis *= training_set[i][1]
	return dis

# 检查是否存在误分类点
def check(training_set, n, gram, alpha, b):
	flag = False

	m = len(training_set)

	for i in range(m):
		if calc_dis(training_set, i, gram, alpha, b) <= 0:
			flag = True
			w, b = update(training_set, n, i, alpha, b)
			break
	return flag, alpha, b

# 更新感知机参数
def update(training_set, n, i, alpha, b):
	yt = 1

	alpha[i] += yt
	b += yt*training_set[i][1]

	global history
	w = calc_w(training_set, n, alpha)
	history.append((alpha[:], w, b))

	return alpha, b

# 感知机
def prece(training_set, n):
	alpha, b, gram = init_param(training_set, n)

	while True:
		flag, alpha, b = check(training_set, n, gram, alpha, b)
		if not flag: break

# initialization function: plot the background of each frame
def init():
	line.set_data([], [])
	x, y, x_, y_ = [], [], [], []
	for p in training_set:
		if p[1] > 0:
			x.append(p[0][0])
			y.append(p[0][1])
		else:
			x_.append(p[0][0])
			y_.append(p[0][1])

	plt.plot(x, y, 'bo', x_, y_, 'rx')
	plt.axis([-6, 6, -6, 6])
	plt.grid(True)
	plt.xlabel('x')
	plt.ylabel('y')
	plt.title('Perceptron Algorithm')
	return line, label

# animation function.  this is called sequentially
def animate(i):
	global history, ax, line, label

	w = history[i][1]
	b = history[i][2]

	if w[0] == 0 and w[1] == 0:
		return line, label
	if w[1] == 0:
		x = -b / w[0]
		y1 = 7
		y2 = -7
		line.set_data([x, x], [y1, y2])
		y1 = 0
		label.set_text(history[i])
		label.set_position([x, y1])
	else:
		x1 = -7
		y1 = -(b + w[0] * x1) / w[1]
		x2 = 7
		y2 = -(b + w[0] * x2) / w[1]
		line.set_data([x1, x2], [y1, y2])
		x1 = 0
		y1 = -(b + w[0] * x1) / w[1]
		label.set_text(history[i])
		label.set_position([x1, y1])
	return line, label

def draw():
	global history, ax, line, label

	# first set up the figure, the axis, and the plot element we want to animate
	fig = plt.figure('Perceptron')
	ax = plt.axes(xlim=(0, 2), ylim=(-2, 2))
	line, = ax.plot([], [], 'g', lw=2)
	label = ax.text([], [], '')
 
	# call the animator.  blit=true means only re-draw the parts that have changed.
	anim = animation.FuncAnimation(fig, animate, init_func=init, frames=len(history), interval=1000, repeat=True, blit=True)
	plt.show()
	
	anim.save('perceptron_pair.gif', fps=2, writer='imagemagick')

if __name__=='__main__':
	training_set = [((3, 3), 1), ((4, 3), 1), ((1, 1), -1)]
	n = 2
	
	history = list()

	prece(training_set, n)

	draw()
