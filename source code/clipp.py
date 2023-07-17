#/usr/bin/env python
from packetparcer import getbranches, getpackageandarchlists, packageandarchparce # importing functions
"""calling the getbranches function inside getpackageandarchlists 
inside the packageandarchparce function in general 
this starts the module"""
packageandarchparce(getpackageandarchlists(getbranches())) 


