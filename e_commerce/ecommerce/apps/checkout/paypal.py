from django.conf import settings
from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment


class PayPalClient:
    def __init__(self):
        self.client_id = getattr(settings, 'PAYPAL_CLIENT_ID')
        self.client_secret = getattr(settings, 'PAYPAL_SECRET')
        self.environment = SandboxEnvironment(client_id=self.client_id, client_secret=self.client_secret)
        self.client = PayPalHttpClient(self.environment)
