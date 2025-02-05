# flask 클래스를 import 한다                 
from flask import Flask

# flask 클래스를 인스턴스화한다
app = Flask(__name__)

# URL과 실행할 함수를 매핑한다
@app.route("/")
def index():
    return "Hello, FlaskBook!"

# 루트 추가하기
@app.route("/hello")
def hello():
    return "Hello, World!"

# 엔드포인트 명 추가하기
@app.route("/hello", methods=["GET"], endpoint="hello-endpoint")
def hello():
    return "Hello, World!!!!"

# Rule에 변수 지정하기
@app.route("/hello/<name>", methods=["GET"], endpoint="helloname-endpoint")
def hello(name):
    return f"Hello, {name}"
