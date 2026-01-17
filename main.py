import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# -----------------------------
# Dummy Orders Database
# -----------------------------
DATABASE = {
    "orders": [
        {
            "id": 1,
            "party": "Riya Boutique",
            "saree": "Banarasi Silk",
            "quantity": 5,
            "remarks": "Urgent delivery",
            "status": "pending"
        },
        {
            "id": 2,
            "party": "Meena Sarees",
            "saree": "Kanjivaram",
            "quantity": 3,
            "remarks": "Blouse matching required",
            "status": "blouse work"
        },
        {
            "id": 3,
            "party": "Lakshmi Stores",
            "saree": "Cotton Silk",
            "quantity": 10,
            "remarks": "Design approved",
            "status": "decho"
        },
        {
            "id": 4,
            "party": "Ananya Fashions",
            "saree": "Chiffon",
            "quantity": 8,
            "remarks": "Gum completed",
            "status": "gum"
        },
        {
            "id": 5,
            "party": "Radha Collections",
            "saree": "Georgette",
            "quantity": 6,
            "remarks": "Delivered to shop",
            "status": "delivered"
        },
        {
            "id": 6,
            "party": "Sita Boutique",
            "saree": "Tussar Silk",
            "quantity": 4,
            "remarks": "Order closed",
            "status": "closed"
        }
    ]
}

# -----------------------------
# Health Check
# -----------------------------
@app.route("/")
def health():
    return "OK", 200

# -----------------------------
# Helper Function
# -----------------------------
def list_orders(status=None):
    orders = DATABASE["orders"]

    if status:
        orders = [o for o in orders if o["status"] == status]

    if not orders:
        return "❌ No orders found."

    reply = ""
    for o in orders:
        reply += (
            f"🧵 Party: {o['party']}\n"
            f"👗 Saree: {o['saree']}\n"
            f"📦 Qty: {o['quantity']}\n"
            f"📝 Remarks: {o['remarks']}\n"
            f"📌 Status: {o['status'].title()}\n"
            "--------------------\n"
        )
    return reply

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
            "🧾 *Order Management Bot*\n\n"
            "1️⃣ List All Orders\n"
            "2️⃣ Pending Orders\n"
            "3️⃣ Decho Orders\n"
            "4️⃣ Blouse Work Orders\n"
            "5️⃣ Gum Orders\n"
            "6️⃣ Delivered Orders\n"
            "7️⃣ Closed Orders\n\n"
            "👉 Send number to continue"
        )

    elif incoming_msg == "1":
        msg.body("📋 *All Orders*\n\n" + list_orders())

    elif incoming_msg == "2":
        msg.body("⏳ *Pending Orders*\n\n" + list_orders("pending"))

    elif incoming_msg == "3":
        msg.body("🧶 *Decho Orders*\n\n" + list_orders("decho"))

    elif incoming_msg == "4":
        msg.body("✂ *Blouse Work Orders*\n\n" + list_orders("blouse work"))

    elif incoming_msg == "5":
        msg.body("🧴 *Gum Orders*\n\n" + list_orders("gum"))

    elif incoming_msg == "6":
        msg.body("🚚 *Delivered Orders*\n\n" + list_orders("delivered"))

    elif incoming_msg == "7":
        msg.body("✅ *Closed Orders*\n\n" + list_orders("closed"))

    else:
        msg.body("❓ Send *hi* to see menu.")

    return str(response)

# -----------------------------
# Railway / Server Entry Point
# -----------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
