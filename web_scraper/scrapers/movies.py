import os
import re
from datetime import datetime
import pickle
import json

import requests
from bs4 import BeautifulSoup as bs


def save_data_with_pickle(file_name, data):
    with open(f"{file_name}_pickle", "wb") as pickle_file:
        pickle.dump(data, pickle_file)


def load_data_with_pickle(file_name):
    with open(f"{file_name}_pickle", "rb") as pickle_file:
        return pickle.load(pickle_file)


def save_data_with_json(file_name, data):
    with open(f"{file_name}.json", "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=2)


def load_data_with_json(file_name):
    with open(f"{file_name}.json", "r", encoding="utf-8") as json_file:
        return json.load(json_file)


def clean_tags(soup):
    for tag in soup.find_all(["span", "sup"]):
        tag.decompose()


def running_time_to_int(running_time):
    if running_time == "N/A":
        return None
    elif isinstance(running_time, list):
        return int(running_time[0].split()[0])
    else:  # running_time --> str
        return int(running_time.split()[0])


def parse_value_syntax(string_to_convert, number_pattern):
    string_to_convert = string_to_convert.replace(",", "")

    return float(re.search(number_pattern, string_to_convert).group())


def word_to_value(word):
    value_dict = {"billion": 1000000000, "million": 1000000, "thousand": 1000}

    return value_dict.get(word.lower(), 1)


def parse_word_syntax(string_to_convert, amounts_pattern, number_pattern):
    word_modifier = re.search(amounts_pattern, string_to_convert, flags=re.IGNORECASE).group()
    word_modifier_value = word_to_value(word_modifier)

    value = parse_value_syntax(string_to_convert, number_pattern)

    return value * word_modifier_value


def money_to_float_conversion(money_to_convert):
    if isinstance(money_to_convert, list):
        money_to_convert = money_to_convert[0]

    number_pattern = r"\d+(,\d{3})*\.*\d*"
    amounts_pattern = r"(billion|million|thousand)"
    full_pattern = rf"\${number_pattern}(-|–|\sto\s)?(\${number_pattern})?\s{amounts_pattern}"

    word_syntax = re.search(full_pattern, money_to_convert, flags=re.IGNORECASE)  # word syntax: $12,5 millions
    value_syntax = re.search(rf"\${number_pattern}", money_to_convert)  # value syntax: $12,000.58

    if word_syntax:
        return parse_word_syntax(word_syntax.group(), amounts_pattern, number_pattern)

    elif value_syntax:
        return parse_value_syntax(value_syntax.group(), number_pattern)

    else:
        return None


def clean_date(date):
    return date.split("(")[0].strip()


def date_conversion(date):
    if isinstance(date, list):
        date = date[0]

    if date == "N/A":
        return None

    date_str = clean_date(date)

    date_formats = ["%B %d, %Y", "%d %B %Y", "%Y"]
    for date_format in date_formats:
        try:
            return datetime.strptime(date_str, date_format)
        except:
            pass


def get_omdb_data(movie_title):
    api_key = os.environ.get("OMDB_API_KEY")
    full_url = f"http://www.omdbapi.com/?apikey={api_key}&t={movie_title}"

    return requests.get(full_url).json()


def get_rotten_tomato_score(omdb_data):
    ratings = omdb_data.get("Ratings", [])

    for rating in ratings:
        if rating["Source"] == "Rotten Tomatoes":
            return rating["Value"]

    return None


def get_content_value(td_element):
    if td_element.find("li"):
        return [li.get_text(" ", strip=True).replace("\xa0", " ") for li in td_element.find_all("li")]

    elif td_element.find("br"):
        return [text for text in td_element.stripped_strings]

    else:
        return td_element.get_text(" ", strip=True).replace("\xa0", " ")


def get_movie_info(url):
    movie_info = {}
    r = requests.get(url)

    soup = bs(r.content)
    clean_tags(soup)
    info_box = soup.find("table", class_="infobox vevent")
    table_rows = info_box.find_all("tr")

    for index, table_row in enumerate(table_rows):
        header = table_row.find("th")

        if index == 0:
            movie_info["title"] = table_row.get_text(" ", strip=True)

        elif header:
            content_key = table_row.find(class_="infobox-label").get_text(" ", strip=True)
            content_value = get_content_value(table_row.find(class_="infobox-data"))
            movie_info[content_key] = content_value

        else:
            pass

    return movie_info


def main():
    base_url = "https://en.m.wikipedia.org"
    r = requests.get("https://en.m.wikipedia.org/wiki/List_of_Walt_Disney_Pictures_films")
    soup = bs(r.content)
    clean_tags(soup)
    movies = soup.select("table.wikitable.sortable i a")

    movies_info = []
    for index, movie in enumerate(movies):
        try:
            relative_path = movie["href"]
            full_path = f"{base_url}{relative_path}"

            movies_info.append(get_movie_info(full_path))
        except Exception as e:
            print(movie.get_text())
            print(e)

    # ------------------------------------------------------------------------------------
    # transorm into desired format + added ratings from imdb, rotten_tomato and metascore
    # ------------------------------------------------------------------------------------
    for movie in movies_info:
        current_running_time = movie.get("Running time", "N/A")
        movie["Running time"] = running_time_to_int(current_running_time)

        current_budget = movie.get("Budget", "N/A")
        movie["Budget"] = money_to_float_conversion(current_budget)

        current_box_office = movie.get("Box office", "N/A")
        movie["Box office"] = money_to_float_conversion(current_box_office)

        current_release_date = movie.get("Release date", "N/A")
        movie["Release date"] = date_conversion(current_release_date)

        title = movie["title"]
        omdb_data = get_omdb_data(title)
        movie["imdb"] = omdb_data.get("imdbRating")
        movie["metascore"] = omdb_data.get("Metascore")
        movie["rotten_tomatoes"] = get_rotten_tomato_score(omdb_data)

    # ------------------------------------------------------------------------------------------------------------------------------
    # save to files -> pickle, json (before it, transorm datetime object to str -> json has problem with handle datetime object) and csv
    # ------------------------------------------------------------------------------------------------------------------------------

    save_data_with_pickle("disney_data", movies_info)

    movies_info_copy = [movie.copy() for movie in movies_info]
    for movie in movies_info_copy:
        current_date = movie["Release date"]
        if current_date:
            movie["Release date"] = current_date.strftime("%B %d, %Y")
        else:
            movie["Release date"] = None

    save_data_with_json("disney_data", movies_info_copy)
