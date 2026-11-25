from django import forms
from .models import Enquiry, Property

class EnquiryForm(forms.ModelForm):
    class Meta:
        model = Enquiry
        fields = ["name", "phone", "email", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Your name", "autocomplete": "name"}),
            "phone": forms.TelInput(attrs={"placeholder": "+91 98765 43210", "autocomplete": "tel"}),
            "email": forms.EmailInput(attrs={"placeholder": "you@example.com", "autocomplete": "email"}),
            "message": forms.Textarea(attrs={"placeholder": "Tell us what you are looking for…", "rows": 4}),
        }

class ContactEnquiryForm(EnquiryForm):
    class Meta(EnquiryForm.Meta):
        fields = ["name", "phone", "email", "property", "message"]
        widgets = {
            **EnquiryForm.Meta.widgets,
            "property": forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["property"].required = False
        self.fields["property"].label = "Property you are interested in (optional)"
        self.fields["property"].queryset = Property.objects.filter(is_published=True).order_by("title")
        self.fields["property"].empty_label = "General enquiry / not sure yet"
