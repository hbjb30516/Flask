from flask import Flask, render_template, request, url_for, redirect, make_response, session, flash
from flask_mail import Mail, Message
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "my_secret_key")

app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER", "smtp.gmail.com")
app.config["MAIL_PORT"] = int(os.environ.get("MAIL_PORT", 587))
app.config["MAIL_USE_TLS"] = os.environ.get("MAIL_USE_TLS", "True") == "True"
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME", "your_email@gmail.com")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD", "your_password")
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_DEFAULT_SENDER", app.config["MAIL_USERNAME"])

mail = Mail(app)

# 이메일 전송 함수
def send_email(to, subject, template, **kwargs):
    try:
        msg_body = render_template(f"email/{template}.txt", **kwargs)
        msg_html = render_template(f"email/{template}.html", **kwargs)

        msg = Message(subject, recipients=[to])
        msg.body = msg_body
        msg.html = msg_html

        mail.send(msg)
        print(f"이메일 전송 완료: {to}")
    except Exception as e:
        print(f"이메일 전송 실패: {e}")

@app.route("/")
def index():
    return redirect(url_for("contact"))

@app.route("/contact")
def contact():
    response = make_response(render_template("contact.html"))
    response.set_cookie("flaskbook_key", "flaskbook_value")
    session["username"] = "AK"
    return response

@app.route("/contact/complete", methods=["POST"])
def contact_complete():
    username = request.form.get("username", "").strip()
    email = request.form.get("email", "").strip()
    description = request.form.get("description", "").strip()

    if not username or not email or not description:
        flash("모든 필드를 입력해야 합니다.", "error")
        return redirect(url_for("contact"))

    # 세션에 데이터 저장
    session["username"] = username
    session["description"] = description

    send_email(to=email, subject="문의가 접수되었습니다.", template="contact_complete", username=username, description=description)

    return redirect(url_for("contact_success"))

@app.route("/contact/success")
def contact_success():
    username = session.pop("username", "고객님")
    description = session.pop("description", "문의 내용이 없습니다.")
    return render_template("email/contact_complete.html", username=username, description=description)

if __name__ == "__main__":
    app.run(debug=True)
