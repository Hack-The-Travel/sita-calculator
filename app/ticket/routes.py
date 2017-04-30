# -*- coding: utf-8 -*-
from flask import render_template
from . import ticket_blueprint
from config import sita as sita_config
from sitaclient import SitaClient


@ticket_blueprint.route('/ticket/<ticket_number>', methods=['GET'])
def ticket_price(ticket_number):
    sita = SitaClient(
        pos=sita_config['pos'],
        dumps_dir=sita_config['dumps_dir'] if 'dumps_dir' in sita_config else None
    )
    price = sita.get_ticket_price(ticket_number)
    context = {
        'ticket_number': ticket_number,
        'total': price['total'],
        'fare': price['fare'],
        'taxes': price['taxes'],
    }
    return render_template('ticket.html', **context)
