from django.http import JsonResponse
from django.views import View
import openai
from decouple import config
from django.middleware.csrf import get_token

# Create your views here.


openai.api_key = config('OPENAI_API_KEY')

class ChatBotView(View):
    def post(self, request, *args, **kwargs):
        try:
            import json
            body = json.loads(request.body)
            user_input = body.get("message")
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": user_input}]
            )
            return JsonResponse({'response': response.choices[0].message['content'].strip()})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
