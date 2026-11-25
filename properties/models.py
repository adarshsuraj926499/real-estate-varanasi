from django.db import models
from django.urls import reverse
from django.utils.text import slugify

class Property(models.Model):
    class Kind(models.TextChoices):
        PLOT = "plot", "Plot"
        DUPLEX = "duplex", "Duplex"

    title = models.CharField(max_length=180)
    slug = models.SlugField(
        "Website URL name",
        max_length=200,
        unique=True,
        blank=True,
        help_text="This appears in the property page link and is generated from the title automatically.",
    )
    kind = models.CharField(max_length=12, choices=Kind.choices)
    price = models.DecimalField(max_digits=14, decimal_places=2, help_text="INR")
    area = models.CharField(max_length=80, help_text="Example: 1200 sq ft or 100 sq yd")
    location = models.CharField(max_length=200)
    address = models.TextField(blank=True)
    description = models.TextField()
    map_url = models.URLField(blank=True, help_text="Google Maps link or embed URL")
    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-is_featured", "-created_at"]
        verbose_name_plural = "Properties"

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title) or "property"
            slug, index = base, 2
            while Property.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug, index = f"{base}-{index}", index + 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("property_detail", args=[self.slug])

    @property
    def cover(self):
        return self.media.filter(is_cover=True).first() or self.media.first()

    def __str__(self):
        return self.title

class PropertyMedia(models.Model):
    class MediaType(models.TextChoices):
        PHOTO = "photo", "Photo"
        VIDEO = "video", "Video"

    property = models.ForeignKey(Property, related_name="media", on_delete=models.CASCADE)
    file = models.FileField(upload_to="properties/%Y/%m/")
    media_type = models.CharField(max_length=8, choices=MediaType.choices, default=MediaType.PHOTO)
    caption = models.CharField(max_length=160, blank=True)
    is_cover = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Photo / video"
        verbose_name_plural = "Photos / videos"

    def __str__(self):
        return f"{self.get_media_type_display()} — {self.property.title}"

class Enquiry(models.Model):
    class Status(models.TextChoices):
        NEW = "new", "New"
        CONTACTED = "contacted", "Contacted"
        CLOSED = "closed", "Closed"

    property = models.ForeignKey(Property, related_name="enquiries", on_delete=models.PROTECT, null=True, blank=True)
    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=30)
    email = models.EmailField(blank=True)
    message = models.TextField(blank=True)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.NEW)
    admin_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} — {self.property.title if self.property else 'General enquiry'}"
