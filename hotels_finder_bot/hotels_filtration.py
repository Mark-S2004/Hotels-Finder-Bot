"""
This module has BookingFiltration Class that filter hotel results after
search button is clicked.
This module is imported to booking.py module.
"""
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException as NSEE


class HotelsFiltration:
    """HotelsFiltration class filters hotel results after search"""

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def star_rating(self, stars: list):
        """Filter hotels by number of stars

        Args:
            stars: List of star numbers awarded to the hotel (from 1 to 5)
        """
        for star in stars:
            tickbox = self.driver.find_element_by_css_selector(
                f'div[data-filters-item="class:class={star}"]'
            )
            tickbox.click()

    def choose_cancellation_policy(self, policies: "list[str]"):
        """Filter hotels by cancellation policies

        Args:
            policies: List of cancellation policies [Free cancellation,
            Book without credit card, No prepayment]
        """
        def convert_policy_to_index(policy: str) -> "tuple[int, str]":
            """Convert policy to its index number in data-filter-item
            attribute in the DOM"""
            policy = policy.capitalize()
            if policy == 'Free cancellation':
                return (2, policy)
            elif policy == 'No prepayment':
                return (5, policy)
            else:
                return (4, policy)
        dom_policies = list(map(convert_policy_to_index, policies))

        for i, policy in dom_policies:
            try:
                self.driver.implicitly_wait(3)
                self.driver.find_element_by_css_selector(
                    f'div[data-filters-item="fc:fc={i}"]'
                ).click()
            except NSEE:
                print(f'There is no hotels that offer {policy} policy')

    def choose_meals(self, meals: 'list[str]'):
        """Choose hotel meal plans

        Args:
            meals: List of meal plans [Self catering, Breakfast included,
            All meals included, All-inclusive, Breakfast & dinner included]
        """
        def convert_meal_to_index(meal: str):
            """Convert meal plan to its index number in data-filter-item
            attribute in the DOM"""
            meal = meal.capitalize()
            if meal == 'Self catering':
                return (999, meal)
            elif meal == 'Breakfast included':
                return (1, meal)
            elif meal == 'All meals included':
                return (3, meal)
            elif meal == 'All-inclusive':
                return (4, meal)
            else:
                return (9, meal)
        dom_meals = list(map(convert_meal_to_index, meals))

        for i, meal in dom_meals:
            try:
                self.driver.implicitly_wait(3)
                self.driver.find_element_by_css_selector(
                    f'div[data-filters-item="mealplan:mealplan={i}"]'
                ).click()
            except NSEE:
                print(f'There is no hotels that offer {meal} meal plan')
