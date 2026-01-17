import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# -----------------------------
# Dummy Database
# -----------------------------
DATABASE = {
    "books": [
        {"id": 1, "name": "Clean Code", "author": "Robert C. Martin", "price": 500},
        {"id": 2, "name": "Flask Web Development", "author": "Miguel Grinberg", "price": 450},
    ],
    "authors": [
        "Robert C. Martin",
        "Miguel Grinberg"
    ]
}

# -----------------------------
# Health Check (IMPORTANT)
# -----------------------------
@app.route("/")
def health():
    return "OK", 200

# -----------------------------
# WhatsApp Webhook
# -----------------------------
@app.route("/whatsapp", methods=["POST"])
def whatsapp_bot():

    incoming_msg = request.values.get("Body", "").lower().strip()
    response = MessagingResponse()
    msg = response.message()

    if incoming_msg == "hi":
        msg.body(
            "📚 Welcome to Book Bot\n\n"
            "1️⃣ Fetch Books\n"
            "2️⃣ Fetch Authors\n"
            "3️⃣ Fetch Book Prices"
        )

    elif incoming_msg == "1":
        reply = "📚 Books:\n"
        for book in DATABASE["books"]:
            reply += f"- {book['name']} by {book['author']}\n"
        msg.body(reply)

    elif incoming_msg == "2":
        reply = "✍ Authors:\n"
        for author in DATABASE["authors"]:
            reply += f"- {author}\n"
        msg.body(reply)

    elif incoming_msg == "3":
        reply = "💰 Prices:\n"
        for book in DATABASE["books"]:
            reply += f"- {book['name']}: ₹{book['price']}\n"
        msg.body(reply)

    else:
        msg.body("Send *hi* to see menu.")

    return str(response)

# -----------------------------
# Railway Entry Point
# -----------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
