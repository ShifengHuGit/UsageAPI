# coding: utf-8
# Copyright (c) 2016, 2020, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl
# or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

import requests
import sys
import click
import oci
import traceback
import datetime

def loadConfig(ProfileName):
    click.echo('Using the Profile: %s' % ProfileName)
    try:
        config = oci.config.from_file(profile_name=ProfileName)
    except:
        click.echo('Not Found for the  Profile: %s, Please check the profile in config file.' % ProfileName)
        sys.exit(0)
    return config

NowDate = datetime.date.today() 
#print(NowData)
td = datetime.timedelta(days=7)
last7days = datetime.date.today() - td
#click.echo("Today: %s  last7: %s" % (NowDate,  last7days))

Time_Started = str(last7days)+"T00:00:00.000Z"
Time_Ended = str(NowDate)+"T00:00:00.000Z"

config=loadConfig(sys.argv[1])
#print(config)
UsageAPI=oci.usage_api.UsageapiClient(config)
Detail = {
"granularity":"DAILY",
 "tenantId":config['tenancy'],
 "timeUsageEnded":Time_Ended,
 "timeUsageStarted":Time_Started,
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
                    "value":"Evan"
               # },
               # {
               #     "key":"compartmentName",
               #     "value":"Evan"
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

#response=UsageAPI.request_summarized_usages(Detail)
#print(response.data)
#Data=response.data
#print(Data["group_by"][0])
#ItemList=Data.items.sort(key=lambada Data.items: Data.items.time_usage_started )
#print(ItemList)
try:
    response=UsageAPI.request_summarized_usages(Detail)
    #print(response.data)
    Data=response.data.items
    #print(Data.group_by)
    Data.sort(key=lambda x:x.time_usage_started)
    #print(Data.items[0].compartment_path)
    #ItemList=Data.items.sort()
    #print(ItemList)
    click.echo("-------------------------------------------------------------")
    for _Item in Data:
        if _Item.computed_amount :
            click.echo("Data Start: %s  Data End: %s" % (_Item.time_usage_started,  _Item.time_usage_ended)) 
            click.echo("Account: %s   fee: %.2f" % (_Item.compartment_name,  _Item.computed_amount)) 
            click.echo("-------------------------------------------------------------")
            #print(_Item.computed_amount)
         
 #   click.echo("%s  Total: %d" % ( C_Name, Fee_total))
except Exception as e:    
    print('Error')
    print(e)
  #  print 'repr(e):\t', repr(e)
