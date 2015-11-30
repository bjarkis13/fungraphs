import csv
import modernsveito as ms

#Makes no data = 0
def fint(lis):
	for i in range(len(lis)):
		if lis[i] == '-': lis[i] = 0
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
	modern = ms.listSveito()
	dic = ms.convertDict()
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
	with open('../data/2004-2014.csv') as f:
		reader = csv.reader(f, delimiter=';')
		for i in reader:
			if i[0] == 'Sveitarfélag' or i[0] == 'Alls': continue
			addline(i)

	return moderndata


if __name__ == '__main__':
	print(toModern())
