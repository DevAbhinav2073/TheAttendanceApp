from django.apps import AppConfig


class InformationConfig(AppConfig):
    name = 'apps.information'

    def ready(self):
        import apps.information.signals
