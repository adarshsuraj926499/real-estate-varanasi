from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .forms import ContactEnquiryForm, EnquiryForm
from .models import Property

WHATSAPP_CONTACTS = [
    {"number": "8173870956", "role": "Property enquiries"},
    {"number": "8815596139", "role": "Plot enquiries"},
    {"number": "9264992814", "role": "Duplex enquiries"},
    {"number": "7905747686", "role": "Site visits & support"},
]

def home(request):
    featured = Property.objects.filter(is_published=True, is_featured=True).prefetch_related("media")[:3]
    latest = Property.objects.filter(is_published=True).prefetch_related("media")[:6]
    return render(request, "home.html", {"featured": featured, "properties": latest})

def property_list(request, kind=None):
    qs = Property.objects.filter(is_published=True).prefetch_related("media")
    if kind in ("plot", "duplex"):
        qs = qs.filter(kind=kind)
    return render(request, "property_list.html", {"properties": qs, "kind": kind})

def property_detail(request, slug):
    item = get_object_or_404(Property.objects.prefetch_related("media"), slug=slug, is_published=True)
    form = EnquiryForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        enquiry = form.save(commit=False)
        enquiry.property = item
        enquiry.save()
        return redirect("enquiry_success")
    return render(request, "property_detail.html", {"item": item, "form": form})

def enquiry_success(request):
    return render(request, "enquiry_success.html")

def contact(request):
    return render(request, "contact.html", {"whatsapp_contacts": WHATSAPP_CONTACTS})

def general_enquiry(request):
    form = ContactEnquiryForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("enquiry_success")
    return render(request, "enquiry_form.html", {"form": form})
