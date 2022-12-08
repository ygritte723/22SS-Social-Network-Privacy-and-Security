# This file is used to get the mStar ratios of the merchants



import MySQLdb

conn = MySQLdb.connect(host="localhost", port=3306, user="root", passwd="12345678", db="complaintBoard")
cur = conn.cursor()

sql = 'select * from merchant'
try:
    cur.execute(sql)
    sum = cur.rowcount
    print(sum)
except:
    print('error')


sql = 'select * from merchant where mStar=1'
try:
    cur.execute(sql)
    results = cur.rowcount
    print(results)
    print(results/sum)
except:
    print('error')

sql = 'select * from merchant where mStar=2'
try:
    cur.execute(sql)
    results = cur.rowcount
    print(results)
    print(results/sum)
except:
    print('error')

sql = 'select * from merchant where mStar=3'
try:
    cur.execute(sql)
    results = cur.rowcount
    print(results)
    print(results/sum)

except:
    print('error')

sql = 'select * from merchant where mStar=4'
try:
    cur.execute(sql)
    results = cur.rowcount
    print(results)
    print(results/sum)

except:
    print('error')

sql = 'select mname from merchant where replyratesum=1'
try:
    cur.execute(sql)
    results = cur.rowcount
    print(results)
    print(results/sum)
    results = cur.fetchall()
    for row in results:
        print(row[0])

except:
    print('error')
conn.close()
