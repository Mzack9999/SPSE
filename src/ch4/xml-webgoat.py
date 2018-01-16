#!/usr/bin/env python

# Author: SPSE-3232
# Purpose:
# - Web Services are an important part of web communication now
# - Zeep: http://docs.python-zeep.org/en/master/ (Instead of Zolera - http://pywebsvcs.sourceforge.net/zsi.html)
# - Attack on WebGoat: http://yehg.net/lab/pr0js/training/webgoat.php#Web_Services (WSDL available only on 5.0)
# - Using http://volatileminds.net/CsharpVulnSoap.ova

from zeep import Client


def check_error(injection_result):
    return 'syntax error' in str(injection_result.content)


def pretty_print_vulnerable(operation_name, parameter_name):
    print('[+] Operation: ', operation_name, 'Parameter: ', parameter_name, 'vulnerable')


# Hostname taken from: https://stackoverflow.com/questions/24319662/from-inside-of-a-docker-container-how-do-i-connect-to-the-localhost-of-the-mach
client = Client('http://docker.for.mac.host.internal:8888/Vulnerable.asmx?WSDL')

# List of all methods

# root@74dd00124f9a:/src/ch4# python -mzeep http://docker.for.mac.host.internal:8888/Vulnerable.asmx?WSDL

# Prefixes:
#      ns0: http://tempuri.org/
#      xsd: http://www.w3.org/2001/XMLSchema

# Global elements:
#      ns0:AddUser(username: xsd:string, password: xsd:string)
#      ns0:AddUserResponse(AddUserResult: xsd:string)
#      ns0:ArrayOfString(ns0:ArrayOfString)
#      ns0:DeleteUser(username: xsd:string)
#      ns0:DeleteUserResponse(DeleteUserResult: xsd:boolean)
#      ns0:GetUser(username: xsd:string)
#      ns0:GetUserResponse(GetUserResult: xsd:string)
#      ns0:ListUsers()
#      ns0:ListUsersResponse(ListUsersResult: ns0:ArrayOfString)
#      ns0:boolean(xsd:boolean)
#      ns0:string(xsd:string)
     

# Global types:
#      xsd:anyType
#      ns0:ArrayOfString(string: xsd:string[])
#      xsd:ENTITIES
#      xsd:ENTITY
#      xsd:ID
#      xsd:IDREF
#      xsd:IDREFS
#      xsd:NCName
#      xsd:NMTOKEN
#      xsd:NMTOKENS
#      xsd:NOTATION
#      xsd:Name
#      xsd:QName
#      xsd:anySimpleType
#      xsd:anyURI
#      xsd:base64Binary
#      xsd:boolean
#      xsd:byte
#      xsd:date
#      xsd:dateTime
#      xsd:decimal
#      xsd:double
#      xsd:duration
#      xsd:float
#      xsd:gDay
#      xsd:gMonth
#      xsd:gMonthDay
#      xsd:gYear
#      xsd:gYearMonth
#      xsd:hexBinary
#      xsd:int
#      xsd:integer
#      xsd:language
#      xsd:long
#      xsd:negativeInteger
#      xsd:nonNegativeInteger
#      xsd:nonPositiveInteger
#      xsd:normalizedString
#      xsd:positiveInteger
#      xsd:short
#      xsd:string
#      xsd:time
#      xsd:token
#      xsd:unsignedByte
#      xsd:unsignedInt
#      xsd:unsignedLong
#      xsd:unsignedShort

# Bindings:
#      HttpGetBinding: {http://tempuri.org/}VulnerableServiceHttpGet
#      HttpPostBinding: {http://tempuri.org/}VulnerableServiceHttpPost
#      Soap11Binding: {http://tempuri.org/}VulnerableServiceSoap
#      Soap12Binding: {http://tempuri.org/}VulnerableServiceSoap12

# Service: VulnerableService
#      Port: VulnerableServiceSoap (Soap11Binding: {http://tempuri.org/}VulnerableServiceSoap)
#          Operations:
#             AddUser(username: xsd:string, password: xsd:string) -> AddUserResult: xsd:string
#             DeleteUser(username: xsd:string) -> DeleteUserResult: xsd:boolean
#             GetUser(username: xsd:string) -> GetUserResult: xsd:string
#             ListUsers() -> ListUsersResult: ns0:ArrayOfString

#      Port: VulnerableServiceSoap12 (Soap12Binding: {http://tempuri.org/}VulnerableServiceSoap12)
#          Operations:
#             AddUser(username: xsd:string, password: xsd:string) -> AddUserResult: xsd:string
#             DeleteUser(username: xsd:string) -> DeleteUserResult: xsd:boolean
#             GetUser(username: xsd:string) -> GetUserResult: xsd:string
#             ListUsers() -> ListUsersResult: ns0:ArrayOfString

#      Port: VulnerableServiceHttpGet (HttpGetBinding: {http://tempuri.org/}VulnerableServiceHttpGet)
#          Operations:
#             AddUser(username: xsd:string, password: xsd:string) -> xsd:string
#             DeleteUser(username: xsd:string) -> xsd:boolean
#             GetUser(username: xsd:string) -> xsd:string
#             ListUsers() -> xsd:string

#      Port: VulnerableServiceHttpPost (HttpPostBinding: {http://tempuri.org/}VulnerableServiceHttpPost)
#          Operations:
#             AddUser(username: xsd:string, password: xsd:string) -> xsd:string
#             DeleteUser(username: xsd:string) -> xsd:boolean
#             GetUser(username: xsd:string) -> xsd:string
#             ListUsers() -> xsd:string

# root@74dd00124f9a:/src/ch4# 

# List all users
users_list = client.service.ListUsers()

# Retrieve info for each user
for user in users_list:
    username, password = user.split(':')
    print('username: ', username, '\tpassword: ', password)
    user_details = client.service.GetUser(username)
    print('user details: ', user_details)

# Try to add a user
added_user_useraname, added_user_password = 'test', 'test'
result = client.service.AddUser(added_user_useraname, added_user_password)
print('add user result: ', result)

# Try to remove a user
result = client.service.DeleteUser(added_user_useraname)
print('removed user result: ', result)

# Now try to introduce error for each operations
# Disable zeep answer processing which triggers python exception
with client.options(raw_response=True):
    if (check_error(client.service.GetUser("aa'bb"))):
        pretty_print_vulnerable('GetUser', 'user')

    if (check_error(client.service.AddUser("test'ad'", 'test'))):
        pretty_print_vulnerable('AddUser', 'user')

    if (check_error(client.service.AddUser('test', "test'ad'"))):
        pretty_print_vulnerable('AddUser', 'password')

    if (check_error(client.service.DeleteUser("test'ad'"))):
        pretty_print_vulnerable('DeleteUser', 'user')


