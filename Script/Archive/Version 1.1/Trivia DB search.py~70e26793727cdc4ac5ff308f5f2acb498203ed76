import requests
import re
import csv
import io
import os
import base64
import sys
import html as htmlk
from datetime import datetime


def hooman_readable(x):
	return x.replace('"General Knowledge","', '"Genearl Knowledge"\n"').replace('","difficulty"','"\n"difficulty"').replace('","question"','"\n"question"').replace('","correct_answer"','"\n"correct_answer"').replace('","incorrect_answers"','"\n"incorrect_answers"')


def write_log(log):  # Show information, log information with timestamp
	print(log)	# Output information
	i = datetime.now()	# Fetch datetime
	with open("log.txt", "a", encoding='utf8') as log_write:
		log_write.write("[" + i.strftime('%Y/%m/%d %H:%M:%S') + "]" + " >> " + log + "\n")	# Write date then UI output to log


def get_token():  # request no duplicates, breaks at ~3198
	url = 'https://opentdb.com/api_token.php?command=request'
	html = requests.get(url).text
	token = re.findall(r'"token":"(.*?)"}', html)
	return ''.join(token)

def get_total_entries():
	url = 'https://opentdb.com/api_count_global.php'
	html = requests.get(url).text
	total = re.findall(r'"total_num_of_verified_questions":(.*?),"', html)
	category_totals = []
	for item in total:
		category_totals.append(int(item))
	return category_totals


try:
	os.remove("log.txt")  # Remove existing log file
except FileNotFoundError:
	pass	# If log doesn't exist, continue to main

x = 1
repeats = 0
adds = 0
total_adds = 0
total_category_adds = 0
amount_left_u = 50	# Max requests for each API call = 50
flag = 0
addon = 0

category = 9  # Starting category number
end = "\n"
append = ""
questions = []
qa = []
answers = []
passed_start = False
total = get_total_entries()  # Fetch question-count for overall and each category
token = get_token()  # Generate new token
qcategory = []
qtype = []
qdifficulty = []
qquestion = []
qcorrect = []
qincorrect = []
tryagain = 0
failed = 0
print(total) #show category totals

write_log("╔═════════╦═════════════════╦════════════════════════════╦═════════════════╦══════════════════════════════════════════════════════════════════════════════════╗")
while (total_adds < total[0]):	# Website shows x results but, can only x-2 can be called
	if adds == 0:
		tryagain += 1
		if tryagain == 2:
			tryagain = 0
			category += 1
			write_log("║  [ERR]  ║  Error          ║                            ║                 ║  Could not get last question(s)                                                  ║")


	url = 'https://opentdb.com/api.php?amount=50'
	url +=	'&category=' + str(category) + '&token=' + token
	repeats = 0
	adds = 0
	html = requests.get(url).text
	html_question = re.findall(r'{"category":(.*?)}', html)
	hooman_version = hooman_readable('\n'.join(html_question)).splitlines()
	print("Length of hooman_version is: " + str(len(hooman_version)))

	if (len(hooman_version) < 1):
		print("List is empty...")
		continue

	with open("Logger.txt", "a") as frick:
		frick.write(str(hooman_version))
		frick.write("\n\n\n\n")

	#sum fukkery going on here
	qx = 0
	try:
		for i in range(0, int(len(hooman_version))):
			qquestion.append(hooman_version[qx+3].replace("question:",""))
			qcategory.append(hooman_version[qx])
			qtype.append(hooman_version[qx+1].replace("type:",""))
			qdifficulty.append(hooman_version[qx+2].replace("difficulty:",""))
			qcorrect.append(hooman_version[qx+4].replace("correct_answer:",""))
			qincorrect.append(hooman_version[qx+5].replace("incorrect_answers:",""))
			adds += 1
			qx += 6
	except IndexError:
		pass
	total_adds += adds



	write_log("║  [" + "{:03d}".format(x) + "]" + "  ║  Repeats: [" +
				   "{:02d}".format(repeats) + "]  ║  Total: [" + "{:04d}".format(total_adds) +
				   "/" + str(total[0]) + "] (+" + "{:02d}".format(adds) + ")  ║  Category: [" +
				   "{:02d}".format(category) + "] ║" + "  Using Token [" + token + "]  ║")

	x += 1
	# sleep(0.1) # may reduce API bugs?
	total_category_adds += adds
write_log("╚═════════╩═════════════════╩════════════════════════════╩═════════════════╩══════════════════════════════════════════════════════════════════════════════════╝")

with io.open("trivia.csv", 'w', encoding='utf8', newline='') as f:
	file = csv.writer(f, delimiter=',')
	file.writerow(["Category", "Type", "Difficulty", "Question", "Correct Answer", "Incorrect Answer"])
	for i in range(0, total_adds):
		file.writerow([qcategory[i], qtype[i], qdifficulty[i], qquestion[i], qcorrect[i], qincorrect[i]])


write_log("Total number added: " + str(total_adds))
#input()
