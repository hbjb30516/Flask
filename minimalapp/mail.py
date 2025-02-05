import os
from flask import Flask, render_template, request, url_for, redirect, make_response, session
from flask_mail import Mail, Message

# Flask 애플리케이션 인스턴스 생성
app = Flask(__name__)

# 🔥 SECRET_KEY 설정
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "my_super_secret_key_123")

# 📧 Flask-Mail 설정
app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER", "smtp.gmail.com")
app.config["MAIL_PORT"] = int(os.environ.get("MAIL_PORT", 587))
app.config["MAIL_USE_TLS"] = os.environ.get("MAIL_USE_TLS", "True") == "True"
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME", "your_email@gmail.com")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD", "your_password")
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_DEFAULT_SENDER", app.config["MAIL_USERNAME"])

# Flask-Mail 인스턴스 생성
mail = Mail(app)

# 🔹 이메일 전송 함수
def send_email(to, subject, template, **kwargs):
    """이메일을 보내는 함수"""
    try:
        # 📜 템플릿이 존재하는지 확인
        txt_template_path = f"email/{template}.txt"
        html_template_path = f"email/{template}.html"

        txt_body = render_template(txt_template_path, **kwargs) if os.path.exists(f"templates/{txt_template_path}") else "텍스트 본문이 없습니다."
        html_body = render_template(html_template_path, **kwargs) if os.path.exists(f"templates/{html_template_path}") else "<p>HTML 본문이 없습니다.</p>"

        msg = Message(subject, recipients=[to])
        msg.body = txt_body
        msg.html = html_body

        mail.send(msg)
        print(f"📩 이메일이 {to}에게 성공적으로 전송되었습니다.")
    except Exception as e:
        print(f"❌ 이메일 전송 실패: {e}")

# 🔹 문의 완료 처리 및 이메일 전송
@app.route("/contact/complete", methods=["GET", "POST"])
def contact_complete():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        description = request.form["description"]

        # 📩 이메일 전송
        send_email(
            to=email,
            subject="문의가 접수되었습니다.",
            template="contact_complete",
            username=username,
            description=description
        )

        return redirect(url_for("contact_complete"))
    
    return render_template("contact_complete.html")

# Flask 실행
if __name__ == "__main__":
    app.run(debug=True)