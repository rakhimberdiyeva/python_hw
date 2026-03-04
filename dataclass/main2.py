from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from sqlalchemy.cyextension.processors import date_cls


# 1
# @dataclass
# class Id:
#     value: int
#
#     def __post_init__(self):
#         if self.value <= 0:
#             raise ValueError("id can not be negative")
#
# @dataclass
# class Product:
#     id: Id
#     name: str
#
# @dataclass
# class Warehouse:
#     id: Id
#     name: str
#     location: str
#
# @dataclass
# class Quantity:
#     value: int
#
#     def __post_init__(self):
#         if self.value < 0:
#             raise ValueError("quantity can not be negative")
#
# @dataclass
# class Stock:
#     id: Id
#     product: Product
#     warehouse: Warehouse
#     quantity: Quantity
#
#     def increase(self, amount):
#         self.quantity.value += amount
#
#     def decrease(self, amount):
#         if self.quantity.value - amount < 0:
#             raise ValueError("quantity can not be negative")
#         self.quantity.value -= amount
#
#
# class ReservationStatus(str, Enum):
#     pending = "pending"
#     confirmed = "confirmed"
#     cancelled = "cancelled"
#
# @dataclass
# class Reservation:
#     id: Id
#     stock: Stock
#     quantity: Quantity
#     status: ReservationStatus = ReservationStatus.pending
#
#     def confirm(self):
#         if self.status != ReservationStatus.pending:
#             raise ValueError("only scheduled reservations can be confirmed")
#         self.stock.decrease(self.quantity.value)
#         self.status = ReservationStatus.confirmed
#
#     def cancel(self):
#         if self.status == ReservationStatus.cancelled:
#             raise ValueError("reservations already cancelled")
#         self.status = ReservationStatus.cancelled
#
#
#
# @dataclass(frozen=True)
# class Movement:
#     id: Id
#     stock: Stock
#     quantity: Quantity
#     created_at: datetime = field(default_factory=datetime.now)
#
#
# product1 = Product(Id(1), "hdhd")
# warehouse1= Warehouse(Id(1), "kdkdk", "jhdhj")
# stock1 = Stock(Id(1), product1, warehouse1, Quantity(100))
# reservation1 = Reservation(Id(1), stock1, Quantity(20))
# print(reservation1)
# print(stock1.quantity)
# reservation1.confirm()
# print(reservation1)
# print(stock1.quantity)


# 2
# @dataclass
# class Id:
#     value: int
#
#     def __post_init__(self):
#         if self.value <= 0:
#             raise ValueError("id can not be negative")
#
# @dataclass
# class Patient:
#     id: Id
#     name: str
#
# @dataclass
# class Doctor:
#     id: Id
#     name: str
#
# @dataclass(frozen=True)
# class TimeSlot:
#     start_time: datetime
#     end_time: datetime
#
#     def __post_init__(self):
#         if self.start_time >= self.end_time:
#             raise ValueError("end time must be later than start time")
#
#
# class AppointmentStatus(str, Enum):
#     scheduled = "scheduled"
#     completed = "completed"
#     cancelled = "cancelled"
#
#
# @dataclass
# class Bookings:
#     bookings_list: list = field(default_factory=list)
#
# bookings = Bookings()
#
# @dataclass
# class Appointment:
#     id: Id
#     doctor: Doctor
#     patient: Patient
#     time: TimeSlot
#     status: AppointmentStatus = AppointmentStatus.scheduled
#
#     def __post_init__(self):
#         for b in bookings.bookings_list:
#             if not (self.time.end_time <= b.time.start_time or self.time.start_time >= b.time.end_time):
#                 raise ValueError("already booked")
#         bookings.bookings_list.append(self)
#
#     def complete(self):
#         if self.status != AppointmentStatus.scheduled:
#             raise ValueError("only scheduled appointments can be completed")
#         self.status = AppointmentStatus.completed
#
#
#     def cancel(self):
#         if self.status != AppointmentStatus.scheduled:
#             raise ValueError("only scheduled appointments can be cancelled")
#         self.status = AppointmentStatus.cancelled
#
#
# @dataclass(frozen=True)
# class Diagnosis:
#     name: str
#     appointment: Appointment
#
# @dataclass(frozen=True)
# class Prescription:
#     medication: str
#     dose: str
#     appointment: Appointment
#
#
# patient1 = Patient(
#     Id(1),
#     "patient1"
# )
#
# doctor1 = Doctor(
#     Id(1),
#     "doctor1"
# )
#
# time = TimeSlot(datetime(2026, 3, 1, 13, 00, 00), datetime(2026, 3, 1, 14, 00, 00))
# time2 = TimeSlot(datetime(2026, 3, 1, 13, 00, 00), datetime(2026, 3, 1, 14, 00, 00))
# time3 = TimeSlot(datetime(2026, 3, 1, 15, 00, 00), datetime(2026, 3, 1, 16, 00, 00))
#
# appoinment1 = Appointment(
#     Id(1),
#     doctor1,
#     patient1,
#     time
# )
# print(bookings.bookings_list)
# diagnosis = Diagnosis("nff", appoinment1)
# prescription = Prescription("jjk", "jdkla", appoinment1)
# appoinment1.cancel()



# 3
# @dataclass
# class Id:
#     value: int
#
#     def __post_init__(self):
#         if self.value <= 0:
#             raise ValueError("id can not be negative")
#
# @dataclass(frozen=True)
# class FlightNumber:
#     number: str
#
#     def __post_init__(self):
#         if len(self.number) < 3:
#             raise ValueError("flight number should be at least 3 symbols")
#
# @dataclass
# class Flight:
#     id: Id
#     number: FlightNumber
#     leave_from: str
#     leave_to: str
#     bookings: list = field(default_factory=list)
#
# @dataclass(frozen=True)
# class Seat:
#     id: Id
#     number: str
#
# class Currency(str, Enum):
#     usd = "usd"
#     uzs = "uzs"
#     rub = "rub"
#
# @dataclass(frozen=True)
# class Fare:
#     amount: float
#     currency: Currency
#
# @dataclass
# class Passenger:
#     id: Id
#     name: str
#
# class FlightStatus(str, Enum):
#     new = "new"
#     confirmed = "confirmed"
#     cancelled = "cancelled"
#
# @dataclass
# class Booking:
#     id: Id
#     passenger: Passenger
#     flight: Flight
#     seat: Seat
#     status: FlightStatus = FlightStatus.new
#
#     def __post_init__(self):
#         for booking in self.flight.bookings:
#             if booking.seat == self.seat and booking.flight == self.flight:
#                 raise ValueError("seat already booked")
#
#
#     def confirm(self):
#         if self.status != FlightStatus.new:
#             raise ValueError("only scheduled bookings can be confirmed")
#         self.status = FlightStatus.confirmed
#         self.flight.bookings.append(self)
#
#     def cancel(self):
#         if self.status == FlightStatus.cancelled:
#             raise ValueError("booking already cancelled")
#         self.status = FlightStatus.cancelled
#
#
# @dataclass
# class Ticket:
#     id: Id
#     booking: Booking
#     fare: Fare
#
# flight1 = Flight(Id(1), FlightNumber("bhdhsd"), "hjdjh", "jsdjh")
# passenger1 = Passenger(Id(1), "kjj")
# booking1 = Booking(
#     Id(1),
#     passenger1,
#     flight1,
#     Seat(Id(1), "11"),
# )
# booking1.confirm()
# print(booking1.status)
# print(flight1.bookings)
# booking2 = Booking(
#     Id(2),
#     passenger1,
#     flight1,
#     Seat(Id(1), "11"),
# )