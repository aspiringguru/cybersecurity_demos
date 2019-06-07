#https://pyotp.readthedocs.io/en/latest/
# cd D:\2018_working\coding\googleAuthenticator
#https://tools.ietf.org/html/rfc4226

import pyotp
import time
totp = pyotp.TOTP('base32secret3232')
temp = totp.now()
temp

# OTP verified for current time
totp.verify(temp) # => True
time.sleep(30)
totp.verify(temp) # => False


#as above but with loop to identify time to fail
temp = totp.now()
temp
totp.verify(temp) # => True
tracker = 0
while True:
    if totp.verify(temp):
        tracker += 1
        print("tracker:", tracker)
        time.sleep(1)
    else:
        print("totp.verify(temp) returned false")
        break

print("tracker:", tracker)


#counter based one time passwords

hotp = pyotp.HOTP('base32secret3232')
hotp.at(0) # => '260182'
hotp.at(1) # => '055283'
temp = hotp.at(1401) # => '316439'
temp

# OTP verified with a counter
hotp.verify(temp, 1401) # => True
hotp.verify(temp, 1402) # => False


#https://pypi.org/project/pyotp/
pyotp.totp.TOTP('JBSWY3DPEHPK3PXP').provisioning_uri("sleepyhollowinoz@gmail.com", issuer_name="Secure App")
temp = pyotp.hotp.HOTP('JBSWY3DPEHPK3PXP').provisioning_uri("sleepyhollowinoz@gmail.com", initial_count=0, issuer_name="bmtTest")


import qrcode
import pyotp
mykey = 'JBSWY3DPEHPK3PXP'
temp = pyotp.hotp.HOTP(mykey).provisioning_uri("sleepyhollowinoz@gmail.com", issuer_name="bmtTest")
img = qrcode.make(temp)
img.save("image.jpg")

totp = pyotp.TOTP(mykey)
print("Current OTP:", totp.now())

#https://github.com/neocotic/qrious

import datetime
datetime.datetime.now()

import numpy as np
str(np.datetime64('now'))
str(np.datetime64('today'))

import pandas as pd
str(pd.to_datetime('now'))
str(pd.to_datetime('today'))  #returns local timezone time

from time import gmtime, strftime
print(strftime("%z", gmtime()))

import time
time.tzname

import datetime
tz_string = datetime.datetime.now(datetime.timezone.utc).astimezone().tzname()
tz_string

time.timezone / -(60*60)
