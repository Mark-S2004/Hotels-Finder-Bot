"""
This file is used to automate searching process for hotels on booking.com and
to present the results in the terminal
"""
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .hotels_filtration import HotelsFiltration
from .hotels_report import HotelsReport


class HotelsFinder(webdriver.Chrome):
    """Booking class automates searching for hotels on booking.com and
       presenting them in the terminal

    Attributes:
    driver_path: Chrome Driver path (Raw String). By Default chromedriver
                will be searched for in "C:/SeleniumDrivers"
    teardown: Determines whether brwoser shuts down after code execution
                (Default True)
    """

    def __init__(self, driver_path: str = r";C:\SeleniumDrivers", teardown: bool = True):
        self.driver_path = driver_path
        self.teardown = teardown
        os.environ["PATH"] += self.driver_path
        options = webdriver.ChromeOptions()
        options.binary_location = r'C:\Program Files\Google\Chrome Beta\Application\chrome.exe'
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        super(HotelsFinder, self).__init__(options=options)
        self.implicitly_wait(15)
        self.maximize_window()

    def __exit__(self, *args) -> None:
        if self.teardown:
            self.quit()

    def land_first_page(self):
        """Load the landing page of booking.com."""
        self.get("https://www.booking.com")

    def change_currency(self, currency: str = 'USD'):
        """Changes the currency of hotel prices

        Args:
            currency: The initials of the currency (Default "USD")
        """
        currency_list = self.find_element_by_css_selector(
            'button[data-tooltip-text="Choose your currency"]'
        )
        currency_list.click()
        currency_element = self.find_element_by_css_selector(
            f'a[data-modal-header-async-url-param*="selected_currency={currency.upper()}"]'
        )
        currency_element.click()

    def select_place_togo(self, place_to_go: str):
        """Filters the location of the hotels

        Args:
            place_to_go: The city/province/state/country that you are searching for hotels in
        """
        search_field = self.find_element_by_id('ss')
        search_field.clear()
        search_field.send_keys(place_to_go)
        first_result = self.find_element_by_css_selector(
            'li[data-i="0"]'
        )
        first_result.click()

    def select_dates(self, check_in_date: str, check_out_date: str):
        """Selects the duration and dates of accomodation.
           Dates in the past will automatically be replaced with the current day.

        Args:
            check_in_date (YYYY-MM-DD): Date of check in
            check_in_date (YYYY-MM-DD): Date of check out
        """
        check_in_element = self.find_element_by_css_selector(
            f'td[data-date="{check_in_date}"]'
        )
        check_in_element.click()
        check_out_element = self.find_element_by_css_selector(
            f'td[data-date="{check_out_date}"]'
        )
        check_out_element.click()

    def select_people(self, adult_count: int, children_count: int, children_ages: list, room_count: int):
        """Selects the number of guests and rooms

        Args:
            adult_count: Number of adult guests (+17)
            children_count: Number of children guest (0-17)
            room_count: Number of rooms to be booked
        """
        selection_element = self.find_element_by_id('xp__guests__toggle')
        selection_element.click()
        self.change_guest_count('adults', adult_count)
        self.change_guest_count('children', children_count)
        if children_count:
            for child in range(children_count):
                self.find_element_by_css_selector(
                    f'select[data-group-child-age="{child}"] > option[value="{children_ages[child]}"]'
                ).click()
        self.change_guest_count('rooms', room_count)

    def change_guest_count(self, type_of_guest: str, count: int):
        """Changes the number of guests or rooms

        Args:
            type_of_guest: (adults/children/rooms)
            count: Number of guests or rooms
        """
        default_value = int(self.find_element_by_id(
            f'{"no" if type_of_guest=="rooms" else "group"}_{type_of_guest.lower()}'
        ).get_attribute('value'))
        if count > default_value:
            add_btn = self.find_element_by_css_selector(
                f'button[aria-label="Increase number of {type_of_guest.capitalize()}"]'
            )
            for _ in range(count - default_value):
                add_btn.click()
        else:
            subtract_btn = self.find_element_by_css_selector(
                f'button[aria-label="Decrease number of {type_of_guest.capitalize()}"]'
            )
            for _ in range(default_value - count):
                subtract_btn.click()

    def click_search(self):
        """Search for hotels. Pick place, dates, guest and room count
        before searching."""
        self.find_element_by_css_selector(
            'button[data-sb-id="main"]'
        ).click()

    def apply_filtration(self, stars: list, policies: 'list[str]', meals: 'list[str]'):
        """Filters hotel resutls

        Args:
            stars: List of star numbers awarded to the hotel (from 1 to 5)
            policies: List of cancellation policies [Free cancellation,
            Book without credit card, No prepayment]
            meals: List of meal plans [Self catering, Breakfast included,
            All meals included, All-inclusive, Breakfast & dinner included]
        """
        filtration = HotelsFiltration(driver=self)
        # if statement allow the user to apply no filters
        if stars:
            filtration.star_rating(stars)
        if policies:
            filtration.choose_cancellation_policy(policies)
        if meals:
            filtration.choose_meals(meals)

    def hotel_report(self):
        """Output a table of hotels' names, prices, distances from centre,
           review scores in the terminal."""
        WebDriverWait(self, 5).until(
            EC.invisibility_of_element(
                (By.CSS_SELECTOR, 'div[data-testid="overlay-card"]')
            )
        )
        report = HotelsReport(self)
        name, price, distance, review, link = report.extract_data()
        report.display_table(name, price, distance, review, link)
