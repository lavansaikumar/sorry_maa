from flask import Flask, render_template, request, jsonify
import sqlite3, datetime

app = Flask(__name__)
SECRET_KEY = "my_secret_key_123"  # change this to your own secret key

# Initialize database
def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    time TEXT,
                    location TEXT,
                    action TEXT
                )""")
    conn.commit()
    conn.close()

# Function to log actions
def log_action(action):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    location = request.remote_addr
    c.execute("INSERT INTO logs (time, location, action) VALUES (?, ?, ?)", 
              (now, location, action))
    conn.commit()
    conn.close()

# Routes for pages
@app.route("/")
def home():
    log_action("Visited Home")
    return render_template("index.html")

@app.route("/apology")
def apology():
    log_action("Visited Apology Page")
    return render_template("apology.html")

@app.route("/memories")
def memories():
    log_action("Visited Memories Page")
    return render_template("memories.html")

@app.route("/promise")
def promise():
    log_action("Visited Promise Page")
    return render_template("promise.html")

# Secret logs page
@app.route("/logs")
def logs():
    key = request.args.get("key")
    if key != SECRET_KEY:
        return "Unauthorized"
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT * FROM logs")
    data = c.fetchall()
    conn.close()
    return render_template("logs.html", logs=data)

# API for logging button clicks
@app.route("/log_action", methods=["POST"])
def log_action_api():
    data = request.get_json()
    log_action(data["action"])
    return "Logged", 200

# Search functionality
@app.route("/search", methods=["POST"])
def search():
    data = request.get_json()
    code = data.get("code")

    # If user enters "lavan", show logs
    if code.lower() == "lavan":
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("SELECT time, location, action FROM logs")
        data = c.fetchall()
        conn.close()

        if not data:
            return jsonify({"result": "No logs found yet."})

        # Format logs into readable text
        result = []
        for row in data:
            result.append(f"At {row[0]}, from {row[1]}, clicked: {row[2]}")
        return jsonify({"result": "\n".join(result)})

    # Otherwise, show secret messages
    shared_details = {
        "12341234": "This is my heartfelt message for you, Shireesha ❤️",
        "1111": "Our first memory together was magical 🌸",
        "2222": "I promise to always stand by you 💕"
    }

    result = shared_details.get(code, "No details found for this code.")
    log_action(f"Searched for code {code}")
    return jsonify({"result": result})

if __name__ == "__main__":
    init_db()
    app.run(debug=True)