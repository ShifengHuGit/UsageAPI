# coding: utf-8
# Copyright (c) 2016, 2020, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl 
# or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

import requests
import sys
import click
from oci.config import from_file
from oci.signer import Signer

def loadConfig(ProfileName):
    click.echo('Using the Profile: %s' % ProfileName)
    try:
        config = from_file(profile_name=ProfileName)
    except:
        click.echo('Not Found for the  Profile: %s, Please check the profile in config file.' % ProfileName)
        sys.exit(0)
    return config

config=loadConfig(sys.argv[1])

auth = Signer(
tenancy=config['tenancy'],
user=config['user'],
fingerprint=config['fingerprint'],
private_key_file_location=config['key_file'],
pass_phrase=config['pass_phrase']
)

Region=config['region']
endpoint = 'https://usageapi.'+Region+'.oci.oraclecloud.com/20200107/usage'
#print(endpoint)
body = {
"granularity":"DAILY",
 "tenantId":config['tenancy'],
 "timeUsageEnded":"2020-07-10T00:00:00.000Z",
 "timeUsageStarted":"2020-07-01T00:00:00.000Z",
 "groupBy":[
     "compartmentName",
     "compartmentDepth"
 ],
 "filter":
    {
    "operator":"AND",
    "dimensions":[],
    "tags":[],
    "filters":[
        {
            "operator":"OR",
            "dimensions":[
                {
                    "key":"compartmentName",
                    "value":"ShiF"
                },
                {
                    "key":"compartmentName",
                    "value":"Evan"
                }
                ],
                "tags":[],
                "filters":[]
        }
        ]
    },
"compartmentDepth":6,
"queryType":"COST"

}

response = requests.post(endpoint, json=body, auth=auth)
response.raise_for_status()

print(response.json())
