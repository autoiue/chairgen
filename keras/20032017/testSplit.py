import math

def getsplit(number, ratio):

	test = math.floor(number*ratio)
	train = math.ceil(number*(1-ratio))-number%test

	return train, test

for x in range(0, 67, 3):
	print(split(100+x, 0.1))