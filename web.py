from flask import Flask, render_template, flash, request, url_for, redirect  # , session
import socket
import time

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# host = '192.168.86.26'
host = '192.168.1.10'
port = 12345

HEADER_LENGTH = 10
window_id = "op"
not_online = True

while not_online:
    try:
        client_socket.connect((host, port))
        client_socket.setblocking(False)

        username = window_id.encode('utf-8')
        username_header = '{:10}'.format(len(username)).encode('utf-8')
        client_socket.send(username_header + username)
        print("connected")
        not_online = False
    except Exception as e:
        print(e)
        time.sleep(5)


def robot(data):

    message = data.encode('utf-8')
    message_header = '{:10}'.format(len(message)).encode('utf-8')
    client_socket.send(message_header + message)


app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def index():
    error = ''
    try:

        if request.method == "POST":

            attempted_username = request.form['username']
            attempted_password = request.form['password']

            # flash(attempted_username)
            # flash(attempted_password)

            if attempted_username == "don" and attempted_password == "dogs":
                return redirect(url_for('dashboard'))

            else:
                error = "Invalid credentials. Try Again."

        return render_template("index.html", error=error)

    except Exception as exp:
        flash(exp)
        return render_template("index.html", error=error)


@app.route('/dashboard/')
def dashboard():
    flash('Window 1 needs help!')
    return render_template("dashboard.html")


if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    app.run(host="0.0.0.0", port=80, debug=True)
