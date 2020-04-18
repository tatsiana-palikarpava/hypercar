from django.views import View
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from collections import deque

QUEUE_D = deque()
QUEUE_I = deque()
QUEUE_C = deque()

class WelcomeView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('<h2>Welcome to the Hypercar Service!</h2>')

class MenuView(View):
    def get(self, request, *args, **kwargs):
        global DIAGNOSTIC
        global INFLATE_TIRES
        global CHANGE_OIL
        #return HttpResponse('<a target="_blank" href="/get_ticket/inflate_tires">Inflate tires</a> <a target="_blank" href="/get_ticket/change_oil">Change oil</a> <a target="_blank" href="/get_ticket/diagnostic">Diagnostic</a>')
        return render(request, "hypercar/menu.html")

class GetTicketView(View):
    def get(self, request, *args, **kwargs):
        request_type = str(request).split('/get_ticket/')[1]
        global QUEUE_D
        global QUEUE_I
        global QUEUE_C

        if request_type.startswith('diagnostic'):
            request_type = 'diagnostic'
            time = len(QUEUE_D) * 30 + len(QUEUE_I) * 5 + len(QUEUE_C) * 2
            QUEUE_D.append(len(QUEUE_D) + len(QUEUE_I) + len(QUEUE_C) + 1)
        elif request_type.startswith('inflate_tires'):
            request_type = 'inflate tires'
            time = len(QUEUE_I) * 5 + len(QUEUE_C) * 2
            QUEUE_I.append(len(QUEUE_D) + len(QUEUE_I) + len(QUEUE_C) + 1)
        elif request_type.startswith('change_oil'):
            request_type = 'change oil'
            time = len(QUEUE_C) * 2
            QUEUE_C.append(len(QUEUE_D) + len(QUEUE_I) + len(QUEUE_C) + 1)
        n = len(QUEUE_D) + len(QUEUE_I) + len(QUEUE_C)

        return render(request, "hypercar/get_ticket.html", {'request_type':request_type, 'number': n, 'wait_time': time})

class ProcessingView(View):
    def get(self, request, *args, **kwargs):
        global QUEUE_D
        global QUEUE_I
        global QUEUE_C

        d = len(QUEUE_D)
        i = len(QUEUE_I)
        c = len(QUEUE_C)
        return render(request, "hypercar/processing.html", {'d': d, 'i': i, 'c': c})

    def post(self, request, *args, **kwargs):
        global QUEUE_D
        global QUEUE_I
        global QUEUE_C

        if len(QUEUE_C) > 0:
            next = QUEUE_C.popleft()
            NextTicketView.next = next
        elif len(QUEUE_I) > 0:
            next = QUEUE_I.popleft()
            NextTicketView.next = next
        elif len(QUEUE_D) > 0:
            next = QUEUE_D.popleft()
            NextTicketView.next = next
        else:
            next = None
            NextTicketView.next = next
        return redirect("/next")

class NextTicketView(View):
    next = None
    def set_next(self, n):
        typenext = n
    def get(self, request, *args, **kwargs):
        return render(request, "hypercar/next_ticket.html", {'next': self.next})


