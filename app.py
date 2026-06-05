from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def recommend_format(teams, fields, start_time, end_time):
    # Convert times to minutes
    def to_minutes(t):
        h, m = map(int, t.split(":"))
        return h * 60 + m

    total_minutes = to_minutes(end_time) - to_minutes(start_time)

    # Basic logic
    if teams <= 4:
        return "Round Robin (few teams, everyone can play each other)"

    if teams <= 8 and fields >= 2:
        return "Groups + Knockout (balanced for medium tournaments)"

    if teams > 8 and fields >= 3:
        return "Multiple Groups + Knockout (best for large tournaments)"

    if total_minutes < 180:
        return "Knockout (limited time available)"

    return "Round Robin or Groups (flexible depending on match duration)"


@app.route("/tournament/<int:tournament_id>")
def tournament_details(tournament_id):
    connection = sqlite3.connect("tournaments.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM tournaments WHERE id = ?", (tournament_id,))
    t = cursor.fetchone()

    connection.close()

    if t is None:
        return "Tournament not found"

    # Extract fields
    teams = int(t[3])
    fields = int(t[4])
    start = t[5]
    end = t[6]

    # Get recommendation
    recommendation = recommend_format(teams, fields, start, end)

    return render_template("tournament_details.html", t=t, recommendation=recommendation)

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