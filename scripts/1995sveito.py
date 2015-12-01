'''
This file is used for creating a dictionary to convert
municipalities to their modern equivelant
'''
import csv
import codecs

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

#Makes no data = 0
def fint(lis):
	for i in range(len(lis)):
		if lis[i] == '-' or lis[i] == '.': lis[i] = 0
		else: lis[i] = int(lis[i])
	return lis

def nullis(s):
	for i in s:
		if i != 0: return False
	return True

def sumlis(s, l):
	assert(len(s) == len(l))
	for i in range(len(s)):
		s[i] += l[i]
	return s

def toModern():
	modern = listSveito()
	dic = convertDict()
	moderndata = {}

	#Now you're thinking with functions
	def addline(s):
		#s[1] is always Alls
		index = s[0]
		data = fint(s[2:])
		if nullis(data): return

		#REYKJAVÍK -> REYKJAVÍKURBORG :S
		#print(modern)

		#Do actual conversion
		if index not in modern:
			try:
				index = dic[index]
			except KeyError:
				print('Something is wrong, {} is not in dic'.format(index))

		if index in moderndata:
			moderndata[index] = sumlis(moderndata[index], data)
		else: moderndata[index] = data

	#Currently the file opened is hardcoded
	with codecs.open('../data/1990-2004.csv', encoding='iso-8859-1') as f:
		reader = csv.reader(f, delimiter=';')
		for i in reader:
			if i[0] == 'Sveitarfélag' or i[0] == 'Alls': continue
			addline(i)

	return moderndata

def printdic(dic):
	#Years hardcoded!
	s = 'Sveitarfélag'
	for i in range(1990,2005):
		s += ';' + str(i)
	print(s)

	for i in dic:
		s = str(i)
		for j in dic[i]:
			s += ';' + str(j)
		print(s)


if __name__ == '__main__':
	printdic(toModern())
	#print(toModern())
