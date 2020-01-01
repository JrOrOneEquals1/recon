#!/usr/bin/env python

import os, argparse, time, sys
from selenium import webdriver
from importlib import import_module

parser = argparse.ArgumentParser(description='This tool uses Python Selenium to parse through certain sites and retrieve IP addresses, and emails.')
parser.add_argument('-d', '--domain', help="Customer's web domain.", required=True)
parser.add_argument('-n', '--name', help="All of the customer's names.", required=True, nargs='*')
parser.add_argument('-eF', '--emailFile', help="File name of where emails are saved.", required=False)
parser.add_argument('-iF', '--ipFile', help="File name of where IPs are saved.", required=False)
parser.add_argument('-hunter', '--hunterio', help='Turns off hunter.io.', default=True, required=False, action='store_false')
parser.add_argument('-dns', '--dnsdumpster', help='Turns off dnsdumpster.com.', default=True, required=False, action='store_false')
parser.add_argument('-whois', '--whois', help='Turns off whois.arin.net.', default=True, required=False, action='store_false')
parser.add_argument('-mx', '--mxtoolbox', help='Turns off mxtoolbox.com.', default=True, required=False, action='store_false')
parser.add_argument('-he', '--hurricaneelectric', help='Turns off bgp.he.net.', default=True, required=False, action='store_false')
parser.add_argument('-s', '--setting', help='Loads a saved setting file.', required=False)
parser.add_argument('-nS', '--new-setting', help='Creates a new setting file.', required=False)
args = parser.parse_args()

name1 = args.setting
name2 = args.new_setting
dns_use = args.dnsdumpster
eF = args.emailFile
iF = args.ipFile
hunter_io = args.hunterio
whois_use = args.whois
mx_use = args.mxtoolbox
he_use = args.hurricaneelectric
customer_address = args.domain
customer = args.name

dns_list = []
open_tabs = 0

try:
    input = raw_input
except NameError:
    pass

if iF != None:
    if iF[-4:-1] == '.txt':
        ip = open(iF, 'w')
    elif iF[-4:-1] != '.txt':
        ip = open(iF + '.txt', 'w')
else:
    ip = open('ips.txt', 'w')

if eF != None:
    if eF[-4:-1] == '.txt':
        emails = open(eF, 'w')
    elif eF[-4:-1] != '.txt':
        emails = open(eF + '.txt', 'w')
else:
    emails = open('emails.txt', 'w')

gecko_location = ''
hunter_un = ''
hunter_pw = ''

cred_write = open('recon.config', 'a')

try:
    cred = open('recon.config', 'r').read().split('\n')
    for item in cred:
        item = item.split(' = ')
        if item[0] == ('Geckodriver Location'):
            gecko_location = item[1]
        elif item[0] == ('Hunter email'):
            hunter_un = item[1]
        elif item[0] == ('Hunter password'):
            hunter_pw = item[1]
except:
    print('Your recon.config folder is empty.  Please answer the following questions to fill it.')
    if hunter_io:
        hunter_un = input('What is your hunter.io email? ')
        hunter_pw = input('What is your hunter.io password? ')
        cred_write.write('Hunter email = ' + hunter_un + '\nHunter password = ' + hunter_pw + '\n')
    gecko_location = input('What is the location of geckodriver.exe? ')
    cred_write.write('Geckodriver Location = ' + gecko_location)
    cred_write.close()

if hunter_un == '':
    hunter_un = input('What is your hunter.io email? ')
    cred_write.write('\nHunter email = ' + hunter_un)
if hunter_pw == '':
    hunter_pw = input('What is your hunter.io password? ')
    cred_write.write('\nHunter password = ' + hunter_pw)
if gecko_location == '':
    gecko_location = input('What is the location of geckodriver.exe? ')
    if gecko_location == '':
        gecko_location = './geckodriver.exe'
    cred_write.write('\nGeckodriver Location = ' + gecko_location)

cred_write.close()

