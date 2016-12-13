# -*- coding:utf-8 -*-

'感知机原始模式'

__author__='litterzhang'

from matplotlib import pyplot as plt
from matplotlib import animation

# 初始化感知机参数
def init_param(n):
	w = [0 for i in range(n)]
	b = 0

	global history
	history.append((w[:], b))

	return w, b

# 计算点到超平面的距离
def calc_dis(point, n, w, b):
	dis = 0
	for i in range(n):
		dis += point[0][i]*w[i]
	dis += b
	dis *= point[1]
	return dis

# 检查是否存在误分类点
def check(training_set, n, w, b):
	flag = False

	for data in training_set:
		if calc_dis(data, n, w, b) <= 0:
			flag = True
			w, b = update(data, n, w, b)
			break
	return flag, w, b

# 更新感知机参数
def update(point, n, w, b):
	yt = 1
	for i in range(n):
		w[i] += yt*point[1]*point[0][i]
	b += yt*point[1]

	global history
	history.append((w[:], b))
	return w, b

# 感知机
def prece(training_set, n):
	w, b = init_param(n)

	while True:
		flag, w, b = check(training_set, n, w, b)
		if not flag: break
	return w, b

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

	w = history[i][0]
	b = history[i][1]

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
	
	anim.save('perceptron_origin.gif', fps=2, writer='imagemagick')


if __name__=='__main__':
	training_set = [((4, 3), 1), ((1, 1), -1), ((3, 3), 1)]
	n = 2
	
	history = list()

	prece(training_set, n)
	
	draw()


