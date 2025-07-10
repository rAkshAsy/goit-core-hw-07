from functions import interaction_comands as ic
from functions.address_book import AddressBook

def main():
    msg = '''BOT COMMANDS LIST:
///   hello
///   add [name] [phone]
///   change [name] [old_phone] [new_phone]
///   delete [name]
///   all OR phone [name]
///   add-birthday [name] [DD.MM.YYYY]
///   show-birthday [name]
///   birthdays
///   exit OR close'''

    book = AddressBook()

    while True:
        user_input = input('Enter command: ')

        input_tuple = ic.parce_input(user_input)
        cmd = input_tuple[0]
        argument_list = input_tuple[1]

        match cmd.casefold():

            case "hello":
                print(ic.greeting())

            case 'exit' | 'close':
                break

            case 'add':
                print(ic.add_contact(argument_list, book))

            case 'delete':
                print(ic.delete_contact(argument_list, book))

            case 'all':
                print(book)

            case 'phone':
                print(ic.show_phone(argument_list, book))

            case 'change':
                print(ic.change_contact(argument_list, book))

            case 'add-birthday':
                print(ic.add_birthday(argument_list, book))

            case 'show-birthday':
                print(ic.show_birthday(argument_list, book))

            case 'birthdays':
                print(ic.birthdays(argument_list, book))

            case 'help':
                print(msg)

            case _:
                print('Something went wrong. You can view all available commands using the command: help')



if __name__ == "__main__":
    main()
