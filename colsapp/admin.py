from django.contrib import admin

# Register your models here.
from colsapp.models import *

admin.site.register(
    Movie, list_display=["title"], list_display_links=["title"], list_filter=["genres"]
)

admin.site.register(
    MovieCollection, list_display=["title"], list_display_links=["title"],
)

admin.site.register(
    MovieGenre, list_display=["name"], list_display_links=["name"],
)
