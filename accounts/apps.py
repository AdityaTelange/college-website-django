from django.apps import AppConfig


class RootConfig(AppConfig):
    name = 'accounts'

    def ready(self):
        pass
