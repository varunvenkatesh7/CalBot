import pandas as pd
import calendar
abbr_to_num = {name: num for num, name in enumerate(calendar.month_abbr) if num}
csv1 = pd.read_csv('output1.csv')
df = pd.DataFrame(csv1)
#print(df.head(10))
csv2=pd.read_csv('output2.csv', names =["Date", "Reading"])
df2 = pd.DataFrame(csv2)
#print(df2)
for row in df2.iterrows():
    date_string = row[1][0]
    date_string = date_string.split()
    date = date_string[0:3]
    reading_value = row[1][1]
    lecture_topic = date_string[3:]

    date_word=""
    for word in date:
        date_word = date_word + word+ " "

    lecture_topic_word=""
    for word in lecture_topic:
        lecture_topic_word = lecture_topic_word + word+ " "
    new_row={'Date': date_word , 'Lecture Topic' : lecture_topic_word ,'Reading' : reading_value}
    df = df.append(new_row, ignore_index=True)

print(df)
df.to_csv(r'schedule.csv', index=False)



