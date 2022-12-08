# This file is used to plot the word cloud of all brands.



import MySQLdb
from wordcloud import WordCloud
from wordcloud import STOPWORDS
import matplotlib.pyplot as plt


conn = MySQLdb.connect(host="localhost", port=3306, user="root", passwd="12345678", db="complaintBoard")
cur = conn.cursor()


sql = "SELECT TEXT FROM COMPLAINTS \
      "
text_all =''
try:
    cur.execute(sql)
    results = cur.fetchall()
    for row in results:
        text_all += row[0]

except:
    print("error")

# filename = "covid19.txt"
# with open(filename) as f:
# mytext = f.read()
print(type(text_all))

wcloud = WordCloud(width=2800, height=1600, stopwords=STOPWORDS).generate(text_all)
wcloud.to_file('cloud_all.jpg')
plt.imshow(wcloud)
plt.axis('off')
plt.show()
conn.close()