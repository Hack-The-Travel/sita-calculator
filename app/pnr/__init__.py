# -*- coding: utf-8 -*-
from flask import Blueprint

pnr_blueprint = Blueprint('pnr', __name__)

from . import routes
