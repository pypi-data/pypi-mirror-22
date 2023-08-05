Installation
------------
# pip install servicenow_client


Usage examples
--------------

import servicenow_client

# Create object
# if empty_error is True, exception will be raised if query result is empty
obj = servicenow_client.servNow(instance=instance, user=user, password=password, empty_error=True)

# Create a new record
obj.create(table='incident', data={'short_description':'My Incident Ticket'})

# Update record(s) based on search condition
# searchList=['field', 'operator', 'value']
obj.update(table='incident', searchList=[['short_description','is','My Incident Ticket'], ['number','is not','INC0010022']], data={'state': '1'})

# Search for record(s) and display only 'number' and 'sys_id' from the results
$ if fields is not defined it will return all fiels in response
obj.search(table='incident', searchList=['short_description','is not empty'], fields='number,sys_id')

# Delete record(s) based on search condition
obj.delete(table='problem', searchList=['short_description','is','Problem Ticket'])

# Change state of record(s) based on search condition
obj.changeState(table='incident', searchList=['short_description','is','ISAN Problem 2'], state='In progress')

# Download a specific attachement or particular type of attachement related to record(s) based on search condition
obj.getFile(table='incident', searchList=['short_description','is','test123'], type='.jpg')

# Upload an attachement to record(s) that satisfy the search condition
obj.uploadFile(table='incident', searchList=['short_description', 'is', 'test'], filename='D:\Tulips.jpg')

# Delete an attachement from record(s) that satisfy the search condition
obj.deleteFile(table='incident', searchList=['short_description', 'is', 'Upload 4'], filename='Riddles Treasure Hunt.pdf')

# Send email related to a particular record
# To send email not related to any specific record skip 'table' and 'sysId' fields
obj.sendEmail(table='incident', subject='Hello', message='hi', to='abc@example.com, xyz@example.com', sysId='33434f713200e1e0b5e18110c75b')

# Read email, where sysId is sysId of email
obj.readEmail(sysId='33434f713200e1e0b5e18110c75b')


Compatibility
-------------
Python 2 Tested: Python 2.6+
ServiceNow Tested: Istanbul, Geneva


Author
------
Created by Parul Neeraj <parulneeraj007@gmail.com> in 2017

