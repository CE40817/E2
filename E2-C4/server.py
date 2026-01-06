import time
import secrets
import re
from flask import Flask, request




app = Flask(__name__)

REGEX = re.compile(r"^([a-zA-Z0-9]+)*@example.com$")
FLAG = "CTF{" + secrets.token_hex(12) + "}"


@app.route("/search", methods=["GET"])
def search():
    q = request.args.get("q", "")
    t0 = time.time()
    REGEX.match(q)
    dt = time.time() - t0
    if dt > 3.0:
        return FLAG
    return "ok"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, threaded=False)
