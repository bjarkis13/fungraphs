import codecs

def listSveito():
	s = []
	#Fokk encodings
	#Check if s is correct
	f = codecs.open('sveitarfelog.txt', 'r', encoding='iso-8859-15')
	for i in f:
		i = i.split()[1]
		s.append(i)

	f.close()
	return s

def convertDict():
	s = listSveito()
	dic = {}

	#Fokk encodings
	f = codecs.open('breytingar.txt', 'r', encoding='iso-8859-15')
	for i in f:
		i = i.split()
		if i[0] in dic: print '{} is already in dic!!'.format(i[0])

		dic[i[0]] = i[1]


	#Here we should do repeated applications of the script when
	#dic[i] not in s

	return dic

def printdic(dic):
	for i in dic:
		print '{}: {}'.format(i, dic[i])


if __name__ == '__main__':
	dic = convertDict()
	printdic(dic)
