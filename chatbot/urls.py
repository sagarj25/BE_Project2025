from django.urls import path
from .views import chatbot_view, chatbot_api  # Import the views
from .views import chatbot_response
urlpatterns = [
    path('chatbot/', chatbot_response, name='chatbot_response'),  # API endpoint
    path("chat/", chatbot_view, name="chatbot_view"),   # HTML page
]