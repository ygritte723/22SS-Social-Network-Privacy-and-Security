# This file is used to scrapy the merchants information.

from __future__ import division
from bs4 import BeautifulSoup
import traceback
import MySQLdb
from datetime import datetime
from time import sleep
from difflib import SequenceMatcher
from selenium import webdriver


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def crawMerchant():
    conn = MySQLdb.connect(host="localhost", port=3306, user="root", passwd="12345678", db="complaintBoard")
    cur = conn.cursor()

    logFile = '/Users/mac/Documents/2022春夏/社交网络隐私与安全/lab/lab1/log/error_log.txt'
    errorHandle = open(logFile, 'a+')

    # path2webdriver = '/usr/local/bin/chromedriver.exe'
    driver = webdriver.Chrome()

    def craw_in_page(urlStr):
        sleep(1.5)

        try:
            driver.get(urlStr)
        except:
            traceback.print_exc()
            errorHandle.write('Not go well with opening: ' + urlStr + '\n' + traceback.format_exc() + '\n')
            sleep(2)

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        platform = 'complaintBoard'

        mid = ''
        # error = ''
        dateStr = ''
        mname = ''
        mStar = ''
        sumSUM = ''
        replySUM = ''
        replyRateSUM = ''

        # dateNum = str(int(round(time.time() * 1000))).strip('L')

        hrefS = []
        hrefS = soup.findAll('a', {'class': 'block item-row bname-row'})

        for href in hrefS:
            DT = datetime.now()
            dateStr = DT.strftime('%Y-%m-%d %H:%M:%S')

            if len(href) > 0:
                complaintUrl = href.get('href')
                complaintUrl = 'https://www.complaintsboard.com' + complaintUrl
                # mid
                mid = href.get('id')

                if mid[0] != 'b':
                    # print(href)
                    href = href.contents
                    href = str(href[1])
                    # print(href)
                    if href:
                        href = href.replace('\n', '')
                        href = href.replace('<div class="info"><h4>', '')
                        href = href.replace(
                            '<div class="rating small"><div class="stars2 star2_1"><i><i></i></i></div>', '')
                        href = href.replace('Reviews</div></div>', '')
                        href = href.replace('</h4>', '')
                        href = href.replace(' ', '')
                    print(href)
                    # mname
                    mname = href[:-1]
                    # mname = href.contents[0]

                    # mStar
                    mStar = 1
                    # print(mStar)

                    # sumSUM
                    sumSUM = href[-1]
                    # print(sumSUM)
                    # sumSUM = sumSUM.removeprefix('"')
                    # sumSUM = sumSUM.removesuffix(' Reviews"')

                    try:
                        query = "INSERT INTO merchant (dateStr, mid, mname, mstar, sumSUM) values " + \
                                "(%s, %s, %s, %s, %s) " + \
                                "ON DUPLICATE KEY UPDATE " + \
                                "dateStr = VALUES(dateStr)," + \
                                "mid = VALUES(mid)," + \
                                "mname = VALUES(mname)," + \
                                "mStar = VALUES(mStar)," + \
                                "sumSUM = VALUES(sumSUM)"

                        params = (dateStr, mid, mname, mStar, sumSUM)
                        cur.execute(query, params)
                        conn.commit()
                    except:
                        traceback.print_exc()
                        errorHandle.write('ERROR mid = ' + mid + '\n')
                        print
                        "ERROR mid = ", mid
                        conn.rollback()
                    continue
                # print(mid)

            try:
                driver.get(complaintUrl)
            except:
                traceback.print_exc()
                errorHandle.write('Not go well with opening: ' + complaintUrl + '\n' + traceback.format_exc() + '\n')
                sleep(2)

            soup = BeautifulSoup(driver.page_source, 'html.parser')

            # mname
            companyName = soup.findAll('div', {'class': 'bn-header__image-title'})
            if len(companyName) > 0:
                mname = companyName[0].contents
                mname = mname[0]
                # print(mname)

            # mStar
            starS = soup.findAll('span', {'class': 'bn-profile__info-rating-star bn-profile__info-rating-star--full'})
            if len(starS) > 0:
                mStar = len(starS)
                # print(mStar)

            # sumSUM
            sumSUMS = soup.findAll('a', {'class': 'bn-profile__info-rating-text'})
            if len(sumSUMS) > 0:
                sumSUM = sumSUMS[0].contents
                sumSUM = sumSUM[0].split(' ')
                sumSUM = str(sumSUM[0])
                # print(sumSUM)

            # replySUM
            replySUMS = soup.findAll('span', {'class': 'bn-profile__info-resolved'})

            if len(replySUMS) > 0:
                replySUM = replySUMS[0].contents
                replySUM = replySUM[3]
                replySUM = str(replySUM.contents[0])
                # print(replySUM)
                # print('\n')

            # replyRate
            if sumSUM:
                replyRate = float(replySUM) / float(sumSUM)
                replyRate = round(replyRate, 3)
                replyRateSUM = str(replyRate)
                # print(replyRateSUM)

            try:
                query = "INSERT INTO merchant (dateStr, mid, mname, mstar, replySUM, replyRateSUM, sumSUM) values " + \
                        "(%s, %s, %s, %s, %s, %s, %s) " + \
                        "ON DUPLICATE KEY UPDATE " + \
                        "dateStr = VALUES(dateStr)," + \
                        "mid = VALUES(mid)," + \
                        "mname = VALUES(mname)," + \
                        "mStar = VALUES(mStar)," + \
                        "replySUM = VALUES(replySUM)," + \
                        "replyRateSUM = VALUES(replyRateSUM)," + \
                        "sumSUM = VALUES(sumSUM)"

                params = (dateStr, mid, mname, mStar, replySUM, replyRateSUM, sumSUM)
                cur.execute(query, params)
                conn.commit()
            except:
                traceback.print_exc()
                errorHandle.write('ERROR mid = ' + mid + '\n')
                print
                "ERROR mid = ", mid
                conn.rollback()

    urlStr = 'https://www.complaintsboard.com/bycategory/internet-services'

    craw_in_page(urlStr)

    pages = range(2, 74)

    for page in pages:
        page = str(page)
        urlStr = 'https://www.complaintsboard.com/bycategory/internet-services/page/' + page
        craw_in_page(urlStr)


crawMerchant()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
