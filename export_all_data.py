import os
import django
import json
from django.core import serializers
from django.apps import apps

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BrillianBengaluru.settings")
django.setup()

all_data = []

for model in apps.get_models():
    if model._meta.app_label == "admin":
        continue  # skip admin logs
    queryset = model.objects.all()
    if queryset.exists():
        serialized = serializers.serialize(
            "json",
            queryset,
            use_natural_primary_keys=True,
            use_natural_foreign_keys=True
        )
        all_data.extend(json.loads(serialized))

with open("supabase_clean_data.json", "w", encoding="utf-8") as f:
    json.dump(all_data, f, indent=4, ensure_ascii=False)

print(f"✅ Full data export complete. Total objects exported: {len(all_data)}")
