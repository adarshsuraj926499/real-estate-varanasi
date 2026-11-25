from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("properties/", views.property_list, name="property_list"),
    path("plots/", views.property_list, {"kind": "plot"}, name="plot_list"),
    path("duplex/", views.property_list, {"kind": "duplex"}, name="duplex_list"),
    path("property/<slug:slug>/", views.property_detail, name="property_detail"),
    path("enquiry/success/", views.enquiry_success, name="enquiry_success"),
    path("contact/", views.contact, name="contact"),
    path("enquiry/", views.general_enquiry, name="general_enquiry"),
]
