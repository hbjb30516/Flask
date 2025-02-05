import os
from flask import Flask, render_template, request, url_for, redirect, make_response, session, flash
from flask_mail import Mail, Message  # Flask-Mail import

# Flask 애플리케이션 인스턴스 생성
app = Flask(__name__)

# 🔥 SECRET_KEY 설정 (환경 변수에서 가져오거나 기본값 설정)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "my_super_secret_key_123")

# 📧 Flask-Mail 설정
app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER", "smtp.gmail.com")  # 메일 서버 설정
app.config["MAIL_PORT"] = int(os.environ.get("MAIL_PORT", 587))  # 메일 서버 포트 설정 (정수 변환)
app.config["MAIL_USE_TLS"] = os.environ.get("MAIL_USE_TLS", "True") == "True"  # TLS 사용 여부 설정
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME", "your_email@gmail.com")  # 이메일 계정
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD", "your_password")  # 이메일 비밀번호
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_DEFAULT_SENDER", app.config["MAIL_USERNAME"])  # 기본 발신자 설정

# Flask-Mail 인스턴스 생성
mail = Mail(app)

# 🔹 이메일 전송 함수
def send_email(to, subject, template, **kwargs):
    """이메일을 보내는 함수"""
    try:
        # 템플릿 경로 설정
        txt_template = f"email/{template}.txt"
        html_template = f"email/{template}.html"

        # 템플릿 존재 여부 확인
        msg_body = render_template(txt_template, **kwargs) if os.path.exists(f"templates/{txt_template}") else "텍스트 이메일 본문이 없습니다."
        msg_html = render_template(html_template, **kwargs) if os.path.exists(f"templates/{html_template}") else "<p>HTML 이메일 본문이 없습니다.</p>"

        # 이메일 생성
        msg = Message(subject, recipients=[to])
        msg.body = msg_body
        msg.html = msg_html

        # 이메일 전송
        mail.send(msg)
        print(f"이메일이 {to}에게 성공적으로 전송되었습니다.")
    except Exception as e:
        print(f"이메일 전송 실패: {e}")

# 🔹 기본 라우트 → /contact로 리디렉트
@app.route("/")
def index():
    return redirect(url_for("contact"))  # /contact 페이지로 이동

# 🔹 문의 페이지
@app.route("/contact")
def contact():
    response = make_response(render_template("contact.html"))  # 문의 폼 페이지 렌더링
    response.set_cookie("flaskbook_key", "flaskbook_value")  # 쿠키 설정
    session["username"] = "AK"  # 세션 설정
    return response

# 🔹 문의 완료 처리 및 이메일 전송
@app.route("/contact/complete", methods=["POST"])
def contact_complete():
    # 폼에서 값 가져오기
    username = request.form.get("username", "").strip()  # 사용자명
    email = request.form.get("email", "").strip()  # 이메일 주소
    description = request.form.get("description", "").strip()  # 문의 내용

    # 필수 입력값 체크
    if not username or not email or not description:
        flash("모든 필드를 입력해야 합니다.", "error")
        return redirect(url_for("contact"))

    # 이메일 전송
    send_email(
        to=email,
        subject="문의가 접수되었습니다.",
        template="contact_complete",
        username=username,
        description=description
    )

    return redirect(url_for("contact_success"))  # 문의 완료 후 /contact/success로 이동

# 🔹 문의 성공 페이지 (새로운 라우트 추가)
@app.route("/contact/success")
def contact_success():
    return render_template("email/contact_complete.html")  # 성공 페이지 렌더링

# Flask 실행
if __name__ == "__main__":
    app.run(debug=True)
