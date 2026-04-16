from django.utils import timezone
from django.db.models import F


class VisitorCountMiddleware:
    """Har bir yangi tashrif uchun kunlik hisoblagich.
    Bir xil sessiya bir kunda faqat 1 marta sanaladi."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Faqat asosiy landing sahifani sanash
        if request.path == '/':
            today = timezone.localdate()
            session_key = f'visited_{today}'

            if not request.session.get(session_key):
                # Sessionni belgilaymiz va saqlashga majbur qilamiz
                request.session[session_key] = True
                request.session.modified = True

                try:
                    from shop.models import VisitorStat
                    # get_or_create + F() — atom operatsiya, race condition yo'q
                    VisitorStat.objects.get_or_create(date=today)
                    VisitorStat.objects.filter(date=today).update(
                        count=F('count') + 1
                    )
                except Exception:
                    pass

        return self.get_response(request)
