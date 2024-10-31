from django.apps import AppConfig
from django.db.models.signals import post_migrate


class DataStorageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'data_storage'

    def ready(self):
        post_migrate.connect(run_initial_data_population, sender=self)

def run_initial_data_population(sender, **kwargs):
    from django.core.management import call_command
    call_command('populate_initial_db')
