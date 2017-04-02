# -*- coding: utf-8 -*-
from flask import Blueprint

pnr = Blueprint('pnr', __name__)

from . import routes
