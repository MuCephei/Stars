#tab to space

def tab_to_space(line):
	result = []
	for x in range(len(line)):
		if line[x] == "	":
			result.append("    ")
		else:
			result.append(line[x])
	result = ''.join(result)
	return result

f = open("Geometry.py","r")
f2 = open("Geometry2.py","w")
for line in f:
    f2.write(tab_to_space(line))
    print(line,end='')

f.close()

