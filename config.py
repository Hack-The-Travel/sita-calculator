# -*- coding: utf-8 -*-
import os

cwd = os.path.dirname(os.path.abspath(__file__))

sita = {
    'pos': {
        'gateway': 'https://sws.qa.sita.aero/sws/',
        'certificate': '/'.join([cwd, 'sita_keys/cert.pem']),
        'private_key': '/'.join([cwd, 'sita_keys/key.pem']),
        'ERSP_UserID': 'ROV901/1ROV1AS',
        'AgentSine': '4499/4499W',
        'PseudoCityCode': 'ROV901',
        'AgentDutyCode': '115',
        'ISOCountry': 'RU',
        'AirlineVendorID': 'S7',
        'AirportCode': 'ROV',
        'AXIRequestorID': 'xdfkd-9ejdo-ofkdo-slnc8',
    },
    'dumps_dir': '/tmp/sitaclient',
}


class BaseConfig:
    """Base configuration."""
    DEBUG = False


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True
