#!/usr/bin/python
import os
import xmltodict
import json
import sys
from sys import argv

startlook = '/mnt/o/FTM/lpd/ftm-languagepacks/'


languages = []
for root, dirs, files in os.walk(startlook):
	for dir in dirs:
		if (".git" not in dir):
			languages.append(dir)
	break
print(languages)


for langname in languages:

	print(langname)
	onelang = startlook + langname

	levelplace = onelang + "/levels/"
	outputplace = onelang + "/json"
	os.makedirs(outputplace, exist_ok=True)

	for root, dirs, filenames in os.walk (levelplace):
		for fn in filenames:


			with open(root + fn) as xml_file:



				rawlevelname = fn[:-4]
				print (rawlevelname)


				data_dict = xmltodict.parse(xml_file.read())
				xml_file.close()

				# generate the object using json.dumps()
				# corresponding to json data

				levelstuff = data_dict.popitem()[1]

				ldata = levelstuff.popitem()[1]

				lsegs = ldata.popitem()[1]

				ldata = levelstuff



				l_fadeout = ldata['@HideCallout']
				l_type = ldata['@monsterInputType']
				l_group = ldata['@LettersGroup']

				sn = 0;
				for cseg in lsegs:
					cstones = cseg.popitem()[1].popitem()
					crestofword = cseg.popitem()[1]

					if (crestofword == None):

						crestofword = [];

					csreq = cseg.popitem()[1].popitem()[1]
					clocs = cseg.popitem()
					ctime = cseg.popitem()[1]

					nseg = {
						"SegmentNumber": sn,
						"prompt": {
							"OtherPromptLetters":crestofword,
						},
						"targetstones": csreq,

						"foilstones": cstones,
						"SegmentTime": ctime,
					}
					sn = sn + 1

					print(json.dumps(nseg))
					print("--")


				#json_data = json.dumps(data_dict)

				#print(json_data)




				print("-------")

				# Write the json data to output
				# json file
				#with open(outputplace + "/" +  rawlevelname + ".json", "w") as json_file:
				#	json_file.write(json_data)
			#		json_file.close()
