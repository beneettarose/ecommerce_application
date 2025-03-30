from django.apps import AppConfig


class MyappEcommerceConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "myapp_ecommerce"

    def ready(self):
        import myapp_ecommerce.signals 