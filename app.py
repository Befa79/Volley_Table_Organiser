from flask import Flask, render_template, request, redirect, url_for
import sqlite3

@app.route("/create", methods=["GET", "POST"])
def create_tournament():
    if request.method == "POST":
        name = request.form.get("tournament_name")
        date = request.form.get("tournament_date")
        teams = request.form.get("teams")
        fields = request.form.get("fields")
        start = request.form.get("start_time")
        end = request.form.get("end_time")
        t_type = request.form.get("tournament_type")
        mode = request.form.get("game_mode")

        connection = sqlite3.connect("tournaments.db")
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO tournaments 
            (name, date, teams, fields, start_time, end_time, tournament_type, game_mode)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, date, teams, fields, start, end, t_type, mode))

        connection.commit()
        connection.close()

        return redirect(url_for("tournament_saved"))

    return render_template("create.html")