# flask 클래스를 import 한다                 
from flask import Flask, render_template, request, url_for, redirect 

# flask 클래스를 인스턴스화한다
app = Flask(__name__)

# URL과 실행할 함수를 매핑한다
@app.route("/")
def index():
    return "Hello, FlaskBook!"

# 루트 추가하기
#@app.route("/hello")
#def hello():
#    return "Hello, World!"

# 엔드포인트 명 추가하기
@app.route("/hello", methods=["GET"], endpoint="hello-endpoint")
def hello():
    return "Hello, World!!!!"

# Rule에 변수 지정하기
#@app.route("/hello/<name>", methods=["GET"], endpoint="helloname-endpoint")
def hello(name):
    return f"Hello, {name}"

# Rule에 변수 지정하기
@app.route("/name/<name>")
def show_name(name):
    return render_template("index.html", name=name)

#url_for 함수를 사용해서 URL 생성하기

with app.test_request_context():
    # /
    print(url_for("index"))
    # /hello/world
    print(url_for("hello-endpoint", name="world"))
    # /name/AK?page=1
    print(url_for("show_name", name="AK", page="1"))


@app.route("/contact")
def contact():
       #이메일을 보낸다.

       #contact 앤드포트로 리다이렉트 한다.
    return render_template("contact.html")

@app.route("/contact/complete", methods=["GET", "POST"])
def contact_complete():
    if request.method == "POST":
        return redirect(url_for("contact_complete"))
    return render_template("contact_complete.html")

