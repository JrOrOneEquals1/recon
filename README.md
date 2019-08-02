# About this tool
This tool uses Python Selenium to parse through certain sites and retrieve IP addresses, emails, and leaks.

## Information
You need to have Mozilla Firefox installed.  Your usernames and passwords are used only for logging in to the sites that you request to get the information that you request, only when you request it.  Information found gets saved in files named 'emails.txt' and 'ips.txt'.  The leaks are always found last.  Once it finishes, you will need to hit 'Yes' to download the file.  They will get saved in a file called 'Search Leaks.csv'.

# Installation and usage
To install and use this tool, download recon.py, recon.config, and geckodriver.exe from [here](https://github.com/mozilla/geckodriver/releases) and make sure that they are always in the same folder, or it will not work.  To run the tool, open the command prompt, cd to the folder with recon.py in it, and then type 'python recon.py' and then any additional - usages.  If you get an error saying 'unknown command: python', go [here](https://geek-university.com/python/add-python-to-the-windows-path/).

## Entering credentials
You must have a poppingboxes.com account and an actual hunter.io login/password.  There is an option on the site to sign in with google, but you need to have a password and email with it.  If you usually sign in with google, go to your account information and hit set password, then go to your email and folllow the instructions.  In recon.config, put the necessary credentials in where it tells you to, and put only the credentials in.

## Changing default settings
To change the default settings, open the recon.py file in a text editor, and near the beggining it has lines that start with 'parser.add_argument'.  Change the 'default=True' to 'default=False', and then near the end of the line it will say "action='store_false'", change it to "action='store_true'".
