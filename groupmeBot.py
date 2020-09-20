import requests, time, pandas as pd, calendar
from datetime import datetime
abbr_to_num = {name: num for num, name in enumerate(calendar.month_abbr) if num}

# GETTING DATA FROM CSV THAT HAS DATES, TOPICS, ETC
df = pd.read_csv('schedule.csv')
list_of_rows = [list(row) for row in df.values]
# FIXING DATES AND DATAPROC
for row in list_of_rows:
    try:
        curr_date = row[0]
        month_num = (abbr_to_num[curr_date.split()[1]])
        if month_num < 10:
            month_num ='0'+str(month_num)
        month_num = str(month_num)
        date_num = int(curr_date.split()[2])
        if date_num < 10:
            date_num = str('0' + str(date_num))
        date_num = str(date_num)
        year_num = '2020'
        time_num = '14:50:00'
        full_date = month_num + ":" + date_num + ":" + year_num +" " +time_num
        row[0] = datetime.strptime(full_date,'%m:%d:%Y %H:%M:%S')
    except:
        print()

#data gathered, now getting the closest lecture date in the future
current_closest_date_index = 0
flag =False
for row in range(len(list_of_rows)):
    try:
        todays_date_and_time = datetime.now()
        minumum = list_of_rows[row][0] - todays_date_and_time
        if minumum.days >= 0:
            current_closest_date_index = row
            break
    except:
        continue

#data gathered, now getting the closest exam date in the future
current_closest_exam_index = 0 
for row in range(len(list_of_rows)):
    try:
        todays_date_and_time = datetime.now()
        minumum_exam = list_of_rows[row][0] - todays_date_and_time
        if minumum_exam.days >= 0 and 'EXAM' in list_of_rows[row][1]:
            current_closest_exam_index = row
            break
    except:
        continue

#setting up urls and credentials for http requests
URL = 'GROUPME URL'

POST_URL = 'https://api.groupme.com/v3/bots/post'

#getting latest message id(for invoking bot)
response = requests.get(url=URL, params={'token' :'TOKEN', 'limit':1})
latest_message = (response.json()['response']['messages'][0])
latest_since_id = latest_message['id']
#more creds
PARAMS ={'token' :'TOKEN','since_id' : latest_since_id}

while True:
    #checks if the current date is less than 24h before lecture
    date_and_time_of_closest = list_of_rows[current_closest_date_index][0]
    todays_date_and_time = datetime.now()
    minumum = date_and_time_of_closest - todays_date_and_time
    
    if minumum.total_seconds() < 86400:
        message_text = "Reminder: Lecture Tomorrow. The Topic(Planned) is " + list_of_rows[current_closest_date_index][1] + ", and the Reading is Chapter: " + list_of_rows[current_closest_date_index][2]
        message = {"bot_id"  : "BOT_ID", "text" : message_text}
        #response = requests.post(url=POST_URL, data=message)
        #print(response)
        print(message_text)
        current_closest_date_index +=1
        minumum = list_of_rows[current_closest_date_index][0]
        
    #checking if an exam is within 7 days of the current date
    date_and_time_of_closest_exam = list_of_rows[current_closest_exam_index][0]
    todays_date_and_time = datetime.now()
    minumum_exam = date_and_time_of_closest_exam - todays_date_and_time

    if minumum_exam.total_seconds() < 7*86400:
        message_text = "Reminder: " + list_of_rows[current_closest_exam_index][1] +" in 10 days. Get to Studying!"
        message = {"bot_id" : "BOT_ID", "text" : message_text}
        response = requests.post(url=POST_URL, data=message)
        print(response)
        print(message_text)

        flag = False
        for index in range(len(list_of_rows)):  
            
            first_word = str(list_of_rows[index][1]).split()[0]
        
            if "EXAM" in str(first_word) and index > current_closest_exam_index:
                current_closest_exam_index = index
                minumum_exam = list_of_rows[current_closest_exam_index][0]
                print(minumum_exam)
                flag = True
            
            if flag==True:
                break

    #checking if the bot is being invoked
    response = requests.get(url=URL, params=PARAMS)
    if response.status_code ==200:
        messages = response.json()['response']['messages']
    
        for each_message in messages:
            if "calbot next" in each_message['text']:
                message_text = "Reminder: Lecture on " + str(list_of_rows[current_closest_date_index][0])+", and the Topic(Planned) is " + list_of_rows[current_closest_date_index][1] + ", and the Reading is Chapter: " + list_of_rows[current_closest_date_index][2]
                message = {"bot_id"  : "BOT_ID","text"    : message_text}
                response = requests.post(url=POST_URL, data=message) 
            PARAMS['since_id'] = str(each_message['id'])
            break
        
    time.sleep(20)