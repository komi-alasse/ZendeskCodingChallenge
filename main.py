import requests, json, itertools
from dotenv import dotenv_values

url = dotenv_values('credentials.env')['URL']
user = dotenv_values('credentials.env')['USER'] + '/token'
key = dotenv_values('credentials.env')['API_KEY']

all_tickets  = {}
ticket_ids = {}

def show_menu():
    response = ''
    while response != "q":
        print("------------------------- MENU -------------------------")
        print('\nPlease choose from one of three options.')
        print('* Press 1 to view all tickets.')
        print('* Press 2 to view a single ticket.')
        print('* Press \'q\' to quit.\n')
    
        response = input()

        if response == "q":
            print('Thanks for using the ticket viewer!\n')
            exit()
        
        elif response == '1':
            display_all_tickets()
        elif response == '2':
            get_single_ticket()
        
def display_all_tickets():

    if len(all_tickets) > 25:
        num_pages = len(all_tickets) // 25 + 1
    else:
        num_pages = 1

    response = ''
    current_page = 1
    valid_response = True

    while response != 'b':
        if valid_response:
            max_per_page = len(all_tickets) % 25 if current_page == num_pages else 25
            for i in range(0, max_per_page):
                ticket = all_tickets[i + (25 * (current_page - 1))]
                print('Ticket #' + str(ticket['id']) + ': \'' + ticket['subject'] + '\' last updated on ' + ticket['updated_at'][0:10])
                i += 1
            
            first = 1 + 25 * (current_page - 1)
            last = first + max_per_page - 1
            
            print('Viewing tickets ' + str(first) + '-' + str(last) + ' of ' + str(len(all_tickets)) + 
                ', page ' + str(current_page) + ' of ' + str(num_pages) + '\n')
            
            response = input('Enter the number page you would like to view or type \'b\' to go back to the menu:')
            
            if response == 'b':
                return

            if is_valid_response(response, num_pages):
                current_page = int(response)
                valid_response = True
            else:
                valid_response = False
            
            return len(all_tickets)

def get_single_ticket():
    
    response = ''
    while response != 'b':
        response = input('Enter a ticket number or press \'b\' to go back to the menu: ')

        if response == 'b':
            return

        if not response.isnumeric():
            response = input('Please only enter a numerical value: ')

        if int(response) in ticket_ids:
                ticket_number = int(response)
                endpoint = '/users/' + str(ticket_ids[ticket_number]['requester_id']) + '.json'
                display_ticket_information(ticket_number, endpoint)
        else:
            response = input('Unable to find that ticket. Please enter a valid ticket number: ')

def display_ticket_information(ticket_number, endpoint): 
    response = requests.get(url + endpoint, auth=(user, key))
    
    if response.status_code != 200:
        failed_response_handler(response.status_code)

    name = response.json()['user']['name']

    print("-----------------------------------------------------------")
    print(f'Ticket ID #{ticket_number}')
    print('\nRequestor: ' + name)
    print('Subject: ' + ticket_ids[ticket_number]['subject'])
    print('\nDescription: ' + ticket_ids[ticket_number]['description'] + '\n')
    print("-----------------------------------------------------------")

def is_valid_response(response, num_pages):
    if not response.isnumeric():
        print("Please enter a page number.")
        return False 
    elif int(response) > num_pages or int(response) < 1:
        print("Please enter a number within the range of 0 to number of pages")
        return False
    
    return True
 

def store_tickets(offset, tickets):
    for i, ticket in enumerate(tickets):
        index = i + offset * 100
        all_tickets[index] = ticket
        ticket_ids[ticket['id']] = ticket



def failed_response_handler(status):
    print('Status:', status, "Issue with request, exiting.")
    return -1
    exit()

    
# Collects all tickets for the current account. 
def get_tickets(url, user, key):
    url += "/tickets.json?page[size]=100"

    response = requests.get(url, auth=(user, key))

    if response.status_code != 200:
        failed_response_handler(response.status_code)


    data = response.json()
    offset = 0
    store_tickets(offset, data['tickets'])

    while data['links']['next'] != None:
        offset += 1
        response = requests.get(data['links']['next'], auth=(user,key))
        
        if response.status_code != 200:
             failed_response_handler(response.status_code)

        data = response.json()
        store_tickets(offset, data['tickets'])

def main():
    get_tickets(url, user, key)
    
    print("Welcome to the ticket viewer!")
    response = ''

    while response != 'q':
        response = input("\nType \'m\' to view the menu or \'q\' to quit.\n")

        if response == 'm': 
            show_menu()

    print("Thanks for using the ticket viewer!")

if __name__ == "__main__":
    main()