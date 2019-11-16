# About this tool
This tool uses Python Selenium to parse through certain sites and retrieve IP addresses and emails.

## Information
You need to have Mozilla Firefox installed.  Your usernames and passwords are secure, and used only for logging in to the sites used by the tool when you request it.  Information found gets saved in files named 'emails.txt' and 'ips.txt'.

# Installation and usage
To install and use this tool, you need to have geckodriver.exe from [here](https://github.com/mozilla/geckodriver/releases).  To get Slenium and Urllib3 after cloning, run this command: ```pip install -r requirements.txt```.  To run the tool, use this command: ```recon.py -a company.com -c "company name" "company name 2"```.

## Entering credentials
You must have a poppingboxes.com account and an actual hunter.io login/password.  There is an option on the hunter.io to sign in with google, but you need to have a password and email with it.  If you usually sign in with google, go to your account information and hit set password, then go to your email and folllow the instructions.  In recon.config, put the necessary credentials in where it tells you to.  Make sure to keep lines 1-6 as credentials only, in the correct order.  Lines after 6 are avaialable for notes on what goes where.  If you do not have a recon.config file, or if it is empty, the tool will ask you for the information that nees to go inside.

## Changing default settings
To change the default settings, open the recon.py file in a text editor, and near the beggining it has lines that start with 'parser.add_argument'.  Change the 'default=True' to 'default=False'.  Near the end of the line it will say "action='store_false'", change it to "action='store_true'".
