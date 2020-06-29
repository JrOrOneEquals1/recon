#!/usr/bin/env python

import os, argparse, time, sys
from selenium import webdriver
from importlib import import_module

# Parser arguments
parser = argparse.ArgumentParser(description='This tool uses Python Selenium to parse through certain sites and retrieve IP addresses, and emails.')
parser.add_argument('-d', '--domain', help="Customer's web domain.", required=True)
parser.add_argument('-n', '--name', help="All of the customer's names.  Can include search wildcards.", required=True, nargs='*')
parser.add_argument('-eF', '--emailFile', help="File name of where emails are saved.", required=False)
parser.add_argument('-iF', '--ipFile', help="File name of where IPs are saved.", required=False)
parser.add_argument('-hunter', '--hunterio', help='Turns off hunter.io.', default=True, required=False, action='store_false')
parser.add_argument('-dns', '--dnsdumpster', help='Turns off dnsdumpster.com.', default=True, required=False, action='store_false')
parser.add_argument('-whois', '--whois', help='Turns off whois.arin.net.', default=True, required=False, action='store_false')
parser.add_argument('-whatcms', '--whatcms', help='Turns off whatcms.org.', default=True, required=False, action='store_false')
parser.add_argument('-s', '--setting', help='Loads a saved setting file.', required=False)
parser.add_argument('-nS', '--new-setting', help='Creates a new setting file.', required=False)
parser.add_argument('-cd', '--changeDefault', help='Changes the default value for the specified site.', required=False, nargs='*')
parser.add_argument('--errors', help='Prints the errors that occur.', default=False, required=False, action='store_true')
args = parser.parse_args()

# Set argument values to variables
name1 = args.setting
name2 = args.new_setting
dns_use = args.dnsdumpster
eF = args.emailFile
iF = args.ipFile
hunter_io = args.hunterio
whois_use = args.whois
whatcms = args.whatcms
customer_address = args.domain
customer = args.name
showErrors = args.errors
cd = args.changeDefault

dns_list = []

try: # Python2 compatibility
    input = raw_input
except NameError:
    pass

if iF != None:
    if iF.endswith('.txt'): # This prevents files from being named 'example.txt.txt'
        ip = open(iF, 'w')
    else:
        ip = open(iF + '.txt', 'w')
else:
    ip = open('ips.txt', 'w')

if eF != None:
    if eF.endswith('.txt'):# This prevents files from being named 'example.txt.txt'
        emails = open(eF, 'w')
    else:
        emails = open(eF + '.txt', 'w')
else:
    emails = open('emails.txt', 'w')

chromedriver_location = ''
hunter_un = ''
hunter_pw = ''
cred = ''
cred_write = open('recon.config', 'a')

try:
    cred = open('recon.config', 'r').read().split('\n')
    config = True
except:
    config = False

if config: # If config folder exists
    for item in cred:
        item = item.split(' = ')
        if item[0] == ('Chromedriver Location'):
            chromedriver_location = item[1]
        elif item[0] == ('Hunter email'):
            hunter_un = item[1]
        elif item[0] == ('Hunter password'):
            hunter_pw = item[1]
else: # If config folder does not exist
    print('Your recon.config folder is empty.  Please answer the following questions to fill it.')
    if hunter_io:
        hunter_un = input('What is your hunter.io email? ')
        hunter_pw = input('What is your hunter.io password? ')
        cred_write.write('Hunter email = ' + hunter_un + '\nHunter password = ' + hunter_pw + "\n")
    chromedriver_location = input('What is the location of chromedriver.exe? ')
    cred_write.write('Chromedriver Location = ' + chromedriver_location)

if hunter_un == '' and hunter_io: # These all ask for information if it is blank and needed
    hunter_un = input('What is your hunter.io email? ')
    if len(cred) > 0:
        cred_write.write("\n")
    cred_write.write('Hunter email = ' + hunter_un)
if hunter_pw == '' and hunter_io:
    hunter_pw = input('What is your hunter.io password? ')
    if len(cred) > 0:
        cred_write.write("\n")
    cred_write.write('Hunter password = ' + hunter_pw)
if chromedriver_location == '': # If input is nothing, location is ./chromedriver.exe
    chromedriver_location = './chromedriver.exe'
    if len(cred) > 0:
        cred_write.write("\n")
    cred_write.write('Chromedriver Location = ' + chromedriver_location)

