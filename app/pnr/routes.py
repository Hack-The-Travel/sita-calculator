# -*- coding: utf-8 -*-
from flask import render_template
from . import pnr_blueprint
from lxml import etree
from config import sita as sita_config
from sitaclient import SitaClient
from app.utils import cleanup_nsmap


def get_itinerary(pnr_response):
    nsmap = cleanup_nsmap(pnr_response.nsmap)
    segments = pnr_response.findall('.//common:OriginDestinationOption/common:FlightSegment', namespaces=nsmap)
    itinerary = list()
    for segment in segments:
        itinerary.append({
            'MarketingAirline': 'S7',
            'FlightNumber': segment.attrib['FlightNumber'],
            'DepartureAirport': segment.find('.//common:DepartureAirport', namespaces=nsmap).attrib['LocationCode'],
            'ArrivalAirport': segment.find('.//common:ArrivalAirport', namespaces=nsmap).attrib['LocationCode'],
            'DepartureDateTime': segment.attrib['DepartureDateTime'],
            'ArrivalDateTime': segment.attrib['ArrivalDateTime'],
            'ResBookDesigCode': segment.find('.//common:BookingClassAvail', namespaces=nsmap)\
                .attrib['ResBookDesigCode'],
        })
    return itinerary


def get_price_breakdowns(price_response, ptcs=('ADT', 'CNN', 'INF',)):
    price_fare_breakdowns = price_response['ADT']['PTC_FareBreakdowns']
    nsmap = cleanup_nsmap(price_fare_breakdowns.nsmap)
    price = dict()
    for ptc in ptcs:
        if ptc not in price_response:
            continue
        price_fare_breakdowns = price_response[ptc]['PTC_FareBreakdowns']
        taxes = list()
        for tax in price_fare_breakdowns.findall('.//ota:Taxes/ota:Tax', namespaces=nsmap):
            taxes.append({
                'code': tax.attrib['TaxCode'],
                'amount': tax.attrib['Amount'],
            })
        price[ptc] = {
            'amount': price_fare_breakdowns.find('.//ota:BaseFare', namespaces=nsmap).attrib['Amount'],
            'taxes': taxes,
        }
    return price


@pnr_blueprint.route('/pnr/<pnr_id>', methods=['GET'])
def price_pnr(pnr_id):
    sita = SitaClient(
        pos=sita_config['pos'],
        dumps_dir=sita_config['dumps_dir'] if 'dumps_dir' in sita_config else None
    )
    pnr_response = sita.read_pnr(pnr_id)
    itinerary = get_itinerary(pnr_response)
    price_response = sita.price(itinerary, format='xml')
    price = get_price_breakdowns(price_response)
    context = {
        'pnr_id': pnr_id,
        'price': price,
        'price_response_text': etree.tostring(price_response['ADT']['PTC_FareBreakdowns'], pretty_print=True),
        'pnr_response_text': etree.tostring(pnr_response, pretty_print=True),
    }
    return render_template('pnr.html', **context)
