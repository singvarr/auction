from django.conf import settings

redirect_urls = {
    "SUCCESS_PAYMENT_URL": f"{settings.STRIPE_API_KEY}/success",
    "CANCEL_PAYMENT_URL": f"{settings.STRIPE_API_KEY}/cancel",
}
