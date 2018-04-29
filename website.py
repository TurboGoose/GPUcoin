from mongo_tools import MongoDataBase
from hash_tools import check_hash_strings
from flask import Flask, render_template, request
from vk_tools import get_vk_username, check_vk_user


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


@app.route("/send", methods=["GET", "POST"])
def post():
    message = None
    db.get_top()
    if request.method == "POST":
        user_from = request.form["user_from"].strip()
        user_to = request.form["user_to"].strip()
        num_coins = request.form["num_coins"].strip()

        if user_from and user_to and num_coins:

            if not check_vk_user(user_from):
                message = "Некорректный VK ID отправителя."
            elif not check_vk_user(user_to):
                message = "Некорректный VK ID получателя."
            else:

                num_coins = int(num_coins)

                if num_coins <= 0:
                    message = "Некорректная сумма."
                elif num_coins > db.check_user_balance(user_from):
                    message = "Недостаточно средств."
                elif user_from == user_to:
                    message = "Вы успешно перевели криптовалюту сами себе."
                else:

                    db.send_coins(user_from, user_to, num_coins)
                    message = "Готово!"
        else:
            message = "Вы ввели не все данные."

    return render_template("send.html", message=message)


@app.route("/top")
def top_10():
    num = 10
    top = db.get_top(num)
    rendered_top = [(get_vk_username(name), total) for name, total in top]
    return render_template("top.html", top_users=rendered_top, num=num)


if __name__ == "__main__":
    app.run(port=8080, host="localhost")
