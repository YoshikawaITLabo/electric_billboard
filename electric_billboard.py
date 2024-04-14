#!/usr/bin/env python3
# -*- coding: utf8 -*-

import subprocess
import re
import requests, bs4


def eprint(tline):
    tline = tline.replace('\n','')
    param = tline.split('\t')

    #文字色のパラメータ　RGB値
    try:
        param[1]

        if len(re.findall('[0-9]{1,3},[0-9]{1,3},[0-9]{1,3}', param[1])) == 0:
            parac = ''
        else:
            parac = ' -C ' + param[1]

    except IndexError:
        parac = ''

    #スクロール速度のパラメータ
    try:
        param[2]

        if len(re.findall('[0-9]{1,2}', param[2])) == 0:
            paras = ''
        else:
            paras = ' -s ' + param[2]

    except IndexError:
        paras = ''

    #背景色のパラメータ
    try:
        param[3]

        if len(re.findall('[0-9]{1,3},[0-9]{1,3},[0-9]{1,3}', param[3])) == 0:
            parab = ''
        else:
            parab = ' -B ' + param[3]

    except IndexError:
        parab = ''

    command = 'sudo'
    command += ' /home/pi/rpi-rgb-led-matrix/examples-api-use/scrolling-text-example'
    command += ' -l1'
    command += ' -y-1'

    command += parac
    command += paras
    command += parab

    command += ' --led-cols=64'
    command += ' --led-rows=32'
    command += ' --led-parallel=2'
    command += ' --led-chain=3'
    command += ' --led-no-hardware-pulse'
    command += ' --led-slowdown-gpio=4'
    command += ' -f /home/pi/Downloads/font/sazanami-20040629/sazanami-mincho60.bdf '
    command += param[0]
    print(command)
    try:
        subprocess.run(command,shell=True)
    except:
        print('subprocess.check_call() failed')

def news():
    res = requests.get('https://www3.nhk.or.jp/news/catnew.html')
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.content, "html.parser")
    elems = soup.select('em.title')
    
    l = 0
    
    for elem in elems:
        nwt = 'NHKニュース：'
        nwt += elem.getText().replace('\n','') + '\t255,255,255\t2'
        eprint(nwt)
        l += 1
        
        if l > 2:
            break

def weather():
    res = requests.get('https://tenki.jp/forecast/3/15/4520/12239/')
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.content, "html.parser")
    elems = soup.select('div.forecast-days-wrap')
    
    weather = '天気予報　'
    
    for elem in elems:
        weather += elem.getText()
        
    #整形
    weather = weather.replace(u'\xa0', '')
    weather = weather.replace('\n','　') 
    weather = weather.replace(' 　','　') 
    weather = re.sub('　{2,4}', '　', weather)
    weather = re.sub(r'降水確率　(.+?)　(.+?)　(.+?)　(.+?)　', '降水確率　00-06(\\1)　06-12(\\2)　12-18(\\3)　18-24(\\4)　　', weather)
    weather = weather.replace('時間　00-06　06-12　12-18　18-24　','') 
    weather = weather.replace('(','（') 
    weather = weather.replace(')','）') 

    weather += ' :tenki.jp提供'
    weather += '\t255,255,255\t2'

    eprint(weather)

def economic():
    res = requests.get('https://www.nikkei.com/markets/worldidx/')
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.content, "html.parser")
    elems = soup.select('table.cmn-table_style1')
    
    economic = ''
    
    for elem in elems:
        economic += elem.getText()
        
    #整形
    economic = economic.replace('\n','　') 
    economic = economic.replace(u'\xa0', '')
    economic = economic.replace('(','（') 
    economic =economic.replace(')','）') 
    economic = re.sub('　{2,4}', '　', economic)

    #必要箇所抽出
    dt1 = re.search('日経平均.+?[0-9]{1,2}:[0-9]{1,2}', economic)
    dt2 = re.search('TOPIX.+?[0-9]{1,2}:[0-9]{1,2}', economic)
    dt3 = re.search('ドル・円.+?[0-9]{1,2}:[0-9]{1,2}', economic)
    dt4 = re.search('ユーロ・円.+?[0-9]{1,2}:[0-9]{1,2}', economic)

    economici = '経済情報　'
    economici += dt1.group()
    economici += '　'
    economici += dt2.group()
    economici += '　'
    economici += dt3.group()
    economici += '　'
    economici += dt4.group()
    economici += '　日本経済新聞社提供'
    economici += '\t255,255,255\t2'

    eprint(economici)


def main():

    #テキストファイルを読み込む
    f = open('/home/pi/Documents/electric_billboard/display.txt', 'r', encoding='UTF-8')

    while True:
        line = f.readline()

        if line:
            if '[NEWS]' in line:
                news()

            elif '[WEATHER]' in line:
                weather()

            elif '[ECONOMIC]' in line:
                economic()
                
            else:
                eprint(line)
        else:
            break

    f.close()
 
if __name__ == '__main__':
    while  True:
        main()