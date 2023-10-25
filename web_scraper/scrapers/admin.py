from django.contrib import admin

from .models import ScrapedItem, ScrapeRecord


@admin.register(ScrapedItem)
class ScrapedItemAdmin(admin.ModelAdmin):
    list_display = ("source", "title", "likes", "publish_date")


@admin.register(ScrapeRecord)
class ScrapeRecordAdmin(admin.ModelAdmin):
    list_display = ("scrape_date", "source", "items_added")
