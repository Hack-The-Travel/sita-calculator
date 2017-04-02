# -*- coding: utf-8 -*-
from flask import render_template
from . import pnr


@pnr.route('/pnr/<pnr_id>', methods=['GET'])
def price_pnr(pnr_id):
    context = {
        'pnr_id': pnr_id,
    }
    return render_template('pnr.html', **context)
