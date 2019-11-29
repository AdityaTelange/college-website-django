from django.views.generic.base import TemplateView


class Index(TemplateView):
    template_name = "index.html"


class AboutUs(TemplateView):
    template_name = "aboutus.html"


class ContactUS(TemplateView):
    template_name = "contactus.html"
