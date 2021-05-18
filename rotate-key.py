#!/usr/bin/env python

import hvac
client = hvac.Client()
client.secrets.transit.rotate_key(name='jwt')
