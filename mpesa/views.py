import base64
import datetime
import json
import logging
import requests

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

logger = logging.getLogger(__name__)

def get_access_token():
    """Fetch access token from Safaricom sandbox."""
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    try:
        response = requests.get(url, auth=(
            settings.MPESA["CONSUMER_KEY"],
            settings.MPESA["CONSUMER_SECRET"]
        ))
        response.raise_for_status()
        return response.json()['access_token']
    except requests.RequestException as e:
        logger.error(f"Access token error: {e}")
        return None


@csrf_exempt
@require_POST
def stk_push(request):
    """Initiate STK Push to customer's phone."""
    phone = request.POST.get("phone")  # Format: 2547XXXXXXXX
    amount = request.POST.get("amount")

    # Validate phone number
    if not phone or not phone.startswith("254") or len(phone) != 12:
        return JsonResponse({'error': 'Invalid phone number format'}, status=400)

    if not amount or not amount.isdigit():
        return JsonResponse({'error': 'Invalid amount'}, status=400)

    access_token = get_access_token()
    if not access_token:
        return JsonResponse({'error': 'Unable to authenticate with M-Pesa'}, status=500)

    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    password = base64.b64encode(
        f"{settings.MPESA['SHORTCODE']}{settings.MPESA['PASSKEY']}{timestamp}".encode()
    ).decode()

    payload = {
        "BusinessShortCode": settings.MPESA["SHORTCODE"],
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": int(amount),
        "PartyA": phone,
        "PartyB": settings.MPESA["SHORTCODE"],
        "PhoneNumber": phone,
        "CallBackURL": settings.MPESA["CALLBACK_URL"],
        "AccountReference": "BMWPARTS",
        "TransactionDesc": "Order Payment",
    }

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    try:
        url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return JsonResponse(response.json())
    except requests.RequestException as e:
        logger.error(f"STK Push error: {e}")
        return JsonResponse({'error': 'M-Pesa request failed', 'details': str(e)}, status=500)


@csrf_exempt
def mpesa_callback(request):
    """Receive callback from Safaricom once payment is processed."""
    try:
        data = json.loads(request.body)
        logger.info("MPESA CALLBACK:\n%s", json.dumps(data, indent=2))
        # You can save this to your DB here if needed.
    except json.JSONDecodeError as e:
        logger.error("Invalid JSON in callback: %s", e)
        return JsonResponse({"ResultCode": 1, "ResultDesc": "Invalid JSON"}, status=400)

    return JsonResponse({"ResultCode": 0, "ResultDesc": "Accepted"})
