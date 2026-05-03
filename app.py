from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def menu():
    return render_template("menu.html")

@app.route("/create")
def create_tournament():
    return render_template("create.html")

if __name__ == "__main__":
    app.run(debug=True)
