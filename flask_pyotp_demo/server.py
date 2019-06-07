import qrcode
import logging
import pyotp
import os
#from StringIO import StringIO #python 2x
from io import StringIO #python 3x
from io import BytesIO
from flask import Flask, render_template, redirect, request, flash, send_file, make_response

from user import User

app = Flask(__name__)

#to set environment variables in windows 10
#setx FLASK_SESSION_SECRET_KEY "%USERPROFILE%123456"
#setx FLASK_SESSION_SECRET_KEY "123456"
#nb: exit cmd and check value in new cmd session
#echo %FLASK_SESSION_SECRET_KEY%
print("FLASK_SESSION_SECRET_KEY = ", os.environ['FLASK_SESSION_SECRET_KEY'])
app.config.update(SECRET_KEY=os.environ['FLASK_SESSION_SECRET_KEY'])
app.config.update(DEBUG=True)

@app.route('/qr_ssd/<email>')
def qr_ssd(email):
    """
    Return a QR code for the secret key associated with the given email
    address. The QR code is returned as file with MIME type image/png.
    """
    print("route=/qr_ssd/<email> : email:", email)
    u = User.get_user(email)
    if u is None:
        print("user not found, returning ''")
        return ''
    else:
        print("u is not None.")
    t = pyotp.TOTP(u.key)
    print("type(t):", type(t))
    q = qrcode.make(t.provisioning_uri(email))
    print("type(q):", type(q))
    img = StringIO()
    q.save(img)
    img.seek(0)
    return send_file(img, mimetype="image/png")

@app.route('/qr/<email>')
def qr(email):
    """
    Return a QR code for the secret key associated with the given email
    address. The QR code is returned as file with MIME type image/png.
    """
    print("route=/qr/<email> : email:", email)
    u = User.get_user(email)
    if u is None:
        print("user not found, returning ''")
        return ''
    else:
        print("u is not None.")
    t = pyotp.TOTP(u.key)
    print("type(t):", type(t))
    tt = t.provisioning_uri(email)
    print("type(tt):", type(tt))
    q = qrcode.make(tt)
    print("type(q):", type(q))
    img = BytesIO() #StringIO()
    print("type(img):", type(img))
    q.save(img, 'PNG')
    print("------")
    #return img.getvalue()
    response=make_response(img.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response


@app.route('/code/<email>')
def code(email):
    """
    Returns the one-time password associated with the given user for the
    current time window. Returns empty string if user is not found.
    """
    print("route=/code/<email> : email:", email)
    u = User.get_user(email)
    if u is None:
        print("user not found, returning ''")
        return ''
    t = pyotp.TOTP(u.key)
    result = str(t.now())
    print("result:", result)
    return result

@app.route('/user/<email>')
def user(email):
    """User view page."""
    print("route=/user/<email> : email:", email)
    u = User.get_user(email)
    if u is None:
        print("user not found, redirecting to /")
        return redirect('/')
    print("user found, returning view template for user=", u)
    return render_template('/view.html', user=u)


@app.route('/new', methods=['GET', 'POST'])
def new():
    """New user form."""
    print("route=/new")
    if request.method == 'POST':
        print("route=/new + request.method is POST")
        u = User(request.form['email'])
        print("email retrieved from form = ", u)
        if u.save():
            print("user created.")
            return render_template('/created.html', user=u)
        else:
            print("did not create user.")
            flash('Invalid email or user already exists.', 'danger')
            return render_template('new.html')
    else:
        print("route=/new + request.method is GET")
        return render_template('new.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login form."""
    print("route=/login")
    if request.method == 'POST':
        print("route=/login + request.method is POST")
        u = User.get_user(request.form['email'])
        print("email retrieved from form = ", u)
        if u is None:
            print("email is none")
            flash('Invalid email address.', 'danger')
            return render_template('login.html')
        else:
            otp = request.form['otp']
            print("otp from form = ", otp)
            if u.authenticate(otp):
                print("user authenticated")
                flash('Authentication successful!', 'success')
                return render_template('/view.html', user=u)
            else:
                print("error authenticating user.")
                flash('Invalid one-time password!', 'danger')
                return render_template('login.html')
    else:
        print("route=/login + request.method is GET")
        return render_template('login.html')


@app.route('/')
def hello():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
