# This file is used to plot the word cloud of each brand.



import MySQLdb
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt


conn = MySQLdb.connect(host="localhost", port=3306, user="root", passwd="12345678", db="complaintBoard")
cur = conn.cursor()

sql = "SELECT company FROM COMPLAINTS \
      "
try:
    cur.execute(sql)
    results = cur.fetchall()
    company = list(set(results))
    # company = list(company)
    # print(company)

except:
    print("error")

for com in company:
    com = str(com[0])
    print(com)
    sql = "SELECT TEXT FROM COMPLAINTS \
          WHERE company = '%s' " % (com)

    text_all = ''
    try:
        cur.execute(sql)
        results = cur.fetchall()
        for row in results:
            text_all += row[0]

    except:
        print("error")

    wcloud = WordCloud(width=2800, height=1600, stopwords=STOPWORDS).generate(text_all)
    path = com + '.jpg'

    wcloud.to_file(path)

    plt.imshow(wcloud)
    plt.axis('off')
    plt.show()
conn.close()