from django.db import models
from django.utils.translation import ugettext_lazy as _


class ScrapedItem(models.Model):
    source = models.CharField(_("From what website given item was scraped"), max_length=75)
    link = models.TextField(_("Link to item"))
    title = models.CharField(_("Title of item"), max_length=50)
    publish_date = models.DateField(_("Date when item was published"))
    likes = models.IntegerField(_("Number of likes/reactions/thumbs up ect."))

    created = models.DateField(_("Created at"), auto_now_add=True)
    updated = models.DateField(_("Updated at"), auto_now=True)

    class Meta:
        ordering = ("-publish_date",)

    def __str__(self):
        return self.title


class ScrapeRecord(models.Model):
    scrape_date = models.DateField(_("Date when scraping was made"), auto_now_add=True)
    source = models.CharField(_("From what website given item was scraped"), max_length=75)
    link = models.TextField(_("Link to item"))
    items_added = models.IntegerField(_("How many items was scraped"))

    def __str__(self):
        return self.scrape_date.strftime("%Y/%m/%d")

    class Meta:
        ordering = ("-scrape_date",)
