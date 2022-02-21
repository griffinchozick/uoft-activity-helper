from playwright.sync_api import sync_playwright
from credentials import username, password, people

answers = ["Yes", "No", "No", "No", "No", "No", "No", "No"]
utor_username = username
utor_password = password



class BookingSlot:
    def __init__(self, day, time, slots_left, index, have_booked, page_url):
        self.day = day
        self.time = time
        self.slots_left = slots_left
        self.index = index
        self.have_booked = have_booked
        self.page_url = page_url
        self.name = (day + ' ' + time + ' ' + 'Slots Left: ' + slots_left)

def duplicate_booking(booking, bookings_list):
    for _bookings in bookings_list:
        if booking.time == _bookings.time and booking.day == _bookings.day:
            return True
    return False

def main():
    def get_selector(selector):
        page.wait_for_selector(selector)
        return page.query_selector(selector)

    def get_bookings(url, selector, bookings_list):
        page.goto(url)
        button = get_selector(selector)
        button.click()

        page.wait_for_selector('.card-body')
        selectors = page.query_selector_all('.card-body')

        index = 0
        for selector in selectors:
            index += 1
            slots_string = selector.query_selector('//div[1]/p[2]/small').inner_text()
            if slots_string == 'No Spots Available':
                continue
            slots = slots_string.split()[0]

            unrefined_time = selector.query_selector('//div[1]/p[1]/small').inner_text()
            time = unrefined_time[0:2 + unrefined_time.rfind("PM")]
            day = selector.query_selector('//p').inner_text().split(",", 1)[0]
            element = selector.query_selector('.btn')

            have_booked = False
            if element.inner_text() == 'DETAILS':
                have_booked = True

            new_slot = BookingSlot(day, time, slots, index, have_booked, page.url)
            if duplicate_booking(new_slot, bookings_list):
                # Deletes things already recorded (e.g. South end 3:00 has booking but, North End 3:00 has booking too
                continue
            bookings_list.append(new_slot)

    def show_bookings():
        index = 0
        print(str(len(available_bookings)) + ' Bookings Available')
        for booking in available_bookings:
            already_booked = ''
            if booking.have_booked:
                already_booked = ' *Already Booked'

            print(str(index) + ") " + booking.name + already_booked)
            index += 1

#START of the program!!

    person = ''
    valid_input = False
    print("Who are we booking for?")
    while not valid_input:
        person = input()
        if person in people.keys():
            valid_input = True
        else:
            print('Enter a valid person')

    utor_username = people[person][0]
    utor_password = people[person][1]

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto('https://recreation.utoronto.ca/')

        login_link = get_selector('//*[@id="loginLink"]')
        login_link.click()

        login_utor = get_selector('//*[@id="section-sign-in-first"]/div[6]/div/button')
        login_utor.click()

        page.type('input[id = username]', utor_username)
        page.type('input[id = password]', utor_password)

        login_button = page.query_selector('[name="_eventId_proceed"]')
        login_button.click()

        page.wait_for_selector('.Menu-Item')
        activities = page.query_selector_all('.Menu-Item:has(>span.Menu-IconName)')
        swim = []
        for activity in activities:
            if 'Swim' in activity.inner_text():
                swim.append(activity)

        swim[0].click()
        swim_url = page.url

        '''north_end_button = get_selector('//*[@id="list-group"]/div[7]/div/div[2]/div[1]/h3')
        north_end_button.click()

        page.wait_for_selector('.caption')
        north_selectors = page.query_selector_all('.caption.program-schedule-card-caption')'''
        available_bookings = []
        get_bookings(swim_url, '//*[@id="list-group"]/a[7]/div/div[2]/div[1]/h3', available_bookings)
        #North End
        get_bookings(swim_url, '//*[@id="list-group"]/a[5]/div/div[2]/div[1]/h3', available_bookings)
        #South End

        show_bookings()

        valid_input = False
        print('Pick a Booking')
        while not valid_input:
            user_choice = input()
            if user_choice.isdigit():
                if int(user_choice) < len(available_bookings):
                    valid_input = True
                else:
                    print("Enter a number in the range of bookings")
            else:
                print('Enter a digit')

        picked_booking = available_bookings[int(user_choice)]
        page.goto(picked_booking.page_url)
        ind = str(picked_booking.index)
        reg_selector = '//*[@id="mainContent"]/div[2]/section/div/div[' + ind + ']/div/div/div[2]/button'
        register_button = get_selector(reg_selector)
        register_button.click()

        accept_button = get_selector('//*[@id="btnAccept"]')
        accept_button.click()

        add_cart = get_selector('//*[@id="mainContent"]/div[2]/form[2]/div[2]/button[2]')
        add_cart.click()

        checkout = get_selector('//*[@id="checkoutButton"]')
        checkout.click()

        proceed_checkout = get_selector('//*[@id="CheckoutModal"]/div/div/div[2]/button[2]')
        proceed_checkout.click()
        print("Just booked " + picked_booking.name)



        '''for selector in selectors:
            slots = int(selector.query_selector('//div[1]/small/span/small').inner_text().split()[0])
            if slots == 0:
                continue

            time = selector.query_selector('//div[1]/small').inner_text()
            day = selector.query_selector('//label').inner_text().split(",", 1)[0]
            element = selector.query_selector('.btn.btn-primary')

            new_slot = BookingSlot(day, time, slots, element, page.url)
            if duplicate_booking(new_slot, available_slots):
                #Deletes things already recorded (e.g. South end 3:00 has booking but, North End 3:00 has booking too
                continue
            available_slots.append(new_slot)'''

        '''
        
        page.wait_for_selector('.MuiButtonBase-root.MuiButton-root.MuiButton-outlined')
        new_assessment_button = page.query_selector('.MuiButtonBase-root.MuiButton-root.MuiButton-outlined')
        new_assessment_button.click()

        page.wait_for_selector('.sc-oTaAA.ggqipF')
        for index in range(len(answers)):
            num_child = index + answer_to_index(answers[index])
            all_radios = page.query_selector_all('.sc-oTaAA.ggqipF')
            all_radios[num_child].click()

        page.wait_for_selector('//*[@id="root"]/div/div/div/div[2]/main/div/div/div/div/div/button')
        submit_button = page.query_selector('//*[@id="root"]/div/div/div/div[2]/main/div/div/div/div/div/button')
        submit_button.click()
        
        
                def get_selector(selector):
            page.wait_for_selector(selector)
            return page.query_selector(selector)
        '''

        browser.close()


if __name__ == "__main__":
    main()


