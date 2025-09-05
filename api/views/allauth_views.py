
from rest_framework.views import APIView
from rest_framework.response import Response
from ..utils.auth_utils import resend_confirmation_email, send_password_reset_email

class ResendConfirmationEmailView(APIView):
    def post(self, request):
        email = request.data.get("email")
        success = resend_confirmation_email(request, email)
        if success:
            return Response({"message": "Email of confirmation sent"})
        return Response({"error": "Email already verified or does not exist"}, status=400)

class ResetPasswordEmailView(APIView):
    def post(self, request):
        email = request.data.get("email")
        success = send_password_reset_email(request, email)
        if success:
            return Response({"message": "Email of reset password sent"})
        return Response({"error": "User not found"})