if name1 != None:
    path = '.\\'
    files = []
    for r, d, f in os.walk(path):
        for file in f:
            if '.txt' in file and 'set' in file:
                files.append(os.path.join(r, file))
    try:
        y = open(name1 + '.txt', 'r')
    except:
        y = open('set_' + name1 + '.txt', 'r')
    settings = y.read()
    settings = settings.split('\n')
    hunter_io = settings[0]
    dns_use = settings[1]
    whois_use = settings[2]
    mx_use = settings[3]
    he_use = settings[4]
    y.close()

if name2 != None:
    if name2[:3] == 'set_':
        y = open(name2 + '.txt', 'w')
    else:
        y = open('set_' + name2 + '.txt', 'w')
    y.write(str(hunter_io))
    y.write('\n' + str(dns_use))
    y.write('\n' + str(whois_use))
    y.write('\n' + str(mx_use))
    y.write('\n' + str(he_use))
    y.close()

driver = webdriver.Firefox(executable_path=gecko_location)

if dns_use == True:
    driver.get('https://dnsdumpster.com')
    driver.find_element_by_id('regularInput').send_keys(customer_address)
    driver.find_element_by_class_name('btn').click()
    ttimes = 0
    for item in driver.find_elements_by_class_name('col-md-3'):
        if ttimes % 2 == 0:
            text = item.text
            dns_list.append(text)
        ttimes += 1

    for item in dns_list:
        item1 = item.split('\n')
        ip.write(item1[0] + '\n')
    driver.execute_script('''window.open("https://www.google.com","_blank");''')
    open_tabs += 1


global times
global times1
global times2
global times3
global times4

times = 1
times1 = 1
times2 = 1
times3 = 1
times4 = 1


def whois_org():
    item_list = []
    main_div = driver.find_element_by_id('maincontent')
    for item1 in main_div.find_elements_by_tag_name('a'):
        item_list.append(item1.text)
    for item1 in item_list:
        driver.get('https://whois.arin.net/rest/customer/' + item1)
        tables = driver.find_elements_by_tag_name('table')
        try:
            item = tables[1].find_element_by_tag_name('a').text
            ip.write(item + '\n')
        except:
            pass


if whois_use or whois_use == 'True':
    driver.switch_to.window(driver.window_handles[open_tabs])

    def run_arin(second):
        driver.get('https://whois.arin.net/ui/advanced.jsp')
        driver.find_element_by_id('q').send_keys(customer_address)
        global times
        global times1
        global times2
        global times3
        global times4
        times = 1
        times1 = 1
        times2 = 1
        times3 = 1
        times4 = 1
        org = False
        for item in driver.find_elements_by_tag_name('input'):
            if times == 18 and not second:
                item.click()
                driver.find_element_by_id('submitQuery').click()
                org = True
            elif times == 21 and second:
                item.click()
                driver.find_element_by_id('submitQuery').click()
                whois_org()
                break
            if org:
                whois_org()
            times += 1


    run_arin(False)
    run_arin(True)
    driver.execute_script('''window.open("https://www.google.com","_blank");''')
    open_tabs += 1

if mx_use == True or mx_use == 'True':
    driver.switch_to.window(driver.window_handles[open_tabs])
    driver.get('https://mxtoolbox.com/')
    driver.find_element_by_id('ctl00_ContentPlaceHolder1_ucToolhandler_txtToolInput').send_keys(customer_address)
    driver.find_element_by_id('ctl00_ContentPlaceHolder1_ucToolhandler_btnAction').click()
    time.sleep(5)
    times = 0
    for item in driver.find_elements_by_class_name('table-column-IP_Address'):
        ip.write(item.find_element_by_tag_name('a').text + '\n')
        times += 1
    driver.execute_script('''window.open("https://www.google.com","_blank");''')
    open_tabs += 1

