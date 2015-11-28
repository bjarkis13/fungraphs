def listSveito():
	s = []

	#Hopefully this file is correct
	with open('../data/sveitarfelog.txt', 'r') as f:
		for i in f:
			i = i.split(',')[1].strip()
			s.append(i)

	return s

def convertDict(end=True):
	s = listSveito()
	dic = {}

	with open('../data/breytingar.txt', 'r') as f:
		for i in f:
			i = i.split(',')
			if i[0] == 'Fyrir': continue
			if i[0] in dic: print('{} is already in dic!!'.format(i[0]))
			dic[i[0]] = i[1]


	#Continuously apply changes until we are at modern times
	if end:
		for i in dic:
			depth = 0
			while dic[i] not in s:
				for j in dic:
					if dic[i] == j: dic[i] = dic[j]
				depth += 1
				if depth > 10:
					print('Something is afoot, we stop at {}: {}'.format(i, dic[i]))
					break

	return dic

def printdic(dic):
	for i in dic:
		print('{}: {}'.format(i, dic[i]))


if __name__ == '__main__':
	dic = convertDict()
	#printdic(dic)
