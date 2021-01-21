from PIL import Image
from django.shortcuts import render, redirect
from pyzbar import pyzbar
from django.views.generic import CreateView

from .forms import TicketForm
from .models import Ticket

import asyncio
from tornado.platform.asyncio import AnyThreadEventLoopPolicy
from channels.db import database_sync_to_async


async def write_qr(ticket, qr_data):
    ticket.qr = qr_data
    await database_sync_to_async(ticket.save)()


async def write_photo(ticket, photo):
    ticket.photo = photo
    await database_sync_to_async(ticket.save)()


async def write_number(ticket, number):
    ticket.number = number
    await database_sync_to_async(ticket.save)()


class TicketCreateView(CreateView):
    model = Ticket
    form_class = TicketForm
    template_name = 'tickets_create.html'

    def post(self, request, *args, **kwargs):
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = Ticket.objects.create()

            data = pyzbar.decode(Image.open(request.FILES.get('qr')))
            qr_data = data[0].data.decode('utf-8')
            photo = request.FILES.get('photo')
            number = int(request.POST.get('number'))

            asyncio.set_event_loop_policy(AnyThreadEventLoopPolicy())
            event_loop = asyncio.get_event_loop()
            writers = [
                asyncio.ensure_future(write_qr(ticket, qr_data)),
                asyncio.ensure_future(write_photo(ticket, photo)),
                asyncio.ensure_future(write_number(ticket, number))
            ]
            event_loop.run_until_complete(asyncio.gather(*writers))

            return redirect('tickets:success')
        else:
            return render(request, 'tickets_create.html', {'form': TicketForm, 'errors': form.errors})


def success(request):
    return render(request, 'tickets_create_success.html')
