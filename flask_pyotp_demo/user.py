import pyotp
import pickle

USER_FILE_NAME = 'unix_users.data'


class User(object):
    def __init__(self, email, key=None):
        #nb: pyotp key needs to be in base32
        self.email = email
        self.key = key
        if key is None:
            self.key = pyotp.random_base32()

    def save(self):
        print("User.save(self), with self.email=", self.email)
        if len(self.email) < 1:
            print("len(self.email) < 1")
            return False
        users = pickle.load(open(USER_FILE_NAME, 'rb'))
        if self.email in users:
            print("email address already in users list")
            return False
        else:
            print("email address added to users list")
            users[self.email] = self.key
            pickle.dump(users, open(USER_FILE_NAME, 'wb'))
            return True

    def authenticate(self, otp):
        print("User.authenticate with otp=", otp)
        print("")
        p = 0
        try:
            p = int(otp)
        except:
            return False
        t = pyotp.TOTP(self.key)
        print("pyotp.TOTP(self.key)=", t)
        return t.verify(p)

    @classmethod
    def get_user(cls, email):
        users = pickle.load(open(USER_FILE_NAME, 'rb'))
        if email in users:
            return User(email, users[email])
        else:
            print("get_user(cls, email) did not find email=", email)
            return None

    #
    #https://stackoverflow.com/questions/136097/what-is-the-difference-between-staticmethod-and-classmethod
    #https://www.programiz.com/python-programming/methods/built-in/classmethod
