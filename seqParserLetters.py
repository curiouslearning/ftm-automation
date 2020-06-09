#!/usr/bin/python
import os
import codecs
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
import random
from sys import argv
import csv


def removeSpaces (lst):
	lst = [x.lstrip()for x in lst if x != ' ']
	lst = [x.strip() for x in lst if x != ' ']
	lst = [x.lower() for x in lst if x != ' ']
	return lst

def isGameplayText (string):
	if(string != 'BonusLetter'
	and string != 'FireWrongLetter'
	and string != 'MagnetLetter'
	and string != 'Shield'):
		return False
	else:
		return True



def chooseTarget(letters):
	target = ''
	parsedList = [x for x in letters if x not in usedLetters]
	if (not parsedList):
		target = letters[random.randrange(len(letters))]
		return target
	else:
		target = parsedList[random.randrange(len(parsedList))]
		usedLetters.append(target)
		return target


def letterFill (group, root):
	segments = root[0]
	count = 0
	for subTree in segments:
		count = count +1
		#print "puzzle: " + str(segments.getchildren().index(subTree)) #DEBUG
		#print "group: " + str(group) #DEBUG
		print group
		letters = groups[group-1]
	#	print letters
		target = chooseTarget(letters)
		target = target.lower()
		replaceStones(subTree, target, letters)



def replaceStones(troot, targetLet, foils):

	# fix the required letter
	req = "MonsterRequiredLetters"
	reqLets = troot.find(req)
	reqLet = reqLets.find('string')
	oldTarget = reqLet.text
	reqLet.text = targetLet

	#go thru draggable stones
	dragStones = troot.find("Stones")
	for child in dragStones.findall('string'):
		spawnList = [];
		if(not isGameplayText(child.text)):
			if(child.text == oldTarget):
				child.text = targetLet
			else:
				child.text = foils[random.randrange(len(foils))]







########### MAIN ######
groups =[]
usedLetters = []
numFoils = 0
with open('/mnt/o/FTM/MARATHI/nlg.csv', 'rb') as csvfile:
	masterCSV = csv.reader(csvfile)
	next(masterCSV)
	for row in masterCSV:
		group = row[0]
		#print "group: " + str(group)
		messyLetters = row[1].split(',')
		letters = [x.decode('utf8') for x in messyLetters if x !=' ']
		letters = removeSpaces(letters)
		groups.append(letters)
csvfile.close()


indir = '/mnt/o/FTM/buildengine/input_all_letters/'
outdir = '/mnt/o/FTM/MARATHI/levels/'
oldg = -1
for root, dirs, filenames in os.walk (indir):
	for f in filenames:
		print '\n' + f #DEBUG
		tree = ET.parse (os.path.join(root,f))
		treeRoot = tree.getroot()
		group = int(treeRoot.get('LettersGroup'))

		if (group > oldg):
			oldg = group
			usedLetters = []

		letterFill(group, treeRoot)

		tree = ET.ElementTree(treeRoot)
		filename = outdir + f
		#rough_string = ET.tostring(treeRoot, 'utf-8')
		#reparsed = minidom.parseString(rough_string)
		#tree = reparsed.toprettyxml(indent="\t")
		tree.write(open(filename, 'wb'), encoding = 'utf-8')
		#file = open(filename, 'w')
		#file.write(tree)
		#file.close()
		tree = ""
