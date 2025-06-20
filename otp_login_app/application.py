from flask import Flask, request, render_template, session, redirect, url_for
import boto3
import random
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# SNS client
sns_client = boto3.client(
    'sns',
    region_name='ap-south-1',  # Change region if needed
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        mobile = request.form['mobile']
        otp = str(random.randint(100000, 999999))

        session['otp'] = otp
        session['mobile'] = mobile
        session['name'] = name

        message = f"Your OTP is {otp}"
        sns_client.publish(
            PhoneNumber=f"+91{mobile}",
            Message=message
        )
        return redirect(url_for('verify'))

    return render_template('login.html')

@app.route('/verify', methods=['GET', 'POST'])
def verify():
    if request.method == 'POST':
        entered_otp = request.form['otp']
        if entered_otp == session.get('otp'):
            return f"Welcome {session.get('name')}! You are successfully logged in."
        return "Invalid OTP. Try again."

    return render_template('verify.html')
