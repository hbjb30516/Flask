from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def show_name():
    name = None
    if request.method == "POST":
        name = request.form.get("name")
        if name:
            if len(name) % 2 == 0:
                name = name.upper()
            else:
                name = name.lower()
    return render_template("name.html", name=name)