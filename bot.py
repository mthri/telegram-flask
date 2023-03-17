import time

from flask import Flask, request
import telegram
from decouple import config


TOKEN = 'TOKEN' # telegram bot token
HOST = 'HOST' # same FQDN used when generating SSL Cert
CERT = '/home/telegram-flask/server.crt'
CERT_KEY = '/home/telegram-flask/server.key'
PORT = 8443 # allowed port 80, 88, 443 or 8443


app = Flask(__name__)
bot = telegram.Bot(token=TOKEN)
context = (CERT, CERT_KEY)


@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
    try:
        # implement your logic here, for example repeat bot:
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        chat_id = update.message.chat.id
        msg_id = update.message.message_id
        text = update.message.text.encode('utf-8').decode()
        bot.send_message(chat_id=chat_id, text=text, reply_to_message_id=msg_id)
    except:
        pass

    return 'ok'

def set_webhook():
    success: bool = bot.set_webhook(f'https://{HOST}:{PORT}/{TOKEN}',
                                    certificate=open(CERT, 'rb'),
                                    timeout=10)
    if success:
        return 'successfully webhook set'
    else:
        return "webhook failed"


# run once, for set webhook and check is working or not
if __name__ == '__main__':
    set_webhook()
    time.sleep(5)
    app.run(host='0.0.0.0', port=PORT, 
            ssl_context=context, debug=True)