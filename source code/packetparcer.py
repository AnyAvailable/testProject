import requests
import json
from packaging.version import parse 
def getbranches():
    """returns a list of processed brunches in the json format and lists of architectures"""
    #this condition checks if server is available and query is correct#
    if requests.get("https://rdb.altlinux.org/api/export/branch_binary_packages/p10").status_code == 200 and requests.get("https://rdb.altlinux.org/api/export/branch_binary_packages/sisyphus").status_code == 200:
        p10 = requests.get("https://rdb.altlinux.org/api/export/branch_binary_packages/p10").json()["packages"] # this line gets binary data and convert it into json
        sis = requests.get("https://rdb.altlinux.org/api/export/branch_binary_packages/sisyphus").json()["packages"] # this line gets binary data and convert it into json
    else:
        print("Query isn't correct or server is anavailable") # error message
    
    return [p10, sis] # this line return lists of arguments later it used in getpackageandarchlist function


def unpackarchscycle(listofpackages, listofarchs):
    """this function contains cycle that unpacks arcs and add it into arch lists"""
    for i in range(len(listofpackages)): # arcs unpack cycle
        if listofpackages[i]["arch"] not in listofarchs: # if arch is not in list it adds
            try: # checks if there is no arch field in listofpackage
                listofarchs.append(listofpackages[i]["arch"])
            except NameError: 
                print("There is no arch field in package") # if there is no arch field in listofpackage cycle breaks
                break
        else: # if arch in list of arcs cycle continuing
            continue
    
    return listofarchs # this list contains arcs that are in listofpackages


def getpackageandarchlists(brresult): # this function convert data into usable list of arguments
       
    p10archlist = [] # this varaible is list of arcs
    sisarchlist = [] # this varaible is list of arcs
    p10archlist = unpackarchscycle(brresult[0], p10archlist) # this varaible takes p10 arcs
    sisarchlist = unpackarchscycle(brresult[1], sisarchlist) # this varaible takes sis arcs
    gpaalresult = [brresult[0], brresult[1], p10archlist, sisarchlist] # this varaible puts varaibles into list to return them later
    
    return gpaalresult


def packageandarchparce(result):
    """this function creates dictionary parces packages and archs due to work requirements than fill it into dictionary and converts it into json""" 
    
    p10 = result[0] # p10 package list
    sis = result[1] # sis package list
    p10archlist = result[2] # p10 arcs list
    sisarchlist = result[3] # sis arcs list
    parcedpackages = dict()
    parcedpackages.update(packsinp10notinsis = {}, packsinsisnotinp10 = {}, sisvermorethanp10packs = {}) # dictionary structure (not done just varaible with basic dictionary that sorts into different tasks due to work requirements)
    
    for dictionary in parcedpackages: # structure creation cycle
        if dictionary == 'packsinp10notinsis':# this condition checks if inner dictionary coincedencesing with packsinp10notinsis string
            for element in p10archlist: # this cycle unpack list of p10 arcs
                parcedpackages[dictionary].setdefault(element, []) # this cycle fill packsinp10notinsis dictionary with arcs as keys and [] as values
        else: # in case if dictionry not coincedencesing with packsinp10notinsis string this condition fill other dictionaries with arcs from sisarchlist
            for element in sisarchlist: # this cycle unpack list of sis arcs
                parcedpackages[dictionary].setdefault(element, []) # this cycle fill packsinsisnotinp10 and sisvermorethanp10packs dictionaries with arcs as keys and [] as values

    """
    here is an example of structure i generate and used here
    {
        'packsinp10notinsis' : {
            'arch0' : [{package0},{package1},{package2},{package3}...]
            'arch1' : [{package0},{package1},{package2},{package3}...]
            'arch2' : [{package0},{package1},{package2},{package3}...]
            'arch3' : [{package0},{package1},{package2},{package3}...]
            'arch4' : [{package0},{package1},{package2},{package3}...]
        }, 
        'packsinsisnotinp10' : {
            'arch0' : [{package0},{package1},{package2},{package3}...]
            'arch1' : [{package0},{package1},{package2},{package3}...]
            'arch2' : [{package0},{package1},{package2},{package3}...]
            'arch3' : [{package0},{package1},{package2},{package3}...]
            'arch4' : [{package0},{package1},{package2},{package3}...]
        }, 
        'sisvermorethanp10packs' : {
            'arch0' : [{package0},{package1},{package2},{package3}...]
            'arch1' : [{package0},{package1},{package2},{package3}...]
            'arch2' : [{package0},{package1},{package2},{package3}...]
            'arch3' : [{package0},{package1},{package2},{package3}...]
            'arch4' : [{package0},{package1},{package2},{package3}...]
        }, 
    } 
    """

    i = 0 # this increment used to call package from sis which index equals to p10
    for p10dict in p10: # choosing dictionary from p10
        try: # if value of i more than length of sis than put all other packages into parcedpackages["packsinp10notinsis"] due to arch 
            if p10dict['arch'] == sis[i]['arch']: # here condition checks if arch of p10dict equals to arch of sis due to index(during checking condition index of p10dict equals index of sisdict)
                if p10dict not in sis: # if there is no p10dict(package) in sis(list of dictionaries(packages))
                    parcedpackages["packsinp10notinsis"][p10dict['arch']].append(p10dict) # if everything is all right in upper code it adds package into dictionary
        except IndexError: # if value of i more than length of sis than put all other packages into parcedpackages["packsinp10notinsis"] due to arch
            parcedpackages["packsinp10notinsis"][p10dict['arch']].append(p10dict)
        i += 1 # ++i

    i = 0 # this increment used to call package from p10 which index equals to sis
    for sisdict in sis: # choosing dictionary from sis
        try: # if value of i more than length of p10 than put all other packages into parcedpackages["packsinsisnotinp10"] due to arch
            if sisdict['arch'] == p10[i]['arch']: # here condition checks if arch of sisdict equals to arch of p10 due to index(during checking condition index of p10dict equals index of sisdict)
                if sisdict not in p10: # if there is no sisdict(package) in p10(list of dictionaries(packages))
                    parcedpackages["packsinsisnotinp10"][sisdict['arch']].append(sisdict) # if everything is all right in upper code it adds package into dictionary
        except IndexError: # if value of i more than length of p10 than put all other packages into parcedpackages["packsinsisnotinp10"] due to arch
            parcedpackages["packsinsisnotinp10"][sisdict['arch']].append(sisdict)
        i += 1 # ++i

    i = 0 # this increment used to call package from p10 which index equals to sis
    for sisdict in sis: # choosing dictionary from sis
        try: # if value of i more than length of p10 than put all other packages into parcedpackages["sisvermorethanp10packs"] due to arch
            if sisdict['arch'] == p10[i]['arch']: # here condition checks if arch of sisdict equals to arch of p10 due to index(during checking condition index of p10dict equals index of sisdict)
                #print(parse(sisdict['version']))
                if parse(sisdict['version']+"-"+sisdict['release']) > parse(p10[i]['version']+"-"+p10[i]['release']):# here is used parse method of packagin.version lib, that can be used to compare versions 
                    parcedpackages["sisvermorethanp10packs"][sisdict['arch']].append(sisdict) # if everything is all right in upper code it adds package into dictionary        
        except IndexError: # if value of i more than length of p10 than put all other packages into parcedpackages["sisvermorethanp10packs"] due to arch
            parcedpackages["sisvermorethanp10packs"][sisdict['arch']].append(sisdict)
        i += 1 # ++i

    print(json.dumps(parcedpackages, indent=4)) # this line output parcedpackage like json structure


