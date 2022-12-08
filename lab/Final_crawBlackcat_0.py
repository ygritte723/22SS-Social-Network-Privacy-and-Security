# -*- coding: utf-8 -*-
#!/usr/bin/python
# The following will run infinity times on screen till user hit CTRL+C
# The program will sleep for 1 second before updating date and time again.
import urllib2
import urllib
from urllib import unquote
from selenium import webdriver
from bs4 import BeautifulSoup
import re
import traceback
import MySQLdb 

import time
from datetime import datetime
from datetime import timedelta
from threading import Timer
from threading import Thread
from time import sleep

import sys
import requests
from random import random
from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def crawComplaintBatch():
    conn = MySQLdb.connect(host="localhost", port=3306, user="root", passwd="", db="blackcat", charset="utf8")
    cur = conn.cursor()

    logFile = 'log/error_log.txt'
    errorHandle = open(logFile, 'a+')

    path2webdriver = 'E:/Ad_project/chromedriver_win32/chromedriver.exe'
    driver = webdriver.Chrome(executable_path=path2webdriver)
    #arrID = ['17356106806','17356108183','17356114260','17356114822','17356117030','17356117134','17356118774','17356118790','17356118797','17356118811','17356118820','17356119631','17356119649','17356119650','17356119655','17356119678','17356119906','17356119967','17356119976','17356119981','17356119991','17356120082','17356120111','17356236844','17356236851','17356237195','17356237654','17356237683','17356237765','17356238447','17347295891','17347225891','17347224091','17347218791','17347217891','17347217191','17347216710','17347216706','17356240361']
    #arrID = ['17347224091'] # ['17356117134']#['17356237683','17347216710','17356117134'] #['17356121320'] # ['17356106806']

    #arrID = range(17347216704, 17356287146)
    # to do: re-crawl (17347216704, 17347224380)

    #arrID = range(17347224380, 17356287146)    https://tousu.sina.com.cn/complaint/view/17355925396/
    arrID = range(17347645304, 17347650000) + range(17347650000, 17347750000) 
    for cid in arrID:
        sleep(1.5)
        cid = str(cid)
        urlStr = 'https://tousu.sina.com.cn/complaint/view/' + cid + '/'

        try:
            driver.get(urlStr)
        except:
            traceback.print_exc()
            errorHandle.write('Not go well with opening: ' + urlStr + '\n' + traceback.format_exc() + '\n')
            sleep(2)
            continue

        #driver.get(urlStr)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        platform = u"黑猫消费者服务平台"

        #cid = ''
        mid = ''
        uname = ''
        merchant = ''
        title = ''
        issue = ''
        demand = ''
        money = ''
        state = ''
        thumbupNum = ''
        commentNum = ''
        shareNum = ''
        uStartTime = ''
        uComplainDetail = ''
        groupStartTime = ''
        groupStarter = ''
        groupComplainDetail = ''
        uSupTime = ''
        uSupDetail = ''
        uConfirmDoneTime = ''
        uConfirmDone = ''
        uFinalComment = ''
        uStarService = ''
        uStarSpeed = ''
        uStarOverall = ''
        pCheckPassTime = ''
        pNoPassTime = ''
        pMerchantProcessTime = ''
        pMerchantProcess = ''
        pReplyTime = ''
        pReply = ''
        pAutoCompleteTime = ''
        pAutoComplete = ''
        pMerchantNotInTime = ''
        pMerchantNotIn = ''
        mApply4CompleteTime = ''
        mApply4Complete = ''
        mReplyTime = ''
        mReply = ''
        numIMAGE = 0

        # 投诉单不存在 or 当前投诉单只允许本人查看
        divS = soup.findAll('div', {'class':'error'})
        if len(divS) > 0:
            error = divS[0].text.strip()
            #print '--------------error!--------------'

            DT = datetime.now()
            dateStr = DT.strftime('%Y-%m-%d %H:%M:%S') 
            try:
                query = u"INSERT INTO complaint (dateStr, cid, error) values (%s, %s, %s) ON DUPLICATE KEY UPDATE dateStr = VALUES(dateStr)"
                params = (dateStr, cid, error)
                cur.execute(query, params)
                conn.commit()
            except:
                traceback.print_exc()
                errorHandle.write('ERROR cid = ' + cid + ': Not Available\n')
                conn.rollback()
            continue

        # title 2
        h1S = soup.findAll('h1', {'class':'article'})
        if len(h1S) > 0:
            title = h1S[0].text.replace('\n', '').replace('\t', '').strip()

        # uname
        spanS = soup.findAll('span', {'class':'u-name'})
        if len(spanS) > 0:
            uname = spanS[0].text.replace('\n', '').replace('\t', '').strip()
            uname = uname.replace(' ', '')

        # postTime
        spanS = soup.findAll('span', {'class':'u-date'})
        postTime = ''
        year = ''
        if len(spanS) > 0:
            partS = spanS[0].text.strip().split(' ')
            postTime = partS[1] + ' ' + partS[2]
            postTime = postTime.strip()
            if u"年" in postTime:
                year = postTime.split(u"年")[0]

        # detailed complaint info
        ul = soup.find('ul', {'class':'ts-q-list'})
        #get all li elements under ul
        liS = ul.findAll('li')
        rNum = len(liS)
        if rNum > 4:
            cid = liS[0].text.replace('\n', '').replace('\t', '').replace(' ', '').strip().split(u"：")
            merchant = liS[1].text.replace('\n', '').replace('\t', '').replace(' ', '').strip().split(u"：")
            demand = liS[rNum-3].text.replace('\n', '').replace('\t', '').replace(' ', '').strip().split(u"：")
            money = liS[rNum-2].text.replace('\n', '').replace('\t', '').replace(' ', '').strip().split(u"：")
            state = liS[rNum-1].text.replace('\n', '').replace('\t', '').replace(' ', '').strip().split(u"：")

            if rNum > 5:
                issue = liS[2].text.replace('\n', '').replace('\t', '').replace(' ', '').strip().split(u"：")

            aTag = liS[1].find('a', {'suda-uatrack':'key=complaint_company'})
            if aTag != None:
                mid = aTag['href'].split('=')[-1]
                #company = aTag.text.strip()

            if len(cid) > 1:
                cid = cid[1]
            if len(merchant) > 1:
                merchant = merchant[1]
                if u"商家只有入驻" in merchant:
                    merchant = merchant.split(u"商家只有入驻")[0]
            if len(issue) > 1:
                issue = issue[1]
            if len(demand) > 1:
                demand = demand[1]
            if len(money) > 1:
                money = money[1]
            if len(state) > 1:
                state = state[1]

        # thumbup num
        spanS = soup.findAll('span', {'suda-uatrack':'key=complaint_move&value=dianzan'})
        if len(spanS) > 0:
            thumbupNum = spanS[0].text.strip()

        # comment num
        spanS = soup.findAll('span', {'class':'new_msg'})
        if len(spanS) > 0:
            commentNum = spanS[0].text.strip()

        # share num
        spanS = soup.findAll('span', {'suda-uatrack':'key=complaint_move&value=fenxiang'})
        if len(spanS) > 0:
            shareNum = spanS[0].text.replace('\n', '').replace(' ', '')
            shareNum = re.sub('[^0-9]','', shareNum)

        # detailed process
        divS = soup.findAll('div', {'class':'ts-d-item'})
        for div in divS:
            status = div.text.replace('\n', '')
            status = status.replace('\t', ' ')
            status = status.replace(uname, 'USER')
            status = status.replace(merchant, 'MERCHANT')
            status = status.replace(platform, 'PLATFORM')
            status = status.replace(u"黑猫投诉", 'PLATFORM') 

            time = ''
            matchobj = re.search("(\d\d\-\d\d\s\d\d\:\d\d\:\d\d)", status)
            if matchobj != None:
                time = (matchobj.group(0)).strip()
            rest = status.replace(time, '|||')
            #rest = re.sub('\s{2,}','|||', rest).strip()

            if u"满意度：" in status:
                uFinalComment = rest.replace(u"服务态度：处理速度：满意度：", '') 
                uFinalComment = uFinalComment.replace(u"USER评价|||", '') 
                spanS = div.select("span[class^=star]") #.findAll('span', class=re.compile('^star'))
                if len(spanS) > 2:
                    uStarService = ''.join(spanS[0]['class']).replace('star', '')
                    uStarSpeed = ''.join(spanS[1]['class']).replace('star', '')
                    uStarOverall = ''.join(spanS[2]['class']).replace('star', '')
                    threeStar = uStarService + ':' + uStarSpeed + ':' + uStarOverall
                    rest = uFinalComment + '|' + threeStar
            output = year + '-' + time + '|||' + rest

            partS = output.split('|||')
            if len(partS) == 3:
                content = partS[1]
                content_bak = content
                if content.startswith(u"商"):
                    content = content.replace(u"商", '')
                if 'USER' not in content and 'MERCHANT' not in content and 'MERCHANT' not in content:
                    checkStr = ''
                    if content.endswith(u"回复"):
                        checkStr = content.replace(u"回复", '')
                    if content.endswith(u"申请完成投诉"):
                        checkStr = content.replace(u"申请完成投诉", '')
                    if checkStr != '':
                        if similar(checkStr, merchant) >= 0.33:
                            content = content.replace(checkStr, 'MERCHANT')
                        elif similar(checkStr, uname) >= 0.33:
                            content = content.replace(checkStr, 'USER')

                if u"发起投诉" in content or u"USER参与集体投诉" in content or u"USER发起集体投诉" in content:
                    uStartTime = partS[0].strip()
                    uComplainDetail = partS[2].strip()

                if u"发起集体投诉" in content:
                    groupStartTime = partS[0].strip()
                    groupStarter = content.replace(u"发起集体投诉", '')
                    groupComplainDetail = partS[2].strip()  
                elif u"USER补充投诉" in content:
                    uSupTime = partS[0].strip()
                    uSupDetail = partS[2].strip()
                elif u"USER确认完成" in content:
                    uConfirmDoneTime = partS[0].strip()
                    uConfirmDone = partS[2].strip()
                elif u"USER评价" in content:
                    uFinalCommentTime = partS[0].strip()
                    uFinalComment = uFinalComment
                    uStarService = uStarService
                    uStarSpeed = uStarSpeed
                    uStarOverall = uStarOverall

                elif u"PLATFORM审核通过" in content:
                    pCheckPassTime = partS[0].strip()
                elif u"PLATFORM" in content and u"审核" in content and u"未" in content and u"通过" in content:
                    pNoPassTime = partS[0].strip()
                elif u"PLATFORM商家处理中" in content:
                    pMerchantProcessTime = partS[0].strip()
                    pMerchantProcess = partS[2].strip()
                elif u"PLATFORM自动完成" in content:
                    pAutoCompleteTime = partS[0].strip()
                    pAutoComplete = partS[2].strip()
                elif u"PLATFORM商家未入驻" in content:
                    pMerchantNotInTime = partS[0].strip()
                    pMerchantNotIn = partS[2].strip()                    
                elif u"PLATFORM回复" in content:
                    pReplyTime = partS[0].strip()
                    pReply = partS[2].strip()   

                elif u"MERCHANT申请完成投诉" in content:
                    mApply4CompleteTime = partS[0].strip()
                    mApply4Complete = partS[2].strip()
                    if u"最终解决方案解决方案：" in mApply4Complete:
                        mApply4Complete = mApply4Complete.replace(u"最终解决方案解决方案：", '')
                    elif u"解决方案：" in mApply4Complete:
                        mApply4Complete = mApply4Complete.replace(u"解决方案：", ': ')
                elif u"MERCHANT回复" in content:
                    mReplyTime = partS[0].strip()
                    mReply = partS[2].strip()  

                if content != content_bak:
                    output = partS[0] + '|||' + content + '|||' + partS[2] 

        imgS = soup.findAll('img', {'class':'example-image lazyload'})
        i = 0
        imageURLS = []
        for img in imgS:
            dataSRC = img['data-src']
            dataSRC = unquote(dataSRC)                
            partS = dataSRC.split('&img=')
            if len(partS) >= 2:
                image_url = partS[1]
                #sleep(2)
                try:
                    response = requests.get(image_url, stream = True)
                    if not response.ok:
                        print 'response = ', response
                    else:                     
                        img_data = response.content
                        fileName = cid + '_' + str(random())[2:]
                        with open('images_12.5/' + fileName + '.jpg', 'wb') as handler:
                            handler.write(img_data)
                            handler.close()
                        numIMAGE += 1
                        i += 1
                except:
                    print cid + ': image retrieval error!'
                    DT = datetime.now()
                    dateStr = DT.strftime('%Y-%m-%d %H:%M:%S')
                    errorHandle.write(cid + ': image retrieval error!\t' + dateStr + '\n')
                    sleep(2)

        #dateNum = str(int(round(time.time() * 1000))).strip('L')
        DT = datetime.now()
        dateStr = DT.strftime('%Y-%m-%d %H:%M:%S') 

        try:
            query = u"INSERT INTO complaint (dateStr, cid, mid, uname, merchant, title, issue, demand, `money`, state, \
                thumbupNum, commentNum, shareNum, uStartTime, uComplainDetail, groupStartTime, groupStarter, groupComplainDetail, \
                uSupTime, uSupDetail, uConfirmDoneTime, uConfirmDone, uFinalComment, uStarService, uStarSpeed, uStarOverall, \
                pCheckPassTime, pNoPassTime, pMerchantProcessTime, pMerchantProcess, pReplyTime, pReply, pAutoCompleteTime, pAutoComplete, \
                pMerchantNotInTime, pMerchantNotIn, mApply4CompleteTime, mApply4Complete, mReplyTime, mReply, numIMAGE) values "+\
                 "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, \
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) " +\
                "ON DUPLICATE KEY UPDATE "+\
                "dateStr = VALUES(dateStr),"+\
                "issue = VALUES(issue),"+\
                "demand = VALUES(demand),"+\
                "money = VALUES(money),"+\
                "state = VALUES(state),"+\
                "thumbupNum = VALUES(thumbupNum),"+\
                "commentNum = VALUES(commentNum),"+\
                "shareNum = VALUES(shareNum),"+\
                "groupStartTime = VALUES(groupStartTime),"+\
                "groupStarter = VALUES(groupStarter),"+\
                "groupComplainDetail = VALUES(groupComplainDetail),"+\
                "uSupTime = VALUES(uSupTime),"+\
                "uSupDetail = VALUES(uSupDetail),"+\
                "uConfirmDoneTime = VALUES(uConfirmDoneTime),"+\
                "uConfirmDone = VALUES(uConfirmDone),"+\
                "uFinalComment = VALUES(uFinalComment),"+\
                "uStarService = VALUES(uStarService),"+\
                "uStarSpeed = VALUES(uStarSpeed),"+\
                "uStarOverall = VALUES(uStarOverall),"+\
                "pCheckPassTime = VALUES(pCheckPassTime),"+\
                "pNoPassTime = VALUES(pNoPassTime),"+\
                "pMerchantProcessTime = VALUES(pMerchantProcessTime),"+\
                "pMerchantProcess = VALUES(pMerchantProcess),"+\
                "pReplyTime = VALUES(pReplyTime),"+\
                "pReply = VALUES(pReply),"+\
                "pAutoCompleteTime = VALUES(pAutoCompleteTime),"+\
                "pAutoComplete = VALUES(pAutoComplete),"+\
                "pMerchantNotInTime = VALUES(pMerchantNotInTime),"+\
                "pMerchantNotIn = VALUES(pMerchantNotIn),"+\
                "mApply4CompleteTime = VALUES(mApply4CompleteTime),"+\
                "mApply4Complete = VALUES(mApply4Complete),"+\
                "mReplyTime = VALUES(mReplyTime),"+\
                "mReply = VALUES(mReply),"+\
                "numIMAGE = IF(VALUES(numIMAGE) > numIMAGE, VALUES(numIMAGE), numIMAGE)"

            params = (dateStr, cid, mid, uname, merchant, title, issue, demand, money, state, thumbupNum, commentNum, shareNum, uStartTime, \
                uComplainDetail, groupStartTime, groupStarter, groupComplainDetail, uSupTime, uSupDetail, uConfirmDoneTime, \
                uConfirmDone, uFinalComment, uStarService, uStarSpeed, uStarOverall, pCheckPassTime, pNoPassTime, pMerchantProcessTime, \
                pMerchantProcess, pReplyTime, pReply, pAutoCompleteTime, pAutoComplete, pMerchantNotInTime, pMerchantNotIn, \
                mApply4CompleteTime, mApply4Complete, mReplyTime, mReply, numIMAGE)
            cur.execute(query, params)
            conn.commit()
        except:
            traceback.print_exc()
            errorHandle.write('ERROR cid = ' + cid + '\n')
            print "ERROR cid = ", cid
            conn.rollback()



# ----------------------------------entrance of the program--------------------------#
cStr = 'https://tousu.sina.com.cn/complaint/view/17356129146/' # 'https://tousu.sina.com.cn/complaint/view/17356121320/' #'https://tousu.sina.com.cn/complaint/view/17356240361/' #'https://tousu.sina.com.cn/complaint/view/17347216706/' #'https://tousu.sina.com.cn/complaint/view/17356139256/' # 'https://tousu.sina.com.cn/complaint/view/17356200540/'
mStr = 'https://tousu.sina.com.cn/company/view/?couid=2092643773'


crawComplaintBatch()
