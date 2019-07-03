from django.apps import AppConfig


class AuthuserConfig(AppConfig):
    name = 'apps.authuser'

    def ready(self):
        import apps.authuser.signals
