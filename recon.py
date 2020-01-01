second:
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
