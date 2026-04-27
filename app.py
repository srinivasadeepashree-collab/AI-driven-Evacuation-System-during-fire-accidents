import os
from flask import Flask
from twilio.rest import Client

app = Flask(__name__)

account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
client = Client(account_sid, auth_token)

@app.route('/')
def home():
    return "Server running. Use /send-alert"

@app.route('/send-alert', methods=['GET','POST'])
def send_alert():
    guest_numbers = os.environ.get("GUEST_NUMBERS","").split(",")
    staff_numbers = os.environ.get("STAFF_NUMBERS","").split(",")
    security_numbers = os.environ.get("SECURITY_NUMBERS","").split(",")

    def send(body, nums):
        for n in nums:
            n = n.strip()
            if n:
                client.messages.create(
                    body=body,
                    from_='whatsapp:+14155238886',
                    to=n
                )

    send("🚨 Fire detected. Evacuate safely.", guest_numbers)
    send("⚠️ Assist guests and guide evacuation.", staff_numbers)
    send("🚨 Block unsafe exits and manage evacuation.", security_numbers)

    return "Messages sent!"
    
if __name__ == '__main__':
    app.run(debug=True)