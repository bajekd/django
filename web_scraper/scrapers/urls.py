from django.urls import include, path

from .views import ScrapedItemsListView, ScrapedRecordsListView

app_name = "scrapers"

urlpatterns = [
    path("", ScrapedItemsListView.as_view(), name="scraped_items_list"),
    path("history/", ScrapedRecordsListView.as_view(), name="scrape_history"),
]
