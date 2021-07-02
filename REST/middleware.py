from datetime import datetime
from adminboard.models import CreateCandidate
from django.utils.deprecation import MiddlewareMixin
from .tasks import encrypt_db
from .models import TestData


class EncryptDatabaseMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if TestData.objects.all().count() > 0:
            encrypt_db.delay()