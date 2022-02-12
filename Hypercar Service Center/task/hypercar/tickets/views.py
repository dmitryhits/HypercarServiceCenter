from django.views import View
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
import numpy as np

service_links = ['change_oil', 'inflate_tires', 'diagnostic']
services = ['Change oil', 'Inflate tires', 'Get diagnostic']
line_of_cars = {k: [] for k in service_links}
next_pressed = []
current_customer = []


class WelcomeView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('<h2>Welcome to the Hypercar Service!</h2>')


class MenuView(View):
    menu = list(zip(service_links, services))

    def get(self, request, *args, **kwargs):
        return render(request, 'tickets/menu.html', {'menu': self.menu})


class OperatorsView(View):

    def get(self, request, *args, **kwargs):
        operator_menu = [(service, len(line_of_cars[link])) for service, link in zip(services, line_of_cars)]
        return render(request, 'tickets/operator_menu.html', context={'operator_menu': operator_menu})

    def post(self, request, *args, **kwargs):
        next_pressed.append(1)
        return redirect('/next')


class NextView(View):
    processing_ticket = 0

    def get(self, request, *args, **kwargs):
        if next_pressed:
            next_pressed.clear()
            current_customer.clear()
            for tickets in line_of_cars.values():
                if tickets:
                    current_customer.append(tickets.pop(0))
                    break

        if current_customer:
            self.processing_ticket = current_customer[0]

        return render(request, 'tickets/next_ticket.html', context={'next_ticket': self.processing_ticket})


class TicketView(View):

    waiting_times = np.asarray([2, 5, 30])

    def get(self, request, *args, **kwargs):
        service = kwargs['service']
        rank = service_links.index(service)

        n_customers = np.asarray([len(n) for n in line_of_cars.values()])
        waiting_time = sum(self.waiting_times[:rank + 1] * n_customers[:rank + 1])

        ticket_number = sum(n_customers) + 1
        line_of_cars[service].append(ticket_number)
        return render(request, 'tickets/ticket.html',
                      context={'ticket_number': ticket_number, 'waiting_time': waiting_time})

