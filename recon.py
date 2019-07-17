from selenium import webdriver
import os, argparse, time


y = open('set_default.txt', 'r')
settings = y.read()
settings = settings.split('\n')
hunter_io = bool(settings[0])
dns_use = bool(settings[1])
whois_use = bool(settings[2])
mx_use = bool(settings[3])
he_use = bool(settings[4])
leak_get = bool(settings[5])
y.close()
t = 0
for item in settings:
    if item == True:
        settings[t] = False
    elif item == False:
        settings[t] = True
    settings[t] = str(settings[t]).lower()
    t += 1


parser = argparse.ArgumentParser(description='This tool uses Python Selenium to parse through certain sites and retrieve IP addresses, emails, and leaks. It was developed by Cameron Roberts, age 16.')
parser.add_argument('-u', '--hunter', help='Turns off hunter.io.', default=True, required=False, action='store_false')
parser.add_argument('-d', '--dns', help='Turns off dnsdumpster.com.', default=True, required=False, action='store_false')
parser.add_argument('-w', '--whois', help='Turns off whois.arin.net.', default=True, required=False, action='store_false')
parser.add_argument('-m', '--mx', help='Turns off mxtoolbox.com.', default=True, required=False, action='store_false')
parser.add_argument('-e', '--he', help='Turns off bgp.he.net.', default=True, required=False, action='store_false')
parser.add_argument('-l', '--leaks', help='Turns off poppingboxes.org.', default=True, required=False, action='store_false')
parser.add_argument('-s', '--setting', help='Loads a saved setting file.  ("Set_" in the settings name is not necessary)', required=False)
parser.add_argument('-n', '--new-setting', help='Creates a new setting file.  ("Set_" in settings name is not necessary)', required=False)
parser.add_argument('-a', '--address', help="Customer's web domain.", required=True)
parser.add_argument('-c', '--customer', help="All of the customer's names.", required=True, nargs='*')
args = parser.parse_args()

name1 = args.setting
name2 = args.new_setting
dns_use = args.dns
hunter_io = args.hunter
whois_use = args.whois
mx_use = args.mx
he_use = args.he
leak_get = args.leaks
customer_address = args.address
customer = args.customer

dns_list = []
x = 0

cred = open('recon.config', 'r')
cred = cred.read()
cred = cred.split('\n')
hunter_un = cred[0]
hunter_pw = cred[1]
pbun = cred[2]
pbpw = cred[3]


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
    leak_get = settings[5]
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
    y.write('\n' + str(leak_get))
    y.close()


global out_string
out_string = ''
driver = webdriver.Firefox(executable_path='./geckodriver.exe')
if dns_use == True or dns_use == 'True':
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
        out_string += item1[0] + '\n'
    driver.execute_script('''window.open("https://www.google.com","_blank");''')
    x += 1

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

if whois_use == True or whois_use == 'True':
    driver.switch_to.window(driver.window_handles[x])
    
    
    def run_arin(second):
        driver.get('https://whois.arin.net/ui/advanced.jsp')
        driver.find_element_by_id('q').send_keys(customer_address)
        global times
        global times1
        global times2
        global times3
        global times4
        global out_string
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
                main_div = driver.find_element_by_id('maincontent')
                for item1 in main_div.find_elements_by_tag_name('a'):
                    item_list.append(item1.text)
                for item1 in item_list:
                    driver.get('https://whois.arin.net/rest/customer/' + item1)
                    main_content = driver.find_element_by_id('maincontent')
                    for item2 in main_content.find_elements_by_tag_name('td'):
                        if times3 == 23:
                            for item3 in item2.find_elements_by_tag_name('td'):
                                if times4 == 2:
                                    item1 = item3.text.split(' - ')
                                    if len(item1) > 1:
                                        item2_1 = item1[0]
                                        item2_2 = item1[1]
                                        item3 = item2_1.split('.')
                                        item4 = item2_2.split('.')
                                        min1 = int(item3[3])
                                        max1 = int(item4[3])
                                        default = item3[0] + '.' + item3[1] + '.' + item3[2] + '.'
                                        while min1 <= max1:
                                            out_string += default + str(min1) + '\n'
                                            min1 += 1
                                    else:
                                        out_string += item + '\n'
                                times4 += 1
                        times3 += 1
                    times_pic += 1
            elif times == 21 and second:
                item.click()
                driver.find_element_by_id('submitQuery').click()
                main_div = driver.find_element_by_id('maincontent')
                for item1 in main_div.find_elements_by_tag_name('a'):
                    item_list.append(item1.text)
                for item1 in item_list:
                    times1 = 1
                    times2 = 1
                    driver.get('https://whois.arin.net/rest/customer/' + item1)
                    main_content = driver.find_element_by_id('maincontent')
                    for item2 in main_content.find_elements_by_tag_name('td'):
                        if times1 == 23:
                            for item3 in item2.find_elements_by_tag_name('td'):
                                if times2 == 2:
                                    item1 = item3.text.split(' - ')
                                    if len(item1) > 1:
                                        item2_1 = item1[0]
                                        item2_2 = item1[1]
                                        item3 = item2_1.split('.')
                                        item4 = item2_2.split('.')
                                        min1 = int(item3[3])
                                        max1 = int(item4[3])
                                        default = item3[0] + '.' + item3[1] + '.' + item3[2] + '.'
                                        while min1 <= max1:
                                            out_string += default + str(min1) + '\n'
                                            min1 += 1
                                    else:
                                        out_string += item + '\n'
                                times2 += 1
                        times1 += 1
                    times_pic += 1
                break
            elif times == 21:
                run_arin(True)
                break
            times += 1
    
    
    run_arin(False)
    driver.execute_script('''window.open("https://www.google.com","_blank");''')
    x += 1


