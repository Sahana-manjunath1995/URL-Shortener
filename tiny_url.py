from flask import Flask, request, redirect
import string
from math import floor
import pymysql


conn = pymysql.connect(
        host='localhost',
        user='root',
        password = "root",
        db='url',
        )

cur = conn.cursor()
host = 'http://127.0.0.1:81'


def toBase62(num, b = 62):

    if b <= 0 or b > 62:
        return 0
    base = string.digits + string.ascii_lowercase + string.ascii_uppercase
    remainder= num % b
    res = base[remainder]
    q = floor(num / b)
    while q:
        rem = q % b
        q = floor(q / b)
        res = base[int(rem)] + res
    return res


app = Flask(__name__)


@app.route('/url_address', methods=['GET'])
def get_long_url():
    url_address = request.args.get('big_url')
    cur.execute(f"Insert into web_url_two (long_url) values ('{url_address}')")
    conn.commit()
    res = cur.lastrowid
    encoded_string = toBase62(cur.lastrowid)
    short_url= host + encoded_string
    cur.execute(f"update web_url_two set short_url='{short_url}' where id={res}")
    conn.commit()

    return short_url


@app.route('/get_short_url',  methods=['GET'])
def redirect_short_url():
    short_url = request.args.get('short_url')
    cur.execute(f"select long_url from web_url_two where short_url='{short_url}'")
    redirect_url = cur.fetchone()[0]

    return redirect(redirect_url)


app.run(host='0.0.0.0', port=81, debug=True)
