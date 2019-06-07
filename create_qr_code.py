#https://pypi.org/project/qrcode/
#pip install qrcode[pil]

import qrcode
img = qrcode.make('Some data here')
img.save("image.jpg")



#
import pyotp
hotp = pyotp.HOTP('base32secret3232')
temp = hotp.at(1401) # => '316439'
img = qrcode.make(temp)
img.save("image.jpg")