cred_write.close()

if name1 != None: # Loads a pre-existing setting file
    loadFile = open('setting_' + name1 + '.txt', 'r')
    settings = loadFile.read()
    settings = settings.split('\n')
    hunter_io = settings[0]
    dns_use = settings[1]
    whois_use = settings[2]
    whatcms = settings[3]
    loadFile.close()

if name2 != None: # Saves a new setting file
    try:
        skip = False
        existing = open('setting_' + name2 + '.txt', 'r').read() # If the file does not exist, this raises an error that is caught
        override = input("That file already exists.  Do you want to overwrite it? [y/n] ")
        if override == 'n':
            skip = True
    except:
        pass
    if not skip:
        saveFile = open('setting_' + name2 + '.txt', 'w')
        saveFile.write(str(hunter_io))
        saveFile.write('\n' + str(dns_use))
        saveFile.write('\n' + str(whois_use))
        saveFile.write('\n' + str(whatcms))
        saveFile.close()

try: # Opens the chrome session
    go = True
    driver = webdriver.Chrome(executable_path=chromedriver_location)
    driver.maximize_window()
    driver.get('https://google.com')
except Exception as e:
    if showErrors:
        print(e)
    else:
        print('Sorry, Chrome did not open.')

try:
    if dns_use and go:
        driver.get('https://dnsdumpster.com')
        driver.find_element_by_id('regularInput').send_keys(customer_address)
        driver.find_element_by_class_name('btn').click()
        ttimes = 0
        dns_list = []
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
            ip.write(driver.find_elements_by_tag_name("td")[3].text + '\n')
        except:
            pass

def run_arin(inputValue):
    newTab()
    driver.get('https://whois.arin.net/ui/advanced.jsp')
    driver.find_element_by_id('q').send_keys(inputValue)
    driver.find_element_by_xpath("//input[@value='ORGANIZATION']").click()
    driver.find_element_by_id('submitQuery').click()
    whois_org()
    driver.get('https://whois.arin.net/ui/advanced.jsp')
    driver.find_element_by_id('q').send_keys(inputValue)
    driver.find_element_by_xpath("//input[@value='CUSTOMER']").click()
    driver.find_element_by_id('submitQuery').click()
    whois_org()

def newTab():
    if driver.current_url != "https://www.google.com/":
        driver.execute_script('window.open("https://google.com");')
        driver.switch_to.window(driver.window_handles[-1])

try:
    if whois_use and go:
        run_arin(customer_address) # Search whois.arin with customer domain

        t = 0
        for name in customer: # Search whois.arin with customer names
            run_arin(name)
            t += 1
except Exception as e:
    if showErrors:
        print(e)
    else:
        print('Sorry, there was an error with whois.arin.')

try:
    if hunter_io and go:
        newTab()
        driver.get('https://hunter.io/search')
        driver.find_element_by_id('email-field').send_keys(hunter_un)
        driver.find_element_by_id('password-field').send_keys(hunter_pw)
        time.sleep(1)
        driver.find_element_by_class_name('btn-orange').click()
        time.sleep(1)
        driver.find_element_by_id('domain-field').send_keys(customer_address)
        driver.find_element_by_id('search-btn').click()
        time.sleep(3)
        pattern = driver.find_element_by_class_name('domain-pattern').find_element_by_tag_name('strong').text
        while True:
            try:
                driver.find_element_by_class_name('show-more').click()
            except:
                break
            time.sleep(1)
        emails.write(pattern + "\n")
        for item in driver.find_elements_by_class_name('email'):
            emails.write(item.text + '\n')
    emails.close()
except Exception as e:
    if showErrors:
        print(e)
    else:
        print('Sorry, there was an error with hunter.')
        
try:
    if whatcms and go:
        newTab()
        driver.get('https://whatcms.org/')
        driver.find_element_by_id('what-cms-size').send_keys(customer_address)
        driver.find_element_by_class_name('btn-success').click()
except Exception as e:
    if showErrors:
        print(e)
    else:
        print('Sorry, there was an error with whatcms.')

ip.close()

if cd != None:
    for var in cd:
        changeDefault = import_module('changeDefault', package='main')
        changeDefault.main.main("self", var)

print("Continue to close the browser session.")
os.system("pause")
