from django.apps import AppConfig
from django.contrib.auth import get_user_model

class AquariumsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reefmonitor.apps.aquariums'

    def ready(self):
        # Add some functions to user model:
        def id(self):
            return self.id

        UserModel = get_user_model()
        UserModel.add_to_class('id', id)