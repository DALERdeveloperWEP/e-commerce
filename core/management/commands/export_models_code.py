import json
from django.apps import apps
from django.db import models
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Export local Django models into AI-friendly JSON file"

    OUTPUT_FILE = "models_export.json"

    LOCAL_APPS = {
        "cart",
        "catalog",
        "content",
        "orders",
        "reviews",
        "seller",
        "status",
        "stores",
        "users",
    }

    def handle(self, *args, **kwargs):
        result = {}

        for app_config in apps.get_app_configs():

            # ❗ faqat local apps
            if app_config.label not in self.LOCAL_APPS:
                continue

            app_models = []

            for model in app_config.get_models():
                model_data = {
                    "name": model.__name__,
                    "table": model._meta.db_table,
                    "fields": [],
                }

                for field in model._meta.fields:
                    model_data["fields"].append(
                        self.serialize_field(field)
                    )

                app_models.append(model_data)

            result[app_config.label] = app_models

        # 🔥 overwrite file (har safar yangilanadi)
        with open(self.OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=4, ensure_ascii=False)

        self.stdout.write(
            self.style.SUCCESS(
                f"✅ Models exported successfully → {self.OUTPUT_FILE}"
            )
        )

    def serialize_field(self, field):
        field_type = field.__class__.__name__

        data = {
            "name": field.name,
            "type": field_type,
        }

        # relation model
        if hasattr(field, "related_model") and field.related_model:
            data["related_model"] = field.related_model.__name__

        # null / blank
        if hasattr(field, "null"):
            data["null"] = field.null

        if hasattr(field, "blank"):
            data["blank"] = field.blank

        # default (FIXED PROPERLY)
        if field.default is not models.NOT_PROVIDED:
            try:
                if callable(field.default):
                    data["default"] = None
                else:
                    data["default"] = str(field.default)
            except Exception:
                data["default"] = None

        return data