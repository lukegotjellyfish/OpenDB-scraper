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
# print(total) show category totals

url = 'https://opentdb.com/api.php?amount=50'
url +=	'&category=' + str(category) + '&token=' + token
repeats = 0
adds = 0
html = requests.get(url).text
html_question = re.findall(r'{"category":(.*?)}', html)
hooman_version = hooman_readable('\n'.join(html_question).strip()).replace('"','').replace("]","").replace("[","").splitlines()


category = []
qtype = []
difficulty = []
question = []
correct = []
incorrect = []



try:
	x = 0
	for item in hooman_version:
		question_add = hooman_version[x+3].replace("question:","")
		if question_add in qa:
			print("repeat")
			continue
		else:
			question.append(question_add)
			qa.append(question_add)

		category.append(hooman_version[x])
		qtype.append(hooman_version[x+1].replace("type:",""))
		difficulty.append(hooman_version[x+2].replace("difficulty:",""))
		correct.append(hooman_version[x+4].replace("correct_answer:",""))
		incorrect.append(hooman_version[x+5].replace("incorrect_answers:",""))
		x += 6
except IndexError:
	pass


with io.open("trivia.csv", 'w', encoding='utf8', newline='') as f:
	file = csv.writer(f, delimiter=',')
	file.writerow(["Category", "Type", "Difficulty", "Question", "Correct Answer", "Incorrect Answer"])
	for i in range(0, 2):
		file.writerow([category[i], qtype[i], difficulty[i], question[i], correct[i], incorrect[i]])
print("Dun")

input()