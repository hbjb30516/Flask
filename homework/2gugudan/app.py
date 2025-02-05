from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def gugudan():
    result = None
    if request.method == "POST":
        dan = request.form.get("dan")
        
        if not dan:
            result = "아직 아무 숫자도 입력이 안되었습니다."
        elif not dan.isdigit():  # 숫자가 아닐 경우: isdigit()
            result = "문자가 입력되었습니다. 숫자를 입력해주세요."
        else:
            dan = int(dan)
            result = [f"{dan} x {i} = {dan * i}" for i in range(1, 10)]

    return render_template("index.html", result=result)
