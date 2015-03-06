

#createSccFileCmd = 'idcombb -dfn MCRNC=T -dfn ASN=F -dfn BCN=T -dfn ADA=F -dfn CRNC=F -all_open -inlist .\src\obh_qxqx.in1 .\src\obh_qxqx.in2 .\src\obh_qxqx.in3 -out .\src\obh_qxqx.scc'

copySccCmd = 'cp ./*.scc ../src/ && cp ./include/*.* ../src/'

tncheckCmd = 'tncheckc ...'

ERROR_KEY = '(E)'

SHOW_LINE_NUMBER = 2

import subprocess
import sys
import ntpath


def executCmd(cmdText):
	p = subprocess.Popen(cmdText, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

	info = p.stdout.readlines()
	#printLines(info)
	retval = p.wait()
	return info

def usefulInfo(keyword, text):
	index = text.find(keyword)
	if index >= 0:
		return text[index:]

def isErrorInfo(text):
	index = text.find(ERROR_KEY)
	return index >= 0

def minErrorList(keyword, lines):
	totErrorCount = 0
	outLines = []
	for line in lines:
		if not isErrorInfo(line):
			continue
		totErrorCount += 1
		info = usefulInfo(keyword, line)
		if info:
			outLines.append(info)
	return totErrorCount, outLines

def printLines(lines, count=None):
	text = ''
	for i, line in enumerate(lines):
		text += line
		if count and ( count <= (i+1) ):
			break
	print text

def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail

def main():
	executCmd(copySccCmd)
	warnings = executCmd(tncheckCmd)
	if len(sys.argv) < 2:
		printLines(warnings)
		return
	keyword = path_leaf(sys.argv[1])
	totalErrorCount, usefulWarnings = minErrorList(keyword, warnings)
	printLines(usefulWarnings, SHOW_LINE_NUMBER)
	if totalErrorCount > 0:
		print( str(totalErrorCount) + ' error totally')


if __name__ == '__main__':
	main()
