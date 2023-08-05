#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests, json


def get_poe_ports(auth):
    """
    Function to get list of poe ports from Aruba OS switch
    :param auth:  AOSSAuth class object returned by pyarubaoss.auth
    :return list of poe ports
    :rtype list
    """
    headers = {'cookie': auth.cookie}
    url_poe = "http://" + auth.ipaddr + "/rest/v3/poe/ports"
    try:
        r = requests.get(url_poe, headers=headers)
        poe_ports = json.loads(r.text)['port_poe']
        return poe_ports
    except requests.exceptions.RequestException as error:
        return "Error:\n" + str(error) + " get_poe_ports: An Error has occured"