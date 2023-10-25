from celery import shared_task
from celery.decorators import task

from .scrapers import (scrape_python_tagged_articles_from_dev_to,
                       scrape_python_tagged_articles_from_medium_com)


@task
def scrape_dev_to():
    base_url = "https://dev.to/"
    scrape_python_tagged_articles_from_dev_to(base_url)


# @task
# def scrape_bulldogjob():
#     url = "https://bulldogjob.pl/companies/jobs/s/city,Tr%C3%B3jmiasto/remote,true/skills,Python"
#     scrape_python_tagged_jobs_from_bulldogjob(url)


@shared_task
def scrape_async_dev_to():
    base_url = "https://dev.to/"
    scrape_python_tagged_articles_from_dev_to(base_url)


@shared_task
def scrape_async_medium_com():
    base_url = "https://medium.com/"
    scrape_python_tagged_articles_from_medium_com(base_url)
