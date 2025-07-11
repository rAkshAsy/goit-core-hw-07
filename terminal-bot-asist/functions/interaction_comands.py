from .address_book import AddressBook, Record
def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Enter corect arguments for the command. You can use 'help' to know all commands."
        except KeyError:
            return "Sorry, this name is already taken. Please, enter another name."
        except IndexError:
            return "There`s no contact with this name. Please, enter another name."

    return inner


@input_error
def parce_input(user_input:str) -> tuple:
    cmd, *args = user_input.split(' ')
    cmd = cmd.strip().casefold()
    return cmd, args


@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        record.add_phone(phone)
        book.add_record(record)
        message = "Contact added."
    else:
        record.add_phone(phone)
    return message


@input_error
def show_phone(args_list: list, book: AddressBook) -> str:
    name, *_ = args_list
    contact = book.find(name)
    if contact:
        msg = f'Name: {contact.name}'
        if contact.phones:
            p_list = [tel.value for tel in contact.phones]
            msg += f', phones: {', '.join(p_list)}'
        return msg
    raise IndexError


@input_error
def change_contact(args_list: list, book: AddressBook) -> str:
    name, old_phone, new_phone, *_ = args_list
    contact = book.find(name)
    if contact:
        contact.edit_phone(old_phone, new_phone)
        return f'Contact updated: {contact.name} {new_phone}'
    raise IndexError()

        
@input_error
def add_birthday(args: list, book: AddressBook):
    name, b_day, *_ = args
    contact = book.find(name)
    if contact:
        contact.add_birthday(b_day)
        return f'Contact {contact.name} updated. You add birthday: {contact.birthday}'
    else:
        raise IndexError()


@input_error
def delete_contact(args, book: AddressBook) -> str:
    name, *_ = args
    if book.delete(name):
        return f'Contact {name.capitalize()} deleted.'
    raise IndexError()


@input_error
def show_birthday(args: list, book: AddressBook):
    name, *_ = args
    contact = book.find(name)
    if contact:
        return f'Name: {contact.name}, birthday: {contact.birthday}'
    raise IndexError()
\
@input_error
def birthdays(args: list, book: AddressBook):
    result = 'Upcoming birthdays:'
    congrats_list = book.get_upcoming_birthdays()

    if congrats_list:
        for cont in congrats_list:
            result += f'\nName: {cont['name']} - {cont['congratulation_date']}'
    else:
        result += '\nThere`s no birthdays!'
    return result


def greeting() -> str:
    return "Hi! How can I help you?"
