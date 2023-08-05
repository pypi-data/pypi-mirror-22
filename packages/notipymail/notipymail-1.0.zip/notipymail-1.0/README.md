<img src=https://github.com/nbryans/notipy/blob/master/Logo/notipyLogo.png width=300px align=left>
<!---# notipy-->
A module for quickly sending email status and alerts from python programs


This script was created to notify me when a job was completed (and sometimes include an exit status and relevant results)


Notipy is compatible with both python2 and python3

<br />

# Instructions

### Get Notipy

From PyPi
```
pip install notipymail
```
From Source
```
git clone https://github.com/nbryans/notipymail.git
python setup.py sdist
# Move dist\*.zip to desired location. Extract zip
cd Notipy-X.X
python setup.py install
```

### On First Run

In a `python` session
```python
import notipymail.notipy as notipy
notipy.updateSendDetails('yourEmail@emailProvider.com', 'yourPassword', 'smtp.emailProvider.com', '587')
```
This will create file  `senddetails.dat` containing the following contents:
```
email:email@emailProvider.com
password:yourPassword
server:smtp.emailProvider.com
port:587
```
Optionally, you can create this file manually.

### Sending Emails with Notipy:
```python
import notipymail.notipy as notipy
notipy.sendMail("to@address.com", "This is a message")
```

# Notes
Use `notipy.sendMailAsync(..)` to send mail in the background asynchronously.

Send status are logged in `notipy.log`. The log file can be changed in the `#Constants` section of `notipy.py`

To query the log through python, use `notipy.queryLog(5)` where `5` specifies the number of log entries (most recent to least) to retrieve. This operation may be slow for large logs.

In `sendMail` and `sendMailAsync`, there is an optional third parameter where you can specify a subject. *i.e.* `notipy.sendMail("to@address.com", "This is the message", "Custom Subject")`. The default subject is "Notipy Automail"


### Acknowledgements
Logo created using modified images originally distributed by Pixabay.com
https://pixabay.com/en/cartoon-snake-yellow-1293047/
https://pixabay.com/en/email-letter-contact-message-mail-309678/

