from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import re
from CateringApp.models import Product_Master, Order  # Import your models

# Chatbot logic
def chatbot_response(user_message):
    user_message = user_message.lower()

    # 🔹 Handling Product Price Query
    price_keywords = ["price of", "cost of", "rate of"]
    if any(keyword in user_message for keyword in price_keywords):
        # Extract product name using regex
        product_name = re.sub(r"(price of|cost of|rate of)", "", user_message).strip()

        # Query the database for the product
        try:
            product = Product_Master.objects.filter(name__icontains=product_name).first()
            if product:
                return f"The price of {product.name} is ₹{product.price}."
            else:
                return f"Sorry, I couldn't find a product named '{product_name}'."
        except Exception as e:
            return "Sorry, something went wrong while fetching product details."

    # 🔹 Handling Order Status Query
    if "order status" in user_message or "status of order" in user_message:
        # Extract order ID using regex
        order_id_match = re.search(r"\d+", user_message)
        if order_id_match:
            order_id = order_id_match.group()

            # Query the database for the order
            try:
                order = Order.objects.filter(orderid=order_id).first()
                if order:
                    return f"The status of your order (ID: {order.orderid}) is: {order.status}."
                else:
                    return f"Sorry, I couldn't find an order with ID '{order_id}'."
            except Exception as e:
                return "Sorry, something went wrong while fetching order details."
        else:
            return "Please provide a valid order ID."

    # 🔹 Default responses
    responses = {
        "hello": "Hi! How can I assist you?",
        "canteen timing": "The canteen is open from 8 AM to 10 PM.",
        "menu": "Check out our menu under the 'Canteen Food' section.",
        "bye": "Goodbye! Have a great day!",
    }

    return responses.get(user_message, "I'm sorry, I didn't understand that. Can you please rephrase?")

# 🔹 Chatbot API view
@csrf_exempt
def chatbot_api(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get("message", "").strip()
            bot_reply = chatbot_response(user_message)
            return JsonResponse({"reply": bot_reply})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid input."}, status=400)
    return JsonResponse({"error": "Invalid request method."}, status=405)

# 🔹 Chatbot view for rendering the HTML template
def chatbot_view(request):
    return render(request, "chatbot/chat.html")
