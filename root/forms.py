import logging

from django import forms
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


class ContactForm(forms.Form):
    name = forms.CharField(label='Your Name', max_length=100)
    email = forms.EmailField(label="Enter your E-mail id", max_length=254)
    message = forms.CharField(
        max_length=500, widget=forms.Textarea
    )

    def send_mail(self):
        logger.info("Sending email to customer service")

        message = "From: {0}\nEmail: {1}\nMessage: {2}".format(self.cleaned_data["name"],
                                                               self.cleaned_data["email"],
                                                               self.cleaned_data["message"], )
        send_mail("Site message", message, "site@booktime.domain", [self.cleaned_data["email"]],
                  fail_silently=False, )
