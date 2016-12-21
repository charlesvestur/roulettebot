"""
This bot listens to port 5000 for incoming connections from Facebook. It takes
in any messages that the bot receives and echos it back.
"""
from flask import Flask, request
from pymessenger.bot import Bot

app = Flask(__name__)

ACCESS_TOKEN = "EAAFFjl3J7o8BABnMmOb7wGFxkdwZCCotLe8wZBqzGN8sgi8NXr4wiQFySrZBgIfvqtYZBx70q0KhEVQW8liQH1dq9Q5jwfMbGaTnVRWnTwX9mBrCIT81IEoRKXMCFEImMy5c7ZB4MSkydqjne7eZBAJ3b991KRwWGnyPFZBJvudLwZDZD"
VERIFY_TOKEN = "secret"
bot = Bot(ACCESS_TOKEN)


@app.route("/", methods=['GET', 'POST'])
def hello():
    if request.method == 'GET':
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        else:
            return 'Invalid verification token'

    if request.method == 'POST':
        output = request.get_json()
        for event in output['entry']:
            messaging = event['messaging']
            for x in messaging:
                if x.get('message'):
                    recipient_id = x['sender']['id']
                    if x['message'].get('text'):
                        message = x['message']['text']
                        bot.send_text_message(recipient_id, message)
                    if x['message'].get('attachment'):
                        bot.send_attachment_url(recipient_id, x['message']['attachment']['type'],
                                                x['message']['attachment']['payload']['url'])
                else:
                    pass
        return "Success"


if __name__ == "__main__":
    app.run(port=5000, debug=True)