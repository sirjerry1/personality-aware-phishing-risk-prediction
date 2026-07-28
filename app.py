from flask import Flask, render_template, request, redirect, url_for, session
from database import get_connection

app = Flask(__name__)
app.config.from_object("config.Config")
app.secret_key = app.config["SECRET_KEY"]

tipi_questions = [
    "1. I see myself as extraverted, enthusiastic.",
    "2. I see myself as critical, quarrelsome.",
    "3. I see myself as dependable, self-disciplined.",
    "4. I see myself as anxious, easily upset.",
    "5. I see myself as open to new experiences, complex.",
    "6. I see myself as reserved, quiet.",
    "7. I see myself as sympathetic, warm.",
    "8. I see myself as disorganized, careless.",
    "9. I see myself as calm, emotionally stable.",
    "10. I see myself as conventional, uncreative."
]

phishing_scenarios = [

    {
    "title": "Security Alert",
    "sender": "Account Security Team",
    "subject": "Important Security Notice About Your Account",
    "date": "Today, 10:30 AM",
    "button_text": "Verify Account",

    "message":
    """
    Dear Customer,

    We noticed unusual activity on your account.

    Please verify your account within the next 24 hours.
    """
    },
    {
        "title": "Parcel Delivery",
        "sender": "Delivery Services",
        "subject": "Package Delivery Failed",
        "date": "Yesterday, 4:15 PM",
        "button_text": "Track Package",

        "message":
        """
        Dear Customer,

        Your package could not be delivered today.

        Please confirm your delivery details.
        """
    },

    {
        "title": "Account Verification",
        "sender": "Social Media Support",
        "subject": "Verify Your Account",
        "date": "Today, 9:45 AM",
        "button_text": "Verify Account",

        "message":
        """
        Dear User,

        Your account has been flagged for unusual activity.

        Please verify your identity to prevent suspension.
        """
    },

    {
        "title": "SIM Registration",
        "sender": "Mobile Network Support",
        "subject": "Update Your SIM Information",
        "date": "Today, 11:20 AM",
        "button_text": "Update Information",

        "message":
        """
        Dear Customer,

        Your SIM registration requires verification.

        Please update your information within 24 hours.
        """
    },

    {
        "title": "Reward Notification",
        "sender": "Rewards Department",
        "subject": "Congratulations! You Have Been Selected",
        "date": "Today, 2:30 PM",
        "button_text": "Claim Reward",

        "message":
        """
        Dear Customer,

        Congratulations!

        You have been selected to receive a special reward.

        Please claim your reward today.
        """
    }

]




@app.route("/")
def home():
    return render_template("home.html")

@app.route("/consent", methods=["GET", "POST"])
def consent():
    if request.method == "POST":
        print("Participant has agreed to participate.")
        return redirect(url_for("demographics"))

    return render_template("consent.html")

@app.route("/demographics", methods=["GET", "POST"])
def demographics():

    if request.method == "POST":

        age = request.form["age"]
        gender = request.form["gender"]
        occupation = request.form["occupation"]
        education = request.form["education"]
        email_use = request.form["email_use"]
        cyber_training = request.form["cyber_training"]

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute("""
        INSERT INTO participants(
            age,
            gender,
            occupation,
            education,
            email_use,
            cyber_training
        )

        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            age,
            gender,
            occupation,
            education,
            email_use,
            cyber_training
        ))

        connection.commit()
        participant_id = cursor.lastrowid
        session["participant_id"] = participant_id

        connection.close()

        return redirect(url_for("tipi"))

    return render_template("demographics.html")

@app.route("/tipi", methods=["GET", "POST"])
def tipi():

    if request.method == "POST":

        participant_id = session["participant_id"]


        q1 = request.form["q1"]
        q2 = request.form["q2"]
        q3 = request.form["q3"]
        q4 = request.form["q4"]
        q5 = request.form["q5"]
        q6 = request.form["q6"]
        q7 = request.form["q7"]
        q8 = request.form["q8"]
        q9 = request.form["q9"]
        q10 = request.form["q10"]

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
        UPDATE participants
        SET
            tipi_q1 = ?,
            tipi_q2 = ?,
            tipi_q3 = ?,
            tipi_q4 = ?,
            tipi_q5 = ?,
            tipi_q6 = ?,
            tipi_q7 = ?,
            tipi_q8 = ?,
            tipi_q9 = ?,
            tipi_q10 = ?
        WHERE id = ?
        """, (
            q1,
            q2,
            q3,
            q4,
            q5,
            q6,
            q7,
            q8,
            q9,
            q10,
            participant_id
        ))

        connection.commit()
        connection.close()

        return redirect(url_for("phishing", scenario_number=1))

    return render_template(
        "tipi.html",
        questions=tipi_questions
    )

@app.route("/phishing/<int:scenario_number>", methods=["GET", "POST"])
def phishing(scenario_number):

    if scenario_number < 1 or scenario_number > len(phishing_scenarios):
        return redirect(url_for("feedback"))

    if request.method == "POST":

        participant_id = session["participant_id"]

        response = request.form["response"]

        connection = get_connection()
        cursor = connection.cursor()

        column_name = f"scenario{scenario_number}"

        cursor.execute(
            f"UPDATE participants SET {column_name} = ? WHERE id = ?",
            (response, participant_id)
        )

        connection.commit()
        connection.close()

        if scenario_number == len(phishing_scenarios):
            return redirect(url_for("feedback"))

        return redirect(url_for("phishing", scenario_number=scenario_number + 1))

    scenario = phishing_scenarios[scenario_number - 1]

    return render_template(
        "phishing.html",
        scenario=scenario,
        scenario_number=scenario_number,
        total_scenarios=len(phishing_scenarios)
    )

@app.route("/feedback", methods=["GET", "POST"])
def feedback():

    if request.method == "POST":

        participant_id = session["participant_id"]

        confidence = request.form["confidence"]
        comments = request.form["comments"]

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
        UPDATE participants
        SET
            confidence = ?,
            comments = ?
        WHERE id = ?
        """, (
            confidence,
            comments,
            participant_id
        ))

        connection.commit()
        connection.close()

        return redirect(url_for("thank_you"))

    return render_template("feedback.html")

@app.route("/thank_you")
def thank_you():
    return render_template("thank_you.html")

if __name__ == "__main__":
    app.run(debug=True)