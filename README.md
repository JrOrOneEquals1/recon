# About this tool
This tool uses Python Selenium to parse through certain sites and retrieve IP addresses and emails.

## Information
You need to have Google Chrome installed.  Your usernames and passwords are secure, and used only for logging in to the sites used by the tool when you request it.  Information found gets saved in files named 'emails.txt' and 'ips.txt', unless otherwise specified.

# Installation and usage
To install and use this tool, you need to have chromedriver.exe for your Chrome version from [here](https://chromedriver.chromium.org/downloads).  To get Selenium and Urllib3 after cloning, run this command: ```pip install -r requirements.txt```.  Example tool usage: ```recon.py -d company.com -n "company name 1" "company name 2"```.

## Entering credentials
You must have an actual hunter.io login/password.  There is an option on the hunter.io to sign in with google, but you need to have a password and email with it.  If you usually sign in with google, go to your account information and hit set password, then go to your email and folllow the instructions.  If you do not have a recon.config file, or if it is empty, the tool will ask you for the information that needs to go inside.

## Changing default sites
To change the what sites are on or off by default, use the command -cd [[site] [site] ...].  The site you put in is the word after the - command for the site, not the -- command.  It will not change the default until after it runs with the command.  For example, if Hunter default is on and you don't want to use, and you use -cd hunter, you will also need to use -hunter to turn it off.  This will be changing in a future commit.

## Setting files
The only argument for saving and getting setting files is the filename.  It will save whatever you have set the current sites to be.  For example, if you have the command ```recon.py -d company.com -n "Company Name" -hunter -s NoHunter```, the setting file will be to run everything except Hunter, unless you have changed the defaults (it will then save whatever the default values are).
