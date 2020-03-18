from flask import Flask, request, Response, render_template
from datetime import datetime
import urllib.request
import ssl
import os

app = Flask(__name__)

THIS_KEY = os.environ.get('RS_THIS_KEY', "TestKey")
THIS_NAME = os.environ.get('RS_THIS_NAME', 'Server 1')
THIS_SECRET = os.environ.get('RS_THIS_SECRET', "CSCBE{TestFlag}")
OTHER_LOCATION = os.environ.get('RS_OTHER_LOCATION', "localhost:4443")
OTHER_KEY = os.environ.get('RS_OTHER_KEY', "TestKey")
OTHER_NAME = os.environ.get('RS_OTHER_NAME', "Server 1")


def asText(text):
    return Response(text, mimetype='text/txt')


@app.errorhandler(AssertionError)
def handle_assert(error):
    response = asText(error.args)
    response.status_code = 400
    return response


last_secret_acccess = datetime.now()
datetime_format = "%Y-%m-%d %H:%M:%S.%f"


@app.route("/", defaults={'action': 'help'})
@app.route('/api', defaults={'action': 'help'})
@app.route("/api/<action>")
def api(action):
    global last_secret_acccess
    key = request.args.get('key', '')

    if action == 'help':
        return render_template('index.html', RS_SERVER=THIS_NAME)

    if action == 'get_time':
        return asText(datetime.now().strftime(datetime_format))

    if action == 'last_accessed_server':
        url = f"https://{OTHER_LOCATION}/api/last_access?key={OTHER_KEY}"
        context = ssl._create_unverified_context(protocol=ssl.PROTOCOL_TLSv1_2)
        # The default is ECDHE, which wireshark can't crack
        context.set_ciphers("RSA")
        with urllib.request.urlopen(url, context=context) as response:
            other_access = datetime.strptime(
                response.read().decode('utf-8'), datetime_format)
        return asText(OTHER_NAME if other_access > last_secret_acccess else THIS_NAME)

    if action == 'last_access':
        assert key == THIS_KEY, 'Invalid key'
        return asText(str(last_secret_acccess))

    if action == "get_secret":
        assert key == THIS_KEY, 'Invalid key'
        last_secret_acccess = datetime.now()
        return asText(THIS_SECRET)

    return asText("No valid action found.")


if __name__ == "__main__":
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.run(
        host="0.0.0.0",
        port=443,
        ssl_context=('key.cert.pem', 'key.private.pem')
    )
