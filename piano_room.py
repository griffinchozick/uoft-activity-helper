from playwright.sync_api import sync_playwright
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from credentials import username, password
from typing import Dict
from datetime import datetime

utor_username = username
utor_password = password


def main():
    main_url = 'https://harthouse.ca/open'
    piano_rooms = ["East Common Room", "Bickersteth Room", "Music Room", "South Sitting Room"]
    available_bookings = []
    # List (sorted by time) of dictionaries where each dictionary is
    # {
    #   time:
    #   registerlocator:
    #   rooom:
    # }
    #
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        def login(current_page: page) -> None:
            try:
                current_page.click("#loginLink", timeout=100)
                current_page.locator('[title="UTORid login for faculty, staff and students"]').click()
                current_page.fill('#username', username)
                current_page.fill('#password', password)
                current_page.locator('text="log in"').click()
            except PlaywrightTimeoutError:
                pass

        page.goto("https://harthouse.ca/open")

        for room in piano_rooms:
        #Getting all the avalible bookings
            url = page.locator(f"text={room}").get_attribute("href")
            room_page = context.new_page()
            room_page.goto(url)
            login(room_page)
            room_page.wait_for_selector(".program-schedule-card")
            cards = room_page.locator(".program-schedule-card")
            card_count = cards.count()
            for i in range(card_count):
                card = cards.nth(i)
                spots_available = card.locator(".text-right").locator(".text-muted").text_content()
                # print(spots_available)
                if spots_available == "No Spots Available":
                    continue
                card_dict = {}
                date = card.get_attribute("data-instance-dates")
                start_time = card.get_attribute("data-instance-times").split("-")[0][:-1]
                card_datetime = f"{date} {start_time}"
                card_dict["time"] = datetime.strptime(card_datetime, '%A, %B %d, %Y %I:%M %p')
                card_dict["register"] = card.locator("text=Register")
                card_dict["room"] = room
                card_dict["page"] = room_page
                available_bookings.append(card_dict)

        sorted_bookings = sorted(available_bookings, key=lambda d: d["time"])
        i = 0
        for booking in sorted_bookings:
            print(f"{i}) {booking['time'].strftime('%A, %B %d, %I:%M %p')} (@{booking['room']})")
            i += 1

        choice = -1
        valid_input = False
        while not valid_input:
            print("Select your booking!")
            choice_input = input()
            try:
                choice = sorted_bookings[int(choice_input)]
                valid_input = True
            except ValueError:
                print("Choose number value")
            except IndexError:
                print("Choose number in list")
        choice["register"].click()
        choice["page"].click("#checkoutButton")
        choice["page"].click("[data-dismiss='modal']")
        print(booking['time'].strftime('Successfully booked for A%, %B %d, %I:%M %p!'))
        browser.close()


