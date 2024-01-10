# Queens College
# Internet and Web Technologies (CSCI 355)
# Winter 2024
# Assignment 4 - Data Scraping, Storage, and Visualization
# Mahfuz Rahim
# Worked with the class

#[1] Install and import these third-party libraries which are needed in the tasks below
import requests
import html5lib
from bs4 import BeautifulSoup
import OutputUtil as ou

#[2] Define a function to print the HTML content of a webpage at a given URL (uniform resource locator, web address)
def print_page_content(url):
    r = requests.get(url)
    print(r.content)

#[3] Define a function to parse the HTML content for a given URL.
def parse_page_content(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html5lib')
    print(soup.prettify())

#[4] Define a function to get the next text item from an iterator
def next_text(itr):
    return next(itr).text


#[5] Define a function to get the next int item from an iterator
def next_int(itr):
    return int(next_text(itr).replace(',', ''))


#[6] Define a function to scrape the site.
def scrape_covid_data(dict_countries_population):
    url = 'https://www.worldometers.info/coronavirus/countries-where-coronavirus-has-spread/'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    data = []
    itr = iter(soup.find_all('td'))
    # This loop will keep repeating as long as there is data available in the iterator
    while True:
        try:
            country = next_text(itr)
            cases = next_int(itr)
            deaths = next_int(itr)
            continent = next_text(itr)
            if country.startswith('Japan'):
                country = "Japan"
            if country in ['Channel Islands', 'MS Zaandam']:
                continue
            population = dict_countries_population[country]
            percent_cases = round(100 * cases/population, 2)
            percent_deaths = round(100 * deaths/cases, 2)
            data.append([country,continent, population, cases, percent_cases, deaths, percent_deaths])
        except StopIteration:
            break
    return data


#[7] Define a function get_country_population(url) that will scrape this website to get country populations:  https://www.worldometers.info/world-population/population-by-country/. Build a dictionary in which the keys are country names and the values are country populations.
#[8] Add this population data to the previously scraped data. This is important information because the numbers of COVID cases and deaths per country are more significant relative to that country's population.
def scrape_population_data():
    url = 'https://www.worldometers.info/world-population/population-by-country/'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    itr = iter(soup.find_all('td'))
    dict_countries = {}
    while True:
        try:
            no = next_text(itr)
            country = next_text(itr)
            population = next_int(itr)
            for i in range(9):
                junk = next_text(itr)
            dict_countries[country] = population
        except StopIteration:
            break
    return dict_countries


def add_wiki_link(data, i, j):
    name = data[i][j]
    wikiname = name
    if wikiname == 'Australia/Oceania':
        wikiname = 'Australia'
    href = "https://en.wikipedia.org/wiki/" + wikiname.replace(' ', '_')
    a_attributes = 'href="' + href + '" target="_blank"'
    data[i][j] = ou.create_element(ou.TAG_A, name, a_attributes)

def make_output(data, assn):
    title = "COVID Data by Country"
    align = ["L", "L", "R", "R","R", "R", "R"]
    types = ["S", "S", "N", "N", "N", "N", "N"]
    heads = ["Country", "Continent", "Population", "Cases", "Pct Cases", "Deaths", "Pct Deaths"]
    ou.write_tt_file(assn + ".txt", title, heads, data, align)
    ou.write_csv_file(assn + ".csv", heads, data,)
    ou.write_xml_file(assn + ".xml", title, heads, data, True)
    for i in range(len(data)):
        add_wiki_link(data, i, 0)
        add_wiki_link(data, i, 1)
    ou.add_stats(data, [2,3,4,5,6], 0, 1, True)
    ou.write_html_file(assn + ".html", title,  heads, types, align, data, True)

#[9] Define a function to write the data in a text table. Don't hard code values - pass parameters

def main():
    dict_countries_population = scrape_population_data()
    data = scrape_covid_data(dict_countries_population)
    make_output(data, "Assignment4")


if __name__ == "__main__":
    main()

