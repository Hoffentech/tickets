from django.contrib import admin
from django.apps import apps

models = apps.get_models()

for model in models[5:]:
    admin.site.register(model)