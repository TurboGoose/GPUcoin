from flask import Flask, render_template, request
from hash_tools import check_hash_strings
from mongo_tools import MongoDataBase
from vk_tools import get_vk_username


app = Flask(__name__)
db = MongoDataBase()


@app.route("/", methods=["GET", "POST"])
def index():
    strings = []
    if request.method == "POST":
        new_strings = request.form["hashes"].strip().splitlines()
        strings = db.check_coins(check_hash_strings(new_strings))
        db.register_coins([h for h, s in strings if s])
    return render_template("index.html", res=strings)


@app.route("/wallet")
def wallet():
    error = None
    balance = None
    name = None

    user = request.args.get("vk_id")

    if user is not None:
        user = user.strip()
        if user.isdigit():
            user_name = get_vk_username(user)
            if user_name:
                name = user_name
                user_balance = db.check_user_balance(user)
                if user_balance > 0:
                    balance = user_balance
            else:
                error = "Пользователь не найден."
        else:
            error = "Неправильный ID."

    return render_template("wallet.html", error=error, balance=balance, username=name)


if __name__ == "__main__":
    app.run(port=8080, host="localhost")
