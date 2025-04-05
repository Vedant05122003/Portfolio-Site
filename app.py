from flask import Flask, render_template, request, redirect, flash
import os
import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
app.secret_key = os.urandom(24)

# ✅ Replace with your actual info
EMAIL_ADDRESS = "vedantvpawar09@gmail.com"
EMAIL_PASSWORD = "mgwy lmyo iljl wzdg"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/contact', methods=['POST'])
def contact():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    if not name or not email or not message:
        flash("All fields are required!")
        return redirect('/')

    # ✅ Save to CSV
    try:
        with open('submissions.csv', 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([name, email, message])
    except Exception as e:
        print("❌ CSV Error:", e)
        flash("Error saving your message.")
        return redirect('/')

    # ✅ Send Email Notification
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = EMAIL_ADDRESS
        msg['Subject'] = f"📬 New Portfolio Message from {name}"

        body = f"""
        You received a new message via your portfolio site:

        Name: {name}
        Email: {email}
        Message:
        {message}
        """

        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()

        flash("Thanks for contacting me! I’ll get back to you soon.")
    except Exception as e:
        print("❌ Email Error:", e)
        flash("Form saved, but failed to send email.")

    return redirect('/')

if __name__ == '__main__':
    print("🔥 Flask app running with email + CSV")
    app.run(debug=True)
