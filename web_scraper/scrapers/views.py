from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models.query import QuerySet
from django.shortcuts import reverse
from django.views import generic

from .forms import ScrapeForm
from .models import ScrapedItem, ScrapeRecord
from .tasks import scrape_async_dev_to, scrape_async_medium_com


class ScrapedRecordsListView(generic.FormView):
    template_name = "scrape_history.html"
    form_class = ScrapeForm

    def get_success_url(self):
        return reverse("scrapers:scrape_history")

    def form_valid(self, form):
        #scrape_async_dev_to.delay()
        scrape_async_medium_com.delay()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = self.request.GET.get("page", 1)
        qs = ScrapeRecord.objects.all()
        paginator = Paginator(qs, 50)

        try:
            qs = paginator.page(page)
        except PageNotAnInteger:
            qs = paginator.page(1)
        except EmptyPage:
            qs = paginator.page(paginator.num_pages)

        context.update({"object_list": qs})

        return context


class ScrapedItemsListView(generic.ListView):
    template_name = "scraped_items_list.html"
    paginate_by = 50

    def get_queryset(self):
        qs = ScrapedItem.objects.all()

        title = self.request.GET.get("form_title", None)
        if title:
            qs = qs.filter(title__icontains=title)

        return qs.order_by("-likes")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        title = self.request.GET.get("form_title", None)
        if title:
            count = ScrapedItem.objects.filter(title__icontains=title).count()
        else:
            count = ScrapedItem.objects.all().count()

        context.update({"total_results": count})

        return context
