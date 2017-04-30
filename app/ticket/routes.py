# -*- coding: utf-8 -*-
from flask import render_template
from . import ticket_blueprint
from config import sita as sita_config
from sitaclient import SitaClient


def get_ticket_price(ticket_response):
    ns = ticket_response.nsmap
    if None in ns:
        ns['ns'] = ns.pop(None)
    fare_breakdown = ticket_response.find('.//fares:PassengerFare', namespaces=ns)
    taxes_breakdown = fare_breakdown.findall('fares:Taxes/fares:Tax', namespaces=ns)
    taxes = list()
    for tax in taxes_breakdown:
        taxes.append({
            'code': tax.attrib['TaxCode'],
            'amount': tax.attrib['Amount'],
        })
    return {
        'total': fare_breakdown.find('fares:TotalFare', namespaces=ns).attrib['Amount'],
        'fare': fare_breakdown.find('fares:BaseFare', namespaces=ns).attrib['Amount'],
        'taxes': taxes,
    }


@ticket_blueprint.route('/ticket/<ticket_number>', methods=['GET'])
def ticket_price(ticket_number):
    sita = SitaClient(
        pos=sita_config['pos'],
        dumps_dir=sita_config['dumps_dir'] if 'dumps_dir' in sita_config else None
    )
    ticket_response = sita.read_ticket(ticket_number)
    price = get_ticket_price(ticket_response)
    context = {
        'ticket_number': ticket_number,
        'total': price['total'],
        'fare': price['fare'],
        'taxes': price['taxes'],
    }
    return render_template('ticket.html', **context)
