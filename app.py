from flask import Flask, render_template, session, request, redirect

app = Flask(__name__)

app.secret_key = "aaa"

user_data = {}


@app.route("/", methods=["GET"])
def index():
    if "flag" in session and session["flag"]:
        msg = "hello,"+str(session["uid"])
        return render_template("index.html",
                               title="ログイン後の画面です",
                               message=msg)
    else:
        return redirect("/login")


@app.route('/login', methods=['GET'])
def login():
    return render_template("login.html",
                           title="ログインページ",
                           message="以下のフォームからログインしてね")


@app.route('/login', methods=['POST'])
def login_post():
    uid = request.form["uid"]
    pwd = request.form["pwd"]

    #ユーザが登録済みであった場合
    if uid in user_data:
        # IDとパスワードの組み合わせが合っていれば、ログイン済みにする
        if user_data[uid] == pwd:
            session["flag"] = True
        #　ログイン済みにしない
        else:
            session["flag"] = False
    #ユーザが登録していなかった場合、登録してログイン済みにする
    else:
        user_data[uid] = pwd
        session["flag"] = True

    session["uid"] = uid

    if session["flag"]:
        return redirect("/")
    else:
        return render_template("login.html",
                               title="ログインページ",
                               message="パスワードが違います")


@app.route('/logout')
def logout():
    session.pop('uid', None)
    session.pop("flag", None)
    return redirect("/")

# @app.route("/next", methods=["GET"])
# def hello_next():
#     return render_template("next.html",
#                            title="レイアウトファイルを試してみるよ",
#                            message="これは別ページのサンプルです。",
#                            data=["apple","banana","cocoa"])


# @app.route("/<id>/<password>")
# def id_pass(id, password):
#     msg = "id: {}, password: {}".format(id, password)
#     return render_template("index.html",
#                            title="Jinjaテンプレートエンジンを使ってみよう！",
#                            message=msg)


# @app.route("/", methods=["POST"])
# def form():
#     field = request.form["field"]
#     return render_template("index.html",
#                            title="フォームを試してみるよ",
#                            message="あなたは , {} が好きなんですね".format(field))


if __name__ == "__main__":
    app.debug = True
    app.run(host="localhost")
