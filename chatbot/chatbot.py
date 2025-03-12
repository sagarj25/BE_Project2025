def chatbot_response(user_message):
    user_message = user_message.lower()

    # Check for product price queries
    if "price of" in user_message or "cost of" in user_message:
        # Extract product name
        product_name = user_message.replace("price of", "").replace("cost of", "").strip()

        # Query the database for the product
        try:
            product = Product_Master.objects.filter(name__icontains=product_name).first()
            if product:
                return f"The price of {product.name} is ₹{product.price}."
            else:
                return f"Sorry, I couldn't find a product named '{product_name}'."
        except Exception as e:
            return "Sorry, something went wrong. Please try again later."

    # Check for order status queries
    elif "order status" in user_message or "status of order" in user_message:
        # Extract order ID
        order_id = user_message.replace("order status", "").replace("status of order", "").strip()

        # Query the database for the order
        try:
            order = Order.objects.filter(orderid=order_id).first()
            if order:
                return f"The status of your order (ID: {order.orderid}) is: {order.status}."
            else:
                return f"Sorry, I couldn't find an order with ID '{order_id}'."
        except Exception as e:
            return "Sorry, something went wrong. Please try again later."

    # Default responses
    responses = {
        "hello": "Hi! How can I assist you?",
        "menu": "You can check our menu under the 'Canteen Food' section.",
        "hours": "Our canteen is open from 8 AM to 8 PM.",
        "contact": "You can reach us at +91-1234567890 or canteenxpress123@gmail.com.",
        "delivery": "We currently offer in-canteen pickup only.",
    }

    return responses.get(user_message, "I'm sorry, I didn't understand that. Can you please rephrase?")