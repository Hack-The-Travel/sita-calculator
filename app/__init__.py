# -*- coding: utf-8 -*-
import os
from flask import Flask

app = Flask(__name__)
app_settings = os.getenv(
    'APP_SETTINGS',
    'config.DevelopmentConfig'
)
app.config.from_object(app_settings)

from app.pnr import pnr
app.register_blueprint(pnr)
