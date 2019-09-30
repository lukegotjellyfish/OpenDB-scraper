# -*- coding: utf-8 -*-
import requests
import re
import csv
import io
import os
import base64
import sys
import codecs
import html as htmlk
from datetime import datetime
from time import sleep


def write_log(log, mode, filename):  # Show information, log information with timestamp
    if (mode == 1):
        print(log)  # Output information
    i = datetime.now()  # Fetch datetime
    with open(filename, "a", encoding='utf-8') as log_write:
        log_write.write("[" + i.strftime('%Y/%m/%d %H:%M:%S') + "]" + " >> " + log + "\n")  # Write date then UI output to log


def get_token():  # Generate a token to stop duplicate questions
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

files = ["log.txt", "repeat_questions.txt", "trivia.csv"]
for item in files:
    try:
        os.remove(item)
    except FileNotFoundError:
        continue
sleep(1)

x = 1
repeats = 0
adds = 0
total_adds = 0
total_category_adds = 0
amount_left_u = 50  # Max requests for each API call = 50
repeat_counter = 0

category = 9  # Starting category number
end = "\n"
append = ""
questions = []
qa = []
answers = []
qcategories = []
qtype = []
qdifficulty = []
qincorrect_answers = []
passed_start = False
total = get_total_entries()  # Fetch question-count for overall and each category
token = get_token()  # Generate new token
# print(total) show category totals

write_log("╔═════════╦═════════════════╦════════════════════════════╦══════════════════════════╦══════════════════════════════════════════════════════════════════════════════════╗", 1, "log.txt")
while (total_adds < total[0]):  # Website shows x results but, can only x-2 can be called
    if ((passed_start == True) and (total_category_adds >= total[category - 8])):
        #print("finished category [" + str(category-8) + "]")
        category += 1
        total_category_adds = 0
        repeat_counter = 0

    try:
        amount_left_u = total[category - 8] - total_category_adds - repeat_counter
    except IndexError:
      break  # 32 and tried 33 (if categories get added)

    url = 'https://opentdb.com/api.php?amount=' + str(amount_left_u) + "&encode=base64"
    url +=	'&category=' + str(category) + '&token=' + token
    repeats = 0
    adds = 0
    html = requests.get(url).text
    html_q = re.findall(r'"question":"(.*?)","c', html)
    html_a = re.findall(r'"correct_answer":"(.*?)","incorrect', html)
    html_category = re.findall(r'"category":"(.*?)",', html)
    html_type = re.findall(r'"type":"(.*?)",', html)
    html_difficulty = re.findall(r'"difficulty":"(.*?)",', html)
    html_incorrect_answers = re.findall(r'"incorrect_answers":\[(.*?)]', html)

    for o in range(0, len(html_q)):
        if html_q[o] in qa:
            repeat_counter += 1
            write_log(
            "Repeat Question:"+
            "\n  Question: "+ str(base64.b64decode(html_q[o]), "utf-8")+
            "\n  Category: " + str(base64.b64decode(html_category[o]), "utf-8")+
            "\n  Type: " + str(base64.b64decode(html_type[o]), "utf-8")+
            "\n  Difficulty: " + str(base64.b64decode(html_difficulty[o]), "utf-8")+
            "\n  Answer: " + str(base64.b64decode(html_a[o]), "utf-8")+
            "\n  Incorrect Answers: " + str(html_incorrect_answers[o].replace('"',"").split(","))+
            "\n"
            , 0, "repeat_questions.txt")
            repeats += 1
            continue
        else:
            questions.append(html_q[o])
            qa.append(html_q[o])
            adds += 1
            answers.append(html_a[o])
            qcategories.append(html_category[o])
            qtype.append(html_type[o])
            qdifficulty.append(html_difficulty[o])
            qincorrect_answers.append(html_incorrect_answers[o].replace('"',"").split(","))


    total_adds += adds
    total_category_adds += adds

    if (adds == 0):
        write_log("║  [ERR]  ║  Error          ║                            ║                          ║  Could not get last question(s)                                                  ║", 1, "log.txt")
        total_category_adds = total[category - 8]
        continue  # Don't write log

    write_log("║  [" + "{:03d}".format(x) + "]" + "  ║  Repeats: [" +
    "{:02d}".format(repeats) + "]  ║  Total: [" + "{:04d}".format(total_adds) +
    "/" + str(total[0]) + "] (+" + "{:02d}".format(adds) + ")  ║  Category: [" +
    "{:02d}".format(category) + "[" + "{:03d}".format(total_category_adds) + "/" +
    "{:03d}".format(total[category - 8]) + "]] ║" + "  Using Token [" +
    token + "]  ║", 1, "log.txt")

    x += 1
    # sleep(0.1) # may reduce API bugs?
    if (passed_start != True):
        passed_start = True
write_log("╚═════════╩═════════════════╩════════════════════════════╩══════════════════════════╩══════════════════════════════════════════════════════════════════════════════════╝", 1, "log.txt")

final = 0
with io.open("trivia.csv",'w', encoding='utf-8', newline='') as f:
    file = csv.writer(f, delimiter=',')
    file.writerow(["Category", "Type", "Difficulty", "Question", "Answer", "Incorred Answers"])
    for i in range(0, len(answers)):
        file.writerow([
        str(base64.b64decode(qcategories[i]), "utf-8"),
        str(base64.b64decode(qtype[i]), "utf-8"),
        str(base64.b64decode(qdifficulty[i]), "utf-8"),
        questions[i],
        answers[i],
        qincorrect_answers[i]])
        final += 1

write_log("Total number added: " + str(final), 1, "log.txt")
