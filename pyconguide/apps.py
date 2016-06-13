from django.apps import AppConfig


class PyConGuideConfig(AppConfig):
    name = 'pyconguide'
    verbose_name = 'PyCon Guide'

    def ready(self):
        import pyconguide.signals