if he_use == True or he_use == 'True':
    driver.switch_to.window(driver.window_handles[open_tabs])
    driver.get('https://bgp.he.net/ip')
    driver.find_element_by_id('search_search').send_keys(customer_address)

    times = 0
    times1 = 0
    item_list = []
    time.sleep(2)
    for item in driver.find_elements_by_tag_name('input'):
        if times == 1:
            item.click()
            time.sleep(2)
            for item1 in driver.find_elements_by_class_name('dnsdata'):
                if times1 == 4:
                    for item2 in item1.find_elements_by_tag_name('a'):
                        item_list.append(item2.text)
                times1 += 1
            for item1 in item_list:
                driver.get('https://bgp.he.net/ip/' + str(item1))
                try:
                    ip.write('Net Block: ' + driver.find_element_by_class_name('nowrap').find_element_by_tag_name('a').text + '\n')
                except:
                    pass
        times += 1
    driver.execute_script('''window.open("https://www.google.com","_blank");''')
    open_tabs += 1

if hunter_io == True or hunter_io == 'True':
    driver.switch_to.window(driver.window_handles[open_tabs])
    driver.get('https://hunter.io/search')
    driver.find_element_by_id('email-field').send_keys(hunter_un)
    driver.find_element_by_id('password-field').send_keys(hunter_pw)
    time.sleep(1)
    driver.find_element_by_class_name('btn-orange').click()
    time.sleep(1)
    driver.find_element_by_id('domain-field').send_keys(customer_address)
    driver.find_element_by_id('search-btn').click()
    time.sleep(3)

    dp = driver.find_element_by_class_name('domain-pattern')
    pattern = dp.find_element_by_tag_name('strong').text

    while True:
        try:
            driver.find_element_by_class_name('show-more').click()
        except:
            break
        time.sleep(1)
    driver.execute_script('''window.open("https://www.google.com","_blank");''')
    open_tabs += 1
for item in driver.find_elements_by_class_name('email'):
    emails.write(item.text + '\n')
emails.close()

times = 1
times1 = 1
times2 = int(1)
times3 = 1
times4 = 1
names = len(customer)
global tt
tt = 0

while tt < len(customer):
    if whois_use == True or whois_use == 'True':
        driver.switch_to.window(driver.window_handles[open_tabs])


        def run_arin(second):
            driver.get('https://whois.arin.net/ui/advanced.jsp')
            driver.find_element_by_id('q').send_keys(customer[tt])
            global times
            global times1
            global times2
            global times3
            global times4
            times = 1
            times1 = 1
            times2 = 1
            times3 = 1
            times4 = 1
            times_pic = 0
            item_list = []
            for item in driver.find_elements_by_tag_name('input'):
                if times == 18 and not second:
                    item.click()
                    driver.find_element_by_id('submitQuery').click()
                    whois_org()
                elif times == 21 and second:
                    item.click()
                    driver.find_element_by_id('submitQuery').click()
                    whois_org()
                    break
                elif times == 21:
                    run_arin(True)
                    break
                times += 1


        run_arin(False)
    tt += 1
    driver.execute_script('''window.open("https://www.google.com","_blank");''')
    open_tabs += 1

tt = 0
while tt < len(customer):
    if he_use == True or he_use == 'True':
        driver.switch_to.window(driver.window_handles[open_tabs])
        driver.get('https://bgp.he.net/ip')
        driver.find_element_by_id('search_search').send_keys(customer[tt])

        times = 0
        times1 = 0
        item_list = []
        time.sleep(2)
        for item in driver.find_elements_by_tag_name('input'):
            if times == 1:
                item.click()
                time.sleep(2)
                for item1 in driver.find_elements_by_class_name('dnsdata'):
                    if times1 == 4:
                        for item2 in item1.find_elements_by_tag_name('a'):
                            item_list.append(item2.text)
                    times1 += 1
                for item1 in item_list:
                    driver.get('https://bgp.he.net/ip/' + str(item1))
                    ip.write('Net Block: ' + driver.find_element_by_class_name('nowrap').find_element_by_tag_name('a').text + '\n')
            times += 1
    tt += 1
    driver.execute_script('''window.open("https://www.google.com","_blank");''')
    open_tabs += 1

ip.close()

