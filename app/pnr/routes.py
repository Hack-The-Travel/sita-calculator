# -*- coding: utf-8 -*-
from flask import render_template
from . import pnr
from lxml import etree
from config import sita as sita_config
from sitaclient import SitaClient


@pnr.route('/pnr/<pnr_id>', methods=['GET'])
def price_pnr(pnr_id):
    sita = SitaClient(
        pos=sita_config['pos'],
        dumps_dir=sita_config['dumps_dir'] if 'dumps_dir' in sita_config else None
    )
    pnr_response = sita.read_pnr(pnr_id)
    ns = {'common': ''}
    if 'common' in pnr_response.nsmap:
        ns['common'] = pnr_response.nsmap['common']
    segments = pnr_response.findall('.//common:OriginDestinationOption', namespaces=ns)
    itinerary = list()
    for segment in segments:
        itinerary.append({
            'MarketingAirline': 'S7',
            'FlightNumber': 99,
            'DepartureAirport': 'OVB',
            'ArrivalAirport': 'DME',
            'DepartureDateTime': '2017-05-20T01:00:00',
            'ArrivalDateTime': '2017-05-20T07:00:00',
            'ResBookDesigCode': 'S',
        })
    context = {
        'pnr_id': pnr_id,
        'pnr': etree.tostring(pnr_response, pretty_print=True),
    }
    return render_template('pnr.html', **context)
