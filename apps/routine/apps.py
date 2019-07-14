from django.apps import AppConfig


class RoutineConfig(AppConfig):
    name = 'apps.routine'

    def ready(self):
        import apps.routine.signals
