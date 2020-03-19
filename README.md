# About this tool
This tool uses Python Selenium to parse through certain sites and retrieve IP addresses and emails.

## Information
You need to have Mozilla Firefox installed.  Your usernames and passwords are secure, and used only for logging in to the sites used by the tool when you request it.  Information found gets saved in changeable filenames 'emails.txt' and 'ips.txt'.

# Installation and usage
To install and use this tool, you need to have geckodriver.exe from [here](https://github.com/mozilla/geckodriver/releases).  To get Slenium and Urllib3 after cloning, run this command: ```pip install -r requirements.txt```.  Example tool usage: ```recon.py -d company.com -n "company name" "company name 2"```.

## Entering credentials
If you do not have a hunter.io login, adding the ```-hunter``` option will disable it.  There is an option on hunter.io to sign in with google, but you need to have a password and email with it.  If you usually sign in with google, go to your account information and hit set password, then go to your email and folllow the instructions.  If recon.config is empty or missing, the tool will ask you for the information that will go inside.  To change your credentials, add the ```-creds``` or ```--credentials``` to the run command.
