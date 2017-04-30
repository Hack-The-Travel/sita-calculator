# -*- coding: utf-8 -*-
from flask import Blueprint

ticket_blueprint = Blueprint('ticket', __name__)

from . import routes
