# -*- coding: utf-8 -*-
from flask import render_template
from . import ticket_blueprint
from lxml import etree
from config import sita as sita_config
from sitaclient import SitaClient
from app.utils import cleanup_nsmap


def get_ticket_price(ticket_response):
    nsmap = cleanup_nsmap(ticket_response.nsmap)
    total = float(ticket_response.find('.//fares:TotalFare', namespaces=nsmap).attrib['Amount'])
    fare_node = ticket_response.find('.//fares:EquivFare', namespaces=nsmap)
    if fare_node is None:
        fare_node = ticket_response.find('.//fares:BaseFare', namespaces=nsmap)
    fare_str = fare_node.attrib['Amount']
    if fare_str == 'NOFARE':
        fare = 0.0
    else:
        fare = float(fare_str)
    taxes = list()
    for tax in ticket_response.findall('.//fares:Taxes/fares:Tax', namespaces=nsmap):
        taxes.append({
            'code': tax.attrib['TaxCode'],
            'amount': float(tax.attrib['Amount']),
        })
    return {
        'total': total,
        'fare': fare,
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
        'taxes_amount': price['total'] - price['fare'],
        'taxes': price['taxes'],
        'ticket_response': etree.tostring(ticket_response, pretty_print=True),
    }
    return render_template('ticket.html', **context)
