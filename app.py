from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route("/tournament/<int:tournament_id>")
def tournament_details(tournament_id):
    connection = sqlite3.connect("tournaments.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM tournaments WHERE id = ?", (tournament_id,))
    tournament = cursor.fetchone()

    connection.close()

    if tournament is None:
        return "Tournament not found"

    return render_template("tournament_details.html", t=tournament)

@app.route("/")
def menu():
    return render_template("menu.html")

@app.route("/create", methods=["GET", "POST"])
def create_tournament():
    if request.method == "POST":
        # Read form data
        name = request.form.get("tournament_name")
        date = request.form.get("tournament_date")
        teams = request.form.get("teams")
        fields = request.form.get("fields")
        start = request.form.get("start_time")
        end = request.form.get("end_time")
        t_type = request.form.get("tournament_type")
        mode = request.form.get("game_mode")

        # Save to SQLite
        connection = sqlite3.connect("tournaments.db")
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO tournaments 
            (name, date, teams, fields, start_time, end_time, tournament_type, game_mode)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, date, teams, fields, start, end, t_type, mode))

        connection.commit()
        connection.close()

        return "Tournament saved successfully!"

    return render_template("create.html")

@app.route("/tournaments")
def tournaments_list():
    connection = sqlite3.connect("tournaments.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM tournaments")
    tournaments = cursor.fetchall()

    connection.close()

    return render_template("tournaments.html", tournaments=tournaments)

if __name__ == "__main__":
    app.run(debug=True)