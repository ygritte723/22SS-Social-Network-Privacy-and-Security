# This file is used to detect the sumSUM ratios of the merchant



import MySQLdb


conn = MySQLdb.connect(host="localhost", port=3306, user="root", passwd="12345678", db="complaintBoard")
cur = conn.cursor()

sql = 'select sumSUM from merchant'
sum = 0
try:
    cur.execute(sql)
    results = cur.fetchall()
    for row in results:
        sum += float(row[0])
except:
    print('error')
sum_all = sum
print(sum_all)

sql = 'select sumSUM from merchant \
      where sumSUM=1'
sum = 0
try:
    cur.execute(sql)
    results = cur.fetchall()
    print(results)
    for row in results:
        sum += float(row[0])
except:
    print('error')

conn.close()
print(len(results))
print(sum)
print(len(results)/1170.0)
print(sum/sum_all)
