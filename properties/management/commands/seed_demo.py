from django.core.management.base import BaseCommand
from properties.models import Property, PropertyMedia

class Command(BaseCommand):
    help = "Add sample listings to preview the website"
    def handle(self, *args, **options):
        samples = [
            ("Ganga Vista Premium Plot", "plot", "12,50,000", "1200 sq ft", "Sarnath, Varanasi", "A peaceful, well-connected plot with a clear title and room to build your dream home."),
            ("Kashi Courtyard Duplex", "duplex", "78,00,000", "1850 sq ft", "Rohania, Varanasi", "A bright family duplex with a private terrace, modern finishes and convenient access to the city."),
            ("Sunrise Enclave Plot", "plot", "18,75,000", "150 sq yd", "Shivpur, Varanasi", "A thoughtfully located residential plot in a growing neighbourhood, ideal for a future home."),
        ]
        for title, kind, price, area, location, description in samples:
            obj, created = Property.objects.get_or_create(title=title, defaults={
                "kind": kind, "price": price, "area": area, "location": location,
                "description": description, "is_published": True,
                "is_featured": title.startswith("Ganga"),
            })
            self.stdout.write(f"Added {obj}" if created else f"Already exists: {obj}")
        self.stdout.write(self.style.SUCCESS("Sample listings are ready. Add real photos in /admin/."))
