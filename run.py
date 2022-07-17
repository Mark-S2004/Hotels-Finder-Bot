"""
This module imports hotels_finder_bot package and asks the user about hotel
attributes to output a table of hotels that match the user's hotel specs
"""
from hotels_finder_bot import HotelsFinder

currency = input("Enter a currency to format hotel prices (Ex. USD): ")
location = input(
    "Where are you going to stay? [city/province/state/country] (Ex. New York)\n")
check_in = input("Enter check-in date (YYYY-MM-DD): ")
check_out = input("Enter check-out date (YYYY-MM-DD): ")
adults = input("Enter number of adults older than 17: ")
children = int(input("Enter number of children (0-17): "))
children_ages = []
if children:
    for child in range(children):
        age = input(f"Enter the age of your no. {child + 1} child: ")
        children_ages.append(age)
rooms = input("Enter number of rooms: ")

want_star_filter = input("Do you want to filter by stars? [y/n] ")
if want_star_filter == "y":
    stars = input(
        "Enter star score/s (from 1 to 5)\nFor multiple Star scores separate each by comma (Ex. 1,2,3): "
    ).split(',')
else:
    stars = ''

want_policy_filter = input("Do you want to filter by Payment policy? [y/n] ")
if want_policy_filter == "y":
    policies = input(
        "Enter Payment policy/ies [Free cancellation, Book without credit card, No prepayment]\nFor multiple policies separate each by comma (Ex. Free cancellation,No prepayment): "
    ).split(',')
else:
    policies = ''

want_meal_filter = input("Do you want to filter by meal plan? [y/n] ")
if want_meal_filter == "y":
    meals = input(
        "Enter meal plan/s [Self catering, Breakfast included, All meals included, All-inclusive, Breakfast & dinner included]\nFor multiple meal plans separate each by comma (Ex. Self catering,All-inclusive): "
    ).split(',')
else:
    meals = ''

with HotelsFinder(teardown=True) as bot:
    bot.land_first_page()
    bot.change_currency(currency)
    bot.select_place_togo(location)
    bot.select_dates(check_in, check_out)
    bot.select_people(int(adults), children, children_ages, int(rooms))
    bot.click_search()
    bot.apply_filtration(stars, policies, meals)
    bot.hotel_report()
    print('Exiting ...')
