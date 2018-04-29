from flask import Flask, render_template, request
from hash_tools import check_strings
from mongo_tools import MongoDataBase

app = Flask(__name__)
db = MongoDataBase()


@app.route('/', methods=['GET', 'POST'])
def index():
    strings = []
    if request.method == "POST":
        new_strings = request.form["hashes"].strip().splitlines()
        strings = db.check_coins(check_strings(new_strings))
        db.register_coins([h for h, s in strings if s])
    return render_template('index.html', res=strings)


if __name__ == '__main__':
    app.run(port=8080, host='localhost')
