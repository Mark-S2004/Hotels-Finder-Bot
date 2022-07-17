"""
This module has a method for extracting data about each hotel in the
results and for outputing this data in table form in the terminal.
"""
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import StaleElementReferenceException as SERE, NoSuchElementException as NSEE
from prettytable import PrettyTable


class HotelsReport:
    """HotelsReport class extract each hotel's data in the results and
    output the data as a table in the terminal"""

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def extract_data(self):
        """Extract hotels data

        Return:
            names: List of hotel names
            prices: List of hotel prices
            distances: List of the distance between the hotel and the
                        centre of the city
            review scores: List of hotel review scores
            links: List of hotel links on booking.com
        """
        # Keep trying to loop through each element to overcome Stale Element exception
        while True:
            try:
                name_elements = self.driver.find_elements_by_css_selector(
                    'h3 > a > div:first-child'
                )
                names = list(map(lambda x: x.text.strip(), name_elements))
                break
            except SERE:
                print("Element is stale. Retrying ...")

        while True:
            try:
                price_elements = self.driver.find_elements_by_class_name(
                    'fcab3ed991.bd73d13072'
                )
                prices = list(
                    map(lambda x: x.text.strip()[3:], price_elements))
                break
            except SERE:
                print("Element is stale. Retrying ...")

        while True:
            try:
                distance_elements = self.driver.find_elements_by_css_selector(
                    'span[data-testid="distance"]'
                )
                distances = list(
                    map(lambda x: x.text.split()[0], distance_elements))
                break
            except SERE:
                print("Element is stale. Retrying ...")

        while True:
            try:
                link_elements = self.driver.find_elements_by_css_selector(
                    'h3 > a'
                )
                links = list(
                    map(lambda x: x.get_attribute('href'), link_elements))
                break
            except SERE:
                print("Element is stale. Retrying ...")

        hotel_list = self.driver.find_elements_by_css_selector(
            'div[data-testid="property-card"]'
        )
        review_scores = []
        for hotel in hotel_list:
            try:
                review_score = hotel.find_element_by_class_name(
                    'b5cd09854e.d10a6220b4'
                ).text.strip()
            except NSEE:
                review_score = ''
            finally:
                review_scores.append(review_score)
        return names, prices, distances, review_scores, links

    def display_table(self, names: list, prices: list, distance: list, review: list, links: list):
        """Prints the table of hotel data

        Args:
            names: List of hotel names
            prices: List of hotel prices
            distances: List of the distance between the hotel and the
                        centre of the city
            review scores: List of hotel review scores
            links: List of hotel links on booking.com"""
        hotels_table = PrettyTable()
        hotels_table.add_column("Name", names)
        hotels_table.add_column('Price', prices)
        if distance:
            hotels_table.add_column('Distance from Centre', distance)
        hotels_table.add_column('Review Score', review)
        hotels_table.add_column('Link', links)
        hotels_table.del_column('Link')
        print(hotels_table)