if __name__ == "__main__":
    main()



    # def get_selector(selector, get_all=False):
    #     page.wait_for_selector(selector)
    #     if get_all:
    #         return page.query_selector_all(selector)
    #     return page.query_selector(selector)
    #
    # def click_selector(selector: str) -> None:
    #     page.wait_for_selector(selector)
    #     page.query_selector(selector).click()
    #
    # def get_bookings(url, selector, bookings_list):
    #     page.goto(url)
    #     button = get_selector(selector)
    #     button.click()
    #
    #     page.wait_for_selector('.card-body')
    #     selectors = page.query_selector_all('.card-body')
    #
    #     index = 0
    #     for selector in selectors:
    #         index += 1
    #         slots_string = selector.query_selector('//div[1]/p[2]/small').inner_text()
    #         if slots_string == 'No Spots Available':
    #             continue
    #         slots = slots_string.split()[0]
    #
    #         unrefined_time = selector.query_selector('//div[1]/p[1]/small').inner_text()
    #         time = unrefined_time[0:2 + unrefined_time.rfind("PM")]
    #         day = selector.query_selector('//p').inner_text().split(",", 1)[0]
    #         element = selector.query_selector('.btn')
    #
    #         have_booked = False
    #         if element.inner_text() == 'DETAILS':
    #             have_booked = True
    #
    #         new_slot = BookingSlot(day, time, slots, index, have_booked, page.url)
    #         if duplicate_booking(new_slot, bookings_list):
    #             # Deletes things already recorded (e.g. South end 3:00 has booking but, North End 3:00 has booking too
    #             continue
    #         bookings_list.append(new_slot)
    #
    # def show_bookings():
    #     index = 0
    #     print(str(len(available_bookings)) + ' Bookings Available')
    #     for booking in available_bookings:
    #         already_booked = ''
    #         if booking.have_booked:
    #             already_booked = ' *Already Booked'
    #
    #         print(str(index) + ") " + booking.name + already_booked)
    #         index += 1
    #
    # def add_bookings(booking_dict: Dict, room: str) -> None:
    #     booking_cards = get_selector(".card-body", True)
    #     for card in booking_cards:
    #         if card.query_selector(".text-muted").inner_text() == "No Spots Available":
    #             continue
    #         time = card.query_selector(".card-text").inner_text().split(":")[0]
    #         if time not in booking_dict:
    #             booking_dict[time] = []
    #         booking_dict[time].append(room)
    #
    #
    #
    # #START of the program!!
    # main_url = 'https://harthouse.ca/open'
    # with sync_playwright() as p:
    #     browser = p.chromium.launch(headless=False)
    #     page = browser.new_page()
    #
    #     rooms_list = {
    #         "East Common Room": '//html/body/div[1]/div[2]/main/article/section[6]/div/div/ul/li[1]/a',
    #         "Bickerseth Room": '//html/body/div[1]/div[2]/main/article/section[6]/div/div/ul/li[2]/a',
    #         "Music Room": '/html/body/div[1]/div[2]/main/article/section[6]/div/div/ul/li[3]/a',
    #         "South Sitting Room": '//html/body/div[1]/div[2]/main/article/section[6]/div/div/ul/li[4]/a'
    #     }
    #
    #     bookings = {}
    #
    #     for room_key in rooms_list:
    #         page.goto(main_url)
    #         click_selector(rooms_list[room_key])
    #         add_bookings(bookings, room_key)
    #
    #     for key, value in sorted(bookings.items()):  # Note the () after items!
    #         print(key, value)
    #
    #     login_utor = get_selector('//*[@id="section-sign-in-first"]/div[6]/div/button')
    #     login_utor.click()
    #
    #     page.type('input[id = username]', utor_username)
    #     page.type('input[id = password]', utor_password)
    #
    #     login_button = page.query_selector('[name="_eventId_proceed"]')
    #     login_button.click()
    #
    #     page.wait_for_selector('.Menu-Item')
    #     activities = page.query_selector_all('.Menu-Item:has(>span.Menu-IconName)')
    #     swim = []
    #     for activity in activities:
    #         if 'Swim' in activity.inner_text():
    #             swim.append(activity)
    #
    #     swim[0].click()
    #     swim_url = page.url
    #
    #     '''north_end_button = get_selector('//*[@id="list-group"]/div[7]/div/div[2]/div[1]/h3')
    #     north_end_button.click()
    #
    #     page.wait_for_selector('.caption')
    #     north_selectors = page.query_selector_all('.caption.program-schedule-card-caption')'''
    #     available_bookings = []
    #     get_bookings(swim_url, '//*[@id="list-group"]/a[7]/div/div[2]/div[1]/h3', available_bookings)
    #     #North End
    #     get_bookings(swim_url, '//*[@id="list-group"]/a[5]/div/div[2]/div[1]/h3', available_bookings)
    #     #South End
    #
    #     show_bookings()
    #
    #     valid_input = False
    #     print('Pick a Booking')
    #     while not valid_input:
    #         user_choice = input()
    #         if user_choice.isdigit():
    #             if int(user_choice) < len(available_bookings):
    #                 valid_input = True
    #             else:
    #                 print("Enter a number in the range of bookings")
    #         else:
    #             print('Enter a digit')
    #
    #     picked_booking = available_bookings[int(user_choice)]
    #     page.goto(picked_booking.page_url)
    #     ind = str(picked_booking.index)
    #     reg_selector = '//*[@id="mainContent"]/div[2]/section/div/div[' + ind + ']/div/div/div[2]/button'
    #     register_button = get_selector(reg_selector)
    #     register_button.click()
    #
    #     accept_button = get_selector('//*[@id="btnAccept"]')
    #     accept_button.click()
    #
    #     add_cart = get_selector('//*[@id="mainContent"]/div[2]/form[2]/div[2]/button[2]')
    #     add_cart.click()
    #
    #     checkout = get_selector('//*[@id="checkoutButton"]')
    #     checkout.click()
    #
    #     proceed_checkout = get_selector('//*[@id="CheckoutModal"]/div/div/div[2]/button[2]')
    #     proceed_checkout.click()
    #     print("Just booked " + picked_booking.name)
    #
    #
    #     browser.close()
