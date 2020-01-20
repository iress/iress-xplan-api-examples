# EDAI Authentication Using RAPI

## Overview
When 2FA is enabled and mandatory for an Xplan site and the client needs to use EDAI to integrate with Xplan, 
we will need to use Xplan's Resourceful API to authenticate and establish an Xplan session. Once a session has been
established we can use that session in our EDAI calls. 

_**Note:** The user needs to have the `EDAI access` capability._

### Sample code
For login using 2FA please see the class `iress.xplan.api.ResourcefulAPIBasicAuth` in `iress/xplan/api.py`.

For example on how to use 2FA authentication for EDAI please see the class `iress.xplan.edai.EDAICall`
 in `iress/xplan/edai.py`.
