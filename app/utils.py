# -*- coding: utf-8 -*-

"""
utils
~~~~~

This module provides utility functions that are used within sita-calculator
that are also useful for external consumption.
"""


def cleanup_nsmap(nsmap, empty_prefix='no-prefix'):
    """Makes new namespace mapping without empty prefix.

    :param nsmap: list of namespace declarations (prefix->URI mapping).
    :param empty_prefix: name for default namespace (no prefix).
    :return: new nsmap with named default namespace.

    Usage::

        >>> type(xml_response)
        <type 'lxml.etree._Element'>
        >>> xml_response.nsmap
        {
            None: 'http://sita.aero/SITA_RetrieveTicketByTicketNumber/4/0',
            'fares': 'http://sita.aero/fares/common/4/0',
            'SOAP-ENV': 'http://schemas.xmlsoap.org/soap/envelope/',
            'common': 'http://sita.aero/common/3/0',
            'ticketing': 'http://sita.aero/ticketing/common/3/0'
        }
        >>> xml_response.find('.//fares:PassengerFare', namespaces=xml_response.nsmap)
        ValueError: empty namespace prefix is not supported in ElementPath
        >>> cleanup_nsmap(xml_response.nsmap)
        {
            'no-prefix': 'http://sita.aero/SITA_RetrieveTicketByTicketNumber/4/0',
            'fares': 'http://sita.aero/fares/common/4/0',
            'SOAP-ENV': 'http://schemas.xmlsoap.org/soap/envelope/',
            'common': 'http://sita.aero/common/3/0',
            'ticketing': 'http://sita.aero/ticketing/common/3/0'
        }
        >>> xml_response.find('.//fares:PassengerFare', namespaces=cleanup(xml_response.nsmap))
        <Element {http://sita.aero/fares/common/4/0}PassengerFare at 0x10dab4fc8>
    """
    if empty_prefix in nsmap:
        raise LookupError("Prefix '%s' is already in use in namespace declarations. " % empty_prefix)
    clean = nsmap.copy()
    if None in clean:
        clean[empty_prefix] = clean.pop(None)
    return clean
