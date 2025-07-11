import re
from collections import UserDict
from datetime import date, datetime, timedelta

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value: str):
        super().__init__(value)
        self.value = self.value.casefold()
    
    def __str__(self):
        return self.value.capitalize()

class Phone(Field):
    def __init__(self, value: str):
        if not len(value) == 10 or not value.isdigit():
            raise ValueError('Invalid phone number.')
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value):
        date_pattern = r'^\d{2}\.\d{2}\.\d{4}$'
        try:
            if re.match(date_pattern, value):
                self.value = value
            else:
                raise ValueError()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
                

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone: str) -> None:
        obj_phone = Phone(phone)
        if obj_phone:
            self.phones.append(obj_phone)
    
    def remove_phone(self, phone: str) -> None:
        removed_phone = self.find_phone(phone)
        if removed_phone:
            self.phones.remove(removed_phone)

    def find_phone(self, phone: str) -> Phone:
        try:
            finded_phone = [p_obj for p_obj in self.phones if p_obj.value == phone]
            return finded_phone[0]
        except ValueError:
            return None
        except IndexError:
            return None
        
    def edit_phone(self, old_phone, new_phone) -> None:
        if self.find_phone(old_phone):
            self.add_phone(new_phone)
            self.remove_phone(old_phone)
        else:
            raise ValueError('Incorect arguments for self.edit_phone() method.')

    def add_birthday(self, value: str):
        birthday_obj = Birthday(value)
        if birthday_obj:
            self.birthday = birthday_obj

    def __str__(self):
        name = self.name.value.capitalize()
        if self.phones:
            return f"Contact name: {name}, birthday: {self.birthday}, phones: {', '.join([p.value for p in self.phones])}"
        return f'Contact name: {self.name.value}, birthday: {self.birthday}, phones: There`s no phones'
        
    

class AddressBook(UserDict):
    def add_record(self, record: Record):
        key = record.name.value
        if key not in self.data:
            self.data[key] = record
    
    def delete(self, name: str) -> bool:
        if name in self.data:
            del self.data[name]
            return True
        return False
           
    def find(self, name: str):
        search_name = name.casefold()
        return self.data[search_name] if search_name in self.data else None
    
    def get_upcoming_birthdays(self, days=7):
        upcoming_birthdays = []
        today = date.today()

        for _, contact in self.data.items():
            if contact.birthday:
                user_b_day = datetime.strptime(contact.birthday.value, '%d.%m.%Y')
                birthday_this_year = user_b_day.replace(year=today.year).date()
                if birthday_this_year < today:
                    birthday_this_year = user_b_day.replace(year=today.year+1).date()
            
                if 0 <= (birthday_this_year - today).days <= days:
                    if birthday_this_year.weekday() == 5:
                        birthday_this_year += timedelta(days=2)
                    elif birthday_this_year.weekday() == 6:
                        birthday_this_year += timedelta(days=1)
                
                    congratulation_date_str = birthday_this_year.strftime("%d.%m.%Y")
                    upcoming_birthdays.append({"name": contact.name.value.capitalize(), "congratulation_date": congratulation_date_str})
        return upcoming_birthdays
    
    def __str__(self):
        underline = f'\n{'-'*50}\n'
        result = 'Your AddressBook:' + underline
        if self.data:
            for _, record in self.data.items():
                result += f'Contact name: {record.name}, '
                if record.birthday:
                    result += f'Birthday: {record.birthday}, '
                if not record.phones:
                    result += f'phones: There`s no phones' + underline
                else:
                    p_list = [p.value for p in record.phones]
                    result += f'phones: {', '.join(p_list)}' + underline
        else:
            result += 'Your address book is empty!' + underline
        return result


if __name__ == "__main__":

    book = AddressBook()

    names = ['Alex', 'Bill', 'Jane', 'Criss', 'Mary']
    b_days = ['10.07.2000', '08.07.2000', '03.08.1995', '12.07.1980', '17.07.2000']
    for name, b_day in zip(names, b_days):
        rec = Record(name)
        rec.add_birthday(b_day)
        book.add_record(rec)

    print('###'*40)
    print(book.get_upcoming_birthdays())
    print('###'*40)
