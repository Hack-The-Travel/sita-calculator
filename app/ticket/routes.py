# -*- coding: utf-8 -*-
from flask import render_template
from . import ticket_blueprint


@ticket_blueprint.route('/ticket/<ticket_number>', methods=['GET'])
def ticket_price(ticket_number):
    context = dict()
    return render_template('ticket.html', **context)
