import os
import json
from flask import Flask, request, Response
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
# Health Check (Railway Needs This)
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

    # -----------------------------
    # MENU WITH BUTTONS
    # -----------------------------
    if incoming_msg in ["hi", "menu", "hello"]:

        payload = {
            "messaging_product": "whatsapp",
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {
                    "text": "📚 *Welcome to Book Bot*\n\nChoose an option:"
                },
                "action": {
                    "buttons": [
                        {
                            "type": "reply",
                            "reply": {"id": "books", "title": "📚 Fetch Books"}
                        },
                        {
                            "type": "reply",
                            "reply": {"id": "authors", "title": "✍ Fetch Authors"}
                        },
                        {
                            "type": "reply",
                            "reply": {"id": "prices", "title": "💰 Book Prices"}
                        }
                    ]
                }
            }
        }

        return Response(json.dumps(payload), mimetype="application/json")

    # -----------------------------
    # BOOK LIST
    # -----------------------------
    elif incoming_msg == "books":
        reply = "📚 *Available Books*\n\n"
        for book in DATABASE["books"]:
            reply += f"- {book['name']} by {book['author']}\n"
        reply += "\nSend *menu* to go back."

    # -----------------------------
    # AUTHORS LIST
    # -----------------------------
    elif incoming_msg == "authors":
        reply = "✍ *Authors*\n\n"
        for author in DATABASE["authors"]:
            reply += f"- {author}\n"
        reply += "\nSend *menu* to go back."

    # -----------------------------
    # PRICES LIST
    # -----------------------------
    elif incoming_msg == "prices":
        reply = "💰 *Book Prices*\n\n"
        for book in DATABASE["books"]:
            reply += f"- {book['name']}: ₹{book['price']}\n"
        reply += "\nSend *menu* to go back."

    # -----------------------------
    # FALLBACK
    # -----------------------------
    else:
        reply = "❓ I didn’t understand that.\n\nSend *hi* to open menu."

    # -----------------------------
    # TEXT RESPONSE (Non-button replies)
    # -----------------------------
    response = MessagingResponse()
    response.message(reply)
    return str(response)


# -----------------------------
# Railway Entry Point
# -----------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
