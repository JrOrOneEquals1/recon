#!/usr/bin/env python

import os, argparse, time, sys
from selenium import webdriver
from importlib import import_module

parser = argparse.ArgumentParser(description='This tool uses Python Selenium to parse through certain sites and retrieve IP addresses, and emails.')
parser.add_argument('-d', '--domain', help="Customer's web domain.", required=True)
parser.add_argument('-n', '--name', help="All of the customer's names.  Can include search wildcards.", required=True, nargs='*')
parser.add_argument('-eF', '--emailFile', help="File name of where emails are saved.", required=False)
parser.add_argument('-iF', '--ipFile', help="File name of where IPs are saved.", required=False)
parser.add_argument('-hunter', '--hunterio', help='Turns off hunter.io.', default=True, required=False, action='store_false')
parser.add_argument('-dns', '--dnsdumpster', help='Turns off dnsdumpster.com.', default=True, required=False, action='store_false')
parser.add_argument('-whois', '--whois', help='Turns off whois.arin.net.', default=True, required=False, action='store_false')
parser.add_argument('-s', '--setting', help='Loads a saved setting file.', required=False)
parser.add_argument('-nS', '--new-setting', help='Creates a new setting file.', required=False)
parser.add_argument('--errors', help='Prints the errors that occur.', default=False, required=False, action='store_true')
args = parser.parse_args()

name1 = args.setting
name2 = args.new_setting
dns_use = args.dnsdumpster
eF = args.emailFile
iF = args.ipFile
hunter_io = args.hunterio
whois_use = args.whois
customer_address = args.domain
customer = args.name
showErrors = args.errors
hunter_args = args.hunterio_args

dns_list = []

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

chromedriver_location = ''
hunter_un = ''
hunter_pw = ''

cred_write = open('recon.config', 'a')

try:
    cred = open('recon.config', 'r').read().split('\n')
    for item in cred:
        item = item.split(' = ')
        if item[0] == ('Chromedriver Location'):
            chromedriver_location = item[1]
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
    chromedriver_location = input('What is the location of chromedriver.exe? ')
    cred_write.write('Chromedriver Location = ' + chromedriver_location)
    cred_write.close()

if hunter_un == '':
    hunter_un = input('What is your hunter.io email? ')
    cred_write.write('\nHunter email = ' + hunter_un)
if hunter_pw == '':
    hunter_pw = input('What is your hunter.io password? ')
    cred_write.write('\nHunter password = ' + hunter_pw)
if chromedriver_location == '':
    chromedriver_location = input('What is the location of chromedriver.exe? ')
    if chromedriver_location == '':
        chromedriver_location = './chromedriver.exe'
    cred_write.write('\nChromedriver Location = ' + chromedriver_location)

cred_write.close()

if name1 != None:
    path = '.\\'
    files = []
    for r, d, f in os.walk(path):
        for file in f:
            if '.txt' in file and 'setting' in file:
                files.append(os.path.join(r, file))
    try:
        y = open(name1 + '.txt', 'r')
    except:
        y = open('setting_' + name1 + '.txt', 'r')
    settings = y.read()
    settings = settings.split('\n')
    hunter_io = settings[0]
    dns_use = settings[1]
    whois_use = settings[2]
    y.close()

if name2 != None:
    if name2[:3] == 'setting_':
        y = open(name2 + '.txt', 'w')
    else:
        y = open('setting_' + name2 + '.txt', 'w')
    y.write(str(hunter_io))
    y.write('\n' + str(dns_use))
    y.write('\n' + str(whois_use))
    y.close()

try:
    driver = webdriver.Chrome(executable_path=chromedriver_location)
    driver.maximize_window()
    driver.get('https://google.com')
except:
    print("Couldn't open Chrome")

try:
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
except Exception as e:
    if showErrors:
        print(e)
    else:
        print('Sorry, there was an error with dnsdumpster.')

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
            driver.get("https://whois.arin.net/rest/net/" + item + ".html")
            time.sleep(0.5)
            ipAddress = driver.find_elements_by_tag_name("td")[3].text
            ip.write(ipAddress + '\n')
        except:
            pass

try:
    if whois_use or whois_use == 'True':
        if driver.current_url != "https://www.google.com/":
            driver.execute_script('window.open("https://google.com");')
            driver.switch_to.window(driver.window_handles[-1])
        def run_arin(second):
            driver.get('https://whois.arin.net/ui/advanced.jsp')
            driver.find_element_by_id('q').send_keys(customer_address)
            times = 1
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
except Exception as e:
    if showErrors:
        print(e)
    else:
        print('Sorry, there was an error with whois.arin.')

try:
    if hunter_io == True or hunter_io == 'True':
        if driver.current_url != "https://www.google.com/":
            driver.execute_script('window.open("https://google.com");')
            driver.switch_to.window(driver.window_handles[-1])
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
    for item in driver.find_elements_by_class_name('email'):
        emails.write(item.text + '\n')
    emails.close()
except Exception as e:
    if showErrors:
        print(e)
    else:
        print('Sorry, there was an error with hunter.')

names = len(customer)
tt = 0
try:
    while tt < len(customer):
        if driver.current_url != "https://www.google.com/":
            driver.execute_script('window.open("https://google.com");')
            driver.switch_to.window(driver.window_handles[-1])
        if whois_use == True or whois_use == 'True':
            def run_arin(second):
                driver.get('https://whois.arin.net/ui/advanced.jsp')
                driver.find_element_by_id('q').send_keys(customer[tt])
                times = 1
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
except Exception as e:
    if showErrors:
        print(e)
    else:
        print('Sorry, there was an error with whois.arin.')
ip.close()
print("Continue to close the browser session.")
os.system("pause")