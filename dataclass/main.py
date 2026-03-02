from dataclasses import dataclass, field
from datetime import date, time, datetime
from enum import Enum



# TODO: DataClass
# это удобный класс для хранения данных
# без необходимости писать много шаблонного кода



# class Student:
#     def __init__(self, id: int, name: str, group_id: int):
#         self.id = id
#         self.name = name
#         self.group_id = group_id
#
#     def __repr__(self):
#         return f"student name {self.name}"
#
# s1 = Student(1, name="malika", group_id=1)
# print(s1)
#
#
# @dataclass
# class Student:
#     id: int
#     name: str
#     group_id: int
#
# s1 = Student(1, name="malika", group_id=1)
# print(s1)
#
# s1.group_id = 2
# print(s1)


#  говорит о том что нельзя потом изменять объект
@dataclass(frozen=True)
class Id:
    value: int

    # если нужно что то проверить после создания то используем
    def __post_init__(self):
        if self.value <= 0:
            raise ValueError("id should be positive")

id1 = Id(1)
# id1.value = 5


@dataclass(frozen=True)
class Name:
    value: str

    def __post_init__(self):
        if len(self.value) < 3 or len(self.value) > 512:
            raise ValueError("name should be from 3 to 512 symbols")


@dataclass(frozen=True)
class Age:
    value: int

    def __post_init__(self):
        if self.value < 0 and self.value > 200:
            raise ValueError("age should be from 0 to 200")


@dataclass
class Student:
    id: Id
    name: Name
    age: Age

# s2 = Student(Id(-1), "sss", 12)
s3 = Student(Id(1), Name("sss"), Age(2))
# s3.id = Id(-2)
print(s3)


# value object - объект который
# 1. определяется своим значением
# 2. не изменяемый
# 3. сравниваем по содержанию
# 4. нет ид


# Value Object
@dataclass(frozen=True)
class TimeSlot:
    day: date
    start_time: time
    end_time: time


# Entity (сущность) - это объект который
# 1. имеет ид
# 2. может меняться
# 3. сущность это кто а не что
@dataclass
class Lesson:
    id: Id
    slot: TimeSlot


# value object: email, money, daterange
# entity: student, group, lesson, user


#################################################################


@dataclass(frozen=True)
class Id:
    value: int

    def __post_init__(self):
        if self.value <= 0:
            raise ValueError("id should be positive")

class Currency(str, Enum):
    usd = "usd"
    uzs = "uzs"
    rub = "rub"

class TransactionType(str, Enum):
    income = "income"
    outcome = "outcome"

@dataclass(frozen=True)
class Money:
    amount: float
    currency: Currency

    def __post_init__(self):
        if self.amount < 0:
            raise ValueError("money can not be negative")

@dataclass(frozen=True)
class Transaction:
    amount: Money
    type: TransactionType
    created_at: datetime = field(default_factory=datetime.now)

@dataclass
class Wallet:
    id: Id
    currency: Currency
    __transactions: list[Transaction] = field(default_factory=list)

    @property
    def balance(self):
        incomes = [
            transaction.amount.amount
            for transaction in self.__transactions
            if transaction.type == TransactionType.income
        ]

        outcomes = [
            transaction.amount.amount
            for transaction in self.__transactions
            if transaction.type == TransactionType.outcome
        ]

        return sum(incomes) - sum(outcomes)


    def add_transaction(self, transaction: Transaction):
        if self.currency != transaction.amount.currency:
            raise ValueError("Transaction is impossible")
        if transaction.type == TransactionType.outcome and self.balance < transaction.amount.amount:
            raise ValueError("Not enough money")
        self.__transactions.append(transaction)

    @property
    def transactions(self) -> list[Transaction]:
        return self.__transactions

@dataclass
class User:
    id: Id
    wallets: list[Wallet] = field(default_factory=list)

    def add_wallet(self, wallet: Wallet):
        self.wallets.append(wallet)


user1 = User(Id(1))
print(user1)

uzcard = Wallet(Id(1), Currency.uzs)
user1.add_wallet(uzcard)
print(user1.wallets)

user2 = Transaction(
    amount=Money(amount=200000, currency=Currency.uzs),
    type=TransactionType.income
)

user3 = Transaction(
    amount=Money(amount=300000, currency=Currency.uzs),
    type=TransactionType.income
)

user1.wallets[0].add_transaction(user2)
user1.wallets[0].add_transaction(user3)
print(user1.wallets[0].balance)

purchase = Money(40000, Currency.uzs)
user1.wallets[0].add_transaction(
    Transaction(
        amount=purchase,
        type=TransactionType.outcome
    )
)
print(user1.wallets[0].balance)
print(user1.wallets[0].transactions)


##########################################################################

@dataclass(frozen=True)
class Id:
    value: int

    def __post_init__(self):
        if self.value <= 0:
            raise ValueError("id should be positive")

class RoomType(str, Enum):
    standard = "standard"
    deluxe = "deluxe"
    suite = "suite"

@dataclass(frozen=True)
class Room:
    number: int
    type: RoomType

class Currency(str, Enum):
    usd = "usd"
    uzs = "uzs"
    rub = "rub"

@dataclass(frozen=True)
class Money:
    amount: float
    currency: Currency

    def __post_init__(self):
        if self.amount < 0:
            raise ValueError("money can not be negative")


@dataclass(frozen=True)
class DateRange:
    start_time: date
    end_time: date

    def __post_init__(self):
        if self.start_time >= self.end_time:
            raise ValueError("end time must be later than start time")


class BookingStatus(str, Enum):
    new = "new"
    confirmed = "confirmed"
    cancelled = "cancelled"


@dataclass
class Booking:
    id: Id
    room: Room
    price_per_night: Money
    date_range: DateRange
    status: BookingStatus = BookingStatus.new

    def confirm(self):
        if self.status == BookingStatus.confirmed:
            raise ValueError("booking already confirmed")
        self.status = BookingStatus.confirmed

    def cancel(self):
        if self.status == BookingStatus.cancelled:
            raise ValueError("booking already cancelled")
        self.status = BookingStatus.cancelled

@dataclass
class User:
    id: Id
    bookings: list[Booking] = field(default_factory=list)

    def add_booking(self, booking: Booking):
        self.bookings.append(booking)



