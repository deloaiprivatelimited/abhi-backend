from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# -----------------------------
# Dummy Database (in-memory)
# -----------------------------
DATABASE = {
    "books": [
        {"id": 1, "name": "Clean Code", "author": "Robert C. Martin", "price": 500},
        {"id": 2, "name": "Flask Web Development", "author": "Miguel Grinberg", "price": 450},
        {"id": 3, "name": "Python Tricks", "author": "Dan Bader", "price": 300},
    ],
    "authors": [
        "Robert C. Martin",
        "Miguel Grinberg",
        "Dan Bader"
    ]
}

# -----------------------------
# WhatsApp Webhook
# -----------------------------
@app.route("/whatsapp", methods=["POST"])
def whatsapp_bot():

    # Incoming message from user
    incoming_msg = request.values.get("Body", "").lower().strip()

    # Twilio response object
    response = MessagingResponse()
    msg = response.message()

    # -----------------------------
    # Logic
    # -----------------------------
    if incoming_msg == "hi":

        msg.body(
            "📚 *Welcome to Book Bot*\n\n"
            "Please choose an option:\n"
            "1️⃣ Fetch Books\n"
            "2️⃣ Fetch Authors\n"
            "3️⃣ Fetch Book Prices\n\n"
            "Reply with *1*, *2*, or *3*"
        )

    elif incoming_msg == "1":
        reply = "📚 *Books List*\n\n"
        for book in DATABASE["books"]:
            reply += f"- {book['name']} by {book['author']}\n"
        msg.body(reply)

    elif incoming_msg == "2":
        reply = "✍ *Authors List*\n\n"
        for author in DATABASE["authors"]:
            reply += f"- {author}\n"
        msg.body(reply)

    elif incoming_msg == "3":
        reply = "💰 *Book Prices*\n\n"
        for book in DATABASE["books"]:
            reply += f"- {book['name']}: ₹{book['price']}\n"
        msg.body(reply)

    else:
        msg.body(
            "❌ *Invalid input*\n\n"
            "Send *hi* to see the menu again."
        )

    return str(response)


# -----------------------------
# Run Flask App
# -----------------------------
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