if mx_use == True or mx_use == 'True':
    driver.switch_to.window(driver.window_handles[x])
    driver.get('https://mxtoolbox.com/')
    driver.find_element_by_id('ctl00_ContentPlaceHolder1_ucToolhandler_txtToolInput').send_keys(customer_address)
    driver.find_element_by_id('ctl00_ContentPlaceHolder1_ucToolhandler_btnAction').click()
    time.sleep(5)
    times = 0
    for item in driver.find_elements_by_class_name('table-column-IP_Address'):
        out_string += item.find_element_by_tag_name('a').text + '\n'
        times += 1
    driver.execute_script('''window.open("https://www.google.com","_blank");''')
    x += 1

if he_use == True or he_use == 'True':
    driver.switch_to.window(driver.window_handles[x])
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
                    out_string += 'Net Block: ' + driver.find_element_by_class_name('nowrap').find_element_by_tag_name('a').text + '\n'
                except:
                    pass
        times += 1
    driver.execute_script('''window.open("https://www.google.com","_blank");''')
    x += 1

if hunter_io == True or hunter_io == 'True':
    driver.switch_to.window(driver.window_handles[x])
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
    x += 1

email = open('emails.txt', 'w')
for item in driver.find_elements_by_class_name('email'):
    email.write(item.text + '\n')
email.close()




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
        driver.switch_to.window(driver.window_handles[x])


        def run_arin(second):
            driver.get('https://whois.arin.net/ui/advanced.jsp')
            driver.find_element_by_id('q').send_keys(customer[tt])
            global times
            global times1
            global times2
            global times3
            global times4
            global out_string
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
                    main_div = driver.find_element_by_id('maincontent')
                    for item1 in main_div.find_elements_by_tag_name('a'):
                        item_list.append(item1.text)
                    for item1 in item_list:
                        driver.get('https://whois.arin.net/rest/customer/' + item1)
                        main_content = driver.find_element_by_id('maincontent')
                        for item2 in main_content.find_elements_by_tag_name('td'):
                            if times3 == 23:
                                for item3 in item2.find_elements_by_tag_name('td'):
                                    if times4 == 2:
                                        item1 = item3.text.split(' - ')
                                        if len(item1) > 1:
                                            item2_1 = item1[0]
                                            item2_2 = item1[1]
                                            item3 = item2_1.split('.')
                                            item4 = item2_2.split('.')
                                            min1 = int(item3[3])
                                            max1 = int(item4[3])
                                            default = item3[0] + '.' + item3[1] + '.' + item3[2] + '.'
                                            while min1 <= max1:
                                                out_string += default + str(min1) + '\n'
                                                min1 += 1
                                        else:
                                            out_string += item + '\n'
                                    times4 += 1
                            times3 += 1
                        times_pic += 1
                elif times == 21 and second:
                    item.click()
                    driver.find_element_by_id('submitQuery').click()
                    main_div = driver.find_element_by_id('maincontent')
                    for item1 in main_div.find_elements_by_tag_name('a'):
                        item_list.append(item1.text)
                    for item1 in item_list:
                        times1 = 1
                        times2 = 1
                        driver.get('https://whois.arin.net/rest/customer/' + item1)
                        main_content = driver.find_element_by_id('maincontent')
                        for item2 in main_content.find_elements_by_tag_name('td'):
                            if times1 == 23:
                                for item3 in item2.find_elements_by_tag_name('td'):
                                    if times2 == 2:
                                        item1 = item3.text.split(' - ')
                                        if len(item1) > 1:
                                            item2_1 = item1[0]
                                            item2_2 = item1[1]
                                            item3 = item2_1.split('.')
                                            item4 = item2_2.split('.')
                                            min1 = int(item3[3])
                                            max1 = int(item4[3])
                                            default = item3[0] + '.' + item3[1] + '.' + item3[2] + '.'
                                            while min1 <= max1:
                                                out_string += default + str(min1) + '\n'
                                                min1 += 1
                                        else:
                                            out_string += item + '\n'
                                    times2 += 1
                            times1 += 1
                        times_pic += 1
                    break
                elif times == 21:
                    run_arin(True)
                    break
                times += 1
        run_arin(False)
    tt += 1

tt = 0
while tt < len(customer):
    if he_use == True or he_use == 'True':
        driver.execute_script('''window.open("https://www.google.com","_blank");''')
        x = int(x)
        driver.switch_to.window(driver.window_handles[x])
        x += 1
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
                    out_string += 'Net Block: ' + driver.find_element_by_class_name('nowrap').find_element_by_tag_name(
                        'a').text + '\n'
            times += 1
    tt += 1

if leak_get == True or leak_get == 'True':
    driver.execute_script('''window.open("https://www.google.com","_blank");''')
    x = int(x)
    driver.switch_to.window(driver.window_handles[x])
    x += 1
    driver.get('https://poppingboxes.org/')
    driver.find_element_by_class_name('nav-link').click()
    time.sleep(2)
    driver.find_element_by_id('id_login').send_keys(pbun)
    driver.find_element_by_id('id_password').send_keys(pbpw)
    driver.find_element_by_class_name('primaryAction').click()
    time.sleep(2)
    driver.find_element_by_class_name('nav-link').click()
    driver.find_element_by_id('domain').send_keys(customer_address)
    driver.find_element_by_id('retrieve_leak').click()
    time.sleep(2)
    driver.find_element_by_class_name('buttons-csv').click()

ip = open('ips.txt', 'w')
out_list = out_string.split('\n')
for item in out_list:
    ip.write(item + '\n')
ip.close()
