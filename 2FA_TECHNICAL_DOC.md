# 2FA Technical Details

## Overview
When 2FA is enabled and mandatory for an Xplan site and basic authentication is needed to authenticate to Xplan's API 
we will need to pass the One Time Password (OTP) along with the username and password in the 
`Authorization` header. The password and the OTP are separated by `\n\r\t\u0007`. So the `Authorization` header 
value will be `Basic Base64Hash` where the `Base64Hash` is the Base64 hash of the username, password and OTP in the
 format `USER:PASSWORD\n\r\t\u0007OTP`.

#### Example
```
USER = dummy-user
PASSWORD = dummy-pwd
OTP = MR2W23LZFVXXI4C7ONSWG4TFOQ

Base64 Hash = ZHVtbXktdXNlcjpkdW1teS1wd2QKDQkHMTA5ODg1

Authorization Header = Basic ZHVtbXktdXNlcjpkdW1teS1wd2QKDQkHMTA5ODg1
```

_**Note:** Once a session has been established please use the Cookies returned
 (which will have the `XPLANID` session cookie) instead of the `Authorization` header._ 

### Sample code
For login using 2FA please see the class `iress.xplan.api.ResourcefulAPIBasicAuth` in `iress/xplan/api.py`.

## How to set up 2FA
Please use the community document
[Two-factor Authentication](https://community.iress.com/t5/Help-Guide-Xplan/Two-factor-Authentication/ta-p/4994)
to set up 2FA and please select `Software Token`. Use the `Secret Key` provided for the OTP Secret.

_**Important Note:** Please keep the `Secret Key` secure as this is the shared secret used to generate an OTP, if this
is compromised please generate a new one. This should only be used for backend applications that have their own
service account. Front-end apps should use oauth._
