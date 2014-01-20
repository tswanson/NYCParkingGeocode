import urllib2
import urllib
import json
import csv
import sys
import os
import time

#Request app_id and app_key from http://developer.cityofnewyork.us/api/geoclient-api-beta
app_id = 'xxxxxxx'
app_key = 'xxxxxxxxxxxxxxxxxxxxxxxx'

class precinct:
    def __init__(self, row):
        self.precinct = row[0]
        self.precinctFull = row[1]
        self.boro = row[2]
        self.boroCode = row[3]

class streetCode:
    def __init__(self, row):
        self.streetcode = row[0]
        self.streetname = row[1]

class streetReplace:
    def __init__(self, row):
        self.streetin = row[0]
        self.streetout = row[1]
        
class boroAbbrv:
    def __init__(self, row):
        self.boroabbrv = row[0]
        self.borocode = row[1]

class skipID:
    def __init__(self, row):
        self.skipid = row[0]
        
        
class inRow:
    def __init__(self, row):
        self.summonsnumber = row[0]
        self.plateid = row[1]
        self.registrationstate = row[2]
        self.platetype = row[3]
        self.issuedate = row[4]
        self.violationcode = row[5]
        self.vehiclebodytype = row[6]
        self.vehiclemake = row[7]
        self.issuingagency = row[8]
        self.streetcode1 = row[9]
        self.streetcode2 = row[10]
        self.streetcode3 = row[11]
        self.vehicleexpirationdate = row[12]
        self.violationlocation = row[13]
        self.violationprecinct = row[14]
        self.issuerprecinct = row[15]
        self.issuercode = row[16]
        self.issuercommand = row[17]
        self.issuersquad = row[18]
        self.violationtime = row[19]
        self.timefirstobserved = row[20]
        self.violationcounty = row[21]
        self.violationinfrontoforopposite = row[22]
        self.housenumber = row[23]
        self.streetname = row[24]
        self.intersectingstreet = row[25]
        self.datefirstobserved = row[26]
        self.lawsection = row[27]
        self.subdivision = row[28]
        self.violationlegalcode = row[29]
        self.daysparkingineffect = row[30]
        self.fromhoursineffect = row[31]
        self.tohoursineffect = row[32]
        self.vehiclecolor = row[33]
        self.unregisteredvehicle = row[34]
        self.vehicleyear = row[35]
        self.meternumber = row[36]
        self.feetfromcurb = row[37]
        self.violationpostcode = row[38]
        self.violationdescription = row[39]
        self.nostandingorstoppingviolation = row[40]
        self.hydrantviolation = row[41]
        self.doubleparkingviolation = row[42]


class outRow:
    def __init__(self):
        self.summonsnumber = ''
        self.housenumber = ''
        self.streetname = ''
        self.latitude = 0.0
        self.longitude = 0.0
        self.precinct = 0
        self.gsretcode = ''
        self.message = ''

        
def createPrecinctLookup(dir):
    f = open(dir+'precinct.csv', 'r')
    lookup = {}
    try:
        reader = csv.reader(f)
        for row in reader: 
            r = precinct(row)
            lookup[r.precinct] = "%s" % (r.boroCode)
    except:
        print 'Error opening '+dir+'precinct.csv', sys.exc_info()[0]
        
    
    return lookup

def createStreetLookup(dir):
    f = open(dir+'streetcode.csv', 'r')
    lookup = {}
    try:
        reader = csv.reader(f)
        for row in reader: 
            r = streetCode(row)
            lookup[r.streetcode] = "%s" % (r.streetname)
    except:
        print 'Error opening '+dir+'streetcode.csv', sys.exc_info()[0]
    
    return lookup

def createBoroAbbrvLookup(dir):
    f = open(dir+'boroabbrv.csv', 'r')
    lookup = {}
    try:
        reader = csv.reader(f)
        for row in reader: 
            r = boroAbbrv(row)
            lookup[r.boroabbrv] = "%s" % (r.borocode)
    except:
        print 'Error opening '+dir+'boroabbrv.csv', sys.exc_info()[0]
    
    return lookup

def createStreetReplace(dir):
    f = open(dir+'streetreplace.csv', 'r')
    lookup = {}
    try:
        reader = csv.reader(f)
        for row in reader: 
            r = streetReplace(row)
            lookup[r.streetin] = "%s" % (r.streetout)
    except:
        print 'Error opening '+dir+'streetreplace.csv', sys.exc_info()[0]
    
    return lookup

def createSkipId(dir):
    f = open(dir+'goodids.csv', 'r')
    lookup = {}
    i = 0
    try:
        reader = csv.reader(f)
        for row in reader: 
            r = skipID(row)
            i = i+1
            lookup[r.skipid] = "%s" % (r.skipid)
    except:
        print 'Error opening '+dir+'goodids.csv .'+str(i), sys.exc_info()[0]

    print "done1"
    return lookup

def scrubStreet(s,srlookup):
    s = s.upper()
    s = s.replace(',',' ')
     
    s = s.replace('CORNER OF ',' ')
    s = s.replace('CORNER ',' ')
    s = s.replace(' FEET ',' FT ')
    
    
       
    s = s.replace(',',' ')
    
    if(len(s)<5):
        return s
    if(s[1] == '/' and s[3] == ' '):
        s = s[4:]
    i =  s.find('/OF ')
    if(i >= 0):
        s = s[i+4:]
    i =  s.find(' FROM ')
    if(i >= 0):
        s = s[i+6:]
    #repeat
    if(len(s)<5):
        return s
    if(s[1] == '/' and s[3] == ' '):
        s = s[4:]
    
    i =  s.find('ON ')
    if(i == 0):
        s = s[i+3:]

    i =  s.find(' W/O ')
    if(i >= 0):
        s = s[i+5:]

    i =  s.find(' W/O ')
    if(i >= 0):
        s = s[i+5:]
    i =  s.find(' E/O ')
    if(i >= 0):
        s = s[i+5:]
    i =  s.find(' N/O ')
    if(i >= 0):
        s = s[i+5:]
    i =  s.find(' S/O ')
    if(i >= 0):
        s = s[i+5:]
    i =  s.find('OF ')
    if(i == 0):
        s = s[i+3:]

    s = s.replace('0FT ','0 FT ')
    s = s.replace('5FT ','5 FT ')
    i =  s.find(' FT ')
    if(i == 0):
        s = s[i+4:]
        
    if(s in srlookup):
      s = srlookup[s]

    return s

def parseNameFromMessage(s):
    
    if(s[0] == '\''):
        s = s[1:]
    i =  s.find('\'')
    if(i > 0):
        s = s[0:i-1]
    return s

headerOut = "summonsnumber,housenumber,streetname,intersecStreet,street1,street2,street3,longitude,latitude,precinct,gsRetCode,message\n"


try:

    dir = os.path.dirname(os.path.realpath(__file__))+"\\"

    # all_accidents.csv
    f = open(dir+'SampleAddr.csv', 'rb') 
    #f = open(sys.argv[1], 'rb') # opens the csv file
    ofile  = open(dir+'geocodedout.csv', "wb")
    plookup = createPrecinctLookup(dir)
    slookup = createStreetLookup(dir)
    blookup = createBoroAbbrvLookup(dir)
    print "loading skip"
    skiplookup = createSkipId(dir)
    print "done"
    srlookup = createStreetReplace(dir)

    reader = csv.reader(f)  
    x = 0
    bc = '0'
    previous = ""
    current = ""
    o = outRow()
    i = 0
    boro = ""
    exceptionStreet =""
    street1 = ''
    street2 = ''
    street3 = ''
    ofile.writelines(headerOut)
    start = time.time()
    for row in reader:   
        street1 = ''
        street2 = ''
        street3 = ''
        badAddrLon = 0.0
        badAddrLat = 0.0
        r = inRow(row)
        housenumber = r.housenumber
        i
        if(housenumber == 'House Number'):
            continue
       
        if(r.summonsnumber in skiplookup):
            continue
        
           
        #these are moving violations and addresses are very difficult to geocode
        if(r.violationdescription == 'FAILURE TO STOP AT RED LIGHT' or r.violationdescription == 'BUS LANE VIOLATION'):
            continue

        datesplit = r.issuedate.split('/')
        if(len(datesplit)<3):
            continue
        #other years unusable.  Create a histogram of data before using.
        if(datesplit[2] <> '2013'):
            continue
       
        streetname = scrubStreet(r.streetname,srlookup)
        
        intstreet = scrubStreet(r.intersectingstreet,srlookup)
        # Doesn't hit on Penn Plaza 
        if(housenumber.find('1PEN') == 0 or housenumber.find('1PP') == 0):
            housenumber = 257
            
            
        if(housenumber.find('2PEN') == 0):
            housenumber = 218
        if(housenumber.find('2PEN') == 0):
            housenumber = 218
        if(housenumber.find('5PEN') == 0 or housenumber.find('5PP') == 0):
            housenumber = 460
        if(housenumber.find('11PEN') == 0 or housenumber.find('11PP') == 0):
            housenumber = 399
    
        if(housenumber == '201-C'):
            housenumber = 201
        if(housenumber == '69-A'):
            housenumber = 69
        if(housenumber == '1-3-5'):
            housenumber = 3
       
            
        if(intstreet == ' ' and streetname.find(' AND ') > 0):
           j = streetname.find(' AND ')
           intstreet = streetname[i+5:]
           streetname = streetname[0:i]
           
        precinct = r.violationprecinct
        
            
        try:
            bc = plookup[precinct]
        except:
            bc = '0'
        if(bc == '0'):
            try:
                bc = blookup[r.violationcounty]
            except:
                # default, worth trying
                bc = '1'

        try:
            street1 = slookup[bc+r.streetcode1]
        except:
            street1 = ''

        try:
            street2 = slookup[bc+r.streetcode2]
        except:
            street2 = ''

        try:
            street3 = slookup[bc+r.streetcode3]
        except:
            street3 = ''

        
        
        if(housenumber == '' or housenumber == '0' or housenumber == 'W' or housenumber == 'S' or housenumber == 'E' or housenumber == 'N'):

            urlInt  = 'https://api.cityofnewyork.us//geoclient//v1//intersection.json?' + urllib.urlencode({"crossStreetOne": streetname, "crossStreetTwo": intstreet, "borough": bc, "app_id": app_id, "app_key": app_key,"compassDirection": "S"})

            response = urllib2.urlopen(urlInt)
            data = json.load(response)
            retCode = data["intersection"]["geosupportReturnCode"]
            if(retCode == "00"):
                ret = '%s,%s,%s,%s,%s,%s,%s,%f,%f,%s,%s,%s\n' % (r.summonsnumber,housenumber,r.streetname,r.intersectingstreet,street1,street2,street3,data["intersection"]["latitude"],data["intersection"]["longitude"],data["intersection"]["policePrecinct"],data["intersection"]["geosupportReturnCode"],"")
                #str= objid+","+data["intersection"]["latitude"]+","+data["intersection"]["longitude"]+","+data["intersection"]["policePrecionct"]+","+data["intersection"]["geosupportReturnCode"]
            elif(retCode == "01"):
                ret = '%s,%s,%s,%s,%s,%s,%s,%f,%f,%s,%s,%s\n' % (r.summonsnumber,housenumber,r.streetname,r.intersectingstreet,street1,street2,street3,data["intersection"]["latitude"],data["intersection"]["longitude"],data["intersection"]["policePrecinct"],data["intersection"]["geosupportReturnCode"],data["intersection"]["message"].replace(',',' '))
            elif(retCode == "EE"):
                if(parseNameFromMessage(data["intersection"]["message"]) == streetname):
                    urlInt  = 'https://api.cityofnewyork.us//geoclient//v1//intersection.json?' + urllib.urlencode({"crossStreetOne": data["intersection"]["streetName1"], "crossStreetTwo": intstreet, "borough": bc, "app_id": app_id, "app_key": app_key,"compassDirection": "S"})
                else:
                    urlInt  = 'https://api.cityofnewyork.us//geoclient//v1//intersection.json?' + urllib.urlencode({"crossStreetOne": streetname, "crossStreetTwo": data["intersection"]["streetName1"], "borough": bc, "app_id": app_id, "app_key": app_key,"compassDirection": "S"})

                response = urllib2.urlopen(urlInt)
                data = json.load(response)
                retCode = data["intersection"]["geosupportReturnCode"]
                if(retCode == "00"):
                    ret = '%s,%s,%s,%s,%s,%s,%s,%f,%f,%s,%s,%s\n' % (r.summonsnumber,housenumber,r.streetname,r.intersectingstreet,street1,street2,street3,data["intersection"]["latitude"],data["intersection"]["longitude"],data["intersection"]["policePrecinct"],data["intersection"]["geosupportReturnCode"],"")
                    #str= objid+","+data["intersection"]["latitude"]+","+data["intersection"]["longitude"]+","+data["intersection"]["policePrecionct"]+","+data["intersection"]["geosupportReturnCode"]
                elif(retCode == "01"):
                    ret = '%s,%s,%s,%s,%s,%s,%s,%f,%f,%s,%s,%s\n' % (r.summonsnumber,housenumber,r.streetname,r.intersectingstreet,street1,street2,street3,data["intersection"]["latitude"],data["intersection"]["longitude"],data["intersection"]["policePrecinct"],data["intersection"]["geosupportReturnCode"],data["intersection"]["message"].replace(',',' '))
               
                    
                else:
                    ret = '%s,%s,%s,%s,%s,%s,%s,%f,%f,%s,%s,%s\n' % (r.summonsnumber,housenumber,r.streetname,r.intersectingstreet,street1,street2,street3,0.0,0.0,"00",data["intersection"]["geosupportReturnCode"],data["intersection"]["message"].replace(',',' '))
            elif(retCode == "40"):
                urlInt  = 'https://api.cityofnewyork.us//geoclient//v1//intersection.json?' + urllib.urlencode({"crossStreetOne": streetname, "crossStreetTwo": intstreet, "borough": bc, "app_id": app_id, "app_key": app_key,"compassDirection": "E"})

                response = urllib2.urlopen(urlInt)
                data = json.load(response)
                retCode = data["intersection"]["geosupportReturnCode"]
                if(retCode == "00"):
                    ret = '%s,%s,%s,%s,%s,%s,%s,%f,%f,%s,%s,%s\n' % (r.summonsnumber,housenumber,r.streetname,r.intersectingstreet,street1,street2,street3,data["intersection"]["latitude"],data["intersection"]["longitude"],data["intersection"]["policePrecinct"],data["intersection"]["geosupportReturnCode"],"")
                    #str= objid+","+data["intersection"]["latitude"]+","+data["intersection"]["longitude"]+","+data["intersection"]["policePrecionct"]+","+data["intersection"]["geosupportReturnCode"]
                elif(retCode == "01"):
                    ret = '%s,%s,%s,%s,%s,%s,%s,%f,%f,%s,%s,%s\n' % (r.summonsnumber,housenumber,r.streetname,r.intersectingstreet,street1,street2,street3,data["intersection"]["latitude"],data["intersection"]["longitude"],data["intersection"]["policePrecinct"],data["intersection"]["geosupportReturnCode"],data["intersection"]["message"].replace(',',' '))
               
                    
                else:
                    ret = '%s,%s,%s,%s,%s,%s,%s,%f,%f,%s,%s,%s\n' % (r.summonsnumber,housenumber,r.streetname,r.intersectingstreet,street1,street2,street3,0.0,0.0,"00",data["intersection"]["geosupportReturnCode"],data["intersection"]["message"].replace(',',' '))

            else:
                ret = '%s,%s,%s,%s,%s,%s,%s,%f,%f,%s,%s,%s\n' % (r.summonsnumber,housenumber,r.streetname,r.intersectingstreet,street1,street2,street3,0.0,0.0,"00",data["intersection"]["geosupportReturnCode"],data["intersection"]["message"].replace(',',' '))


        else:
            urlAddr = 'https://api.cityofnewyork.us//geoclient//v1//address.json?'      + urllib.urlencode({"houseNumber": housenumber, "street": streetname, "borough": bc, "app_id": app_id, "app_key": app_key})

        
            response = urllib2.urlopen(urlAddr)
            data = json.load(response)
            retCode = data["address"]["geosupportReturnCode"]
            try:
                if(retCode == '42'):
                    badAddrLon = data["address"]["longitudeInternalLabel"]
                    badAddrLat = data["address"]["latitudeInternalLabel"]
            except:
                j = 0
                
            if(retCode == "00"):
                ret = '%s,%s,%s,%s,%s,%s,%s,%f,%f,%s,%s,%s\n' % (r.summonsnumber,housenumber,r.streetname,r.intersectingstreet,street1,street2,street3,data["address"]["latitude"],data["address"]["longitude"],data["address"]["policePrecinct"],data["address"]["geosupportReturnCode"],"")
                #str= objid+","+data["intersection"]["latitude"]+","+data["intersection"]["longitude"]+","+data["intersection"]["policePrecionct"]+","+data["intersection"]["geosupportReturnCode"]
            elif(retCode == "01"):
                ret = '%s,%s,%s,%s,%s,%s,%s,%f,%f,%s,%s,%s\n' % (r.summonsnumber,housenumber,r.streetname,r.intersectingstreet,street1,street2,street3,data["address"]["latitude"],data["address"]["longitude"],data["address"]["policePrecinct"],data["address"]["geosupportReturnCode"],data["address"]["message"].replace(',',' '))
            elif(retCode == "EE"):
                urlAddr = 'https://api.cityofnewyork.us//geoclient//v1//address.json?'      + urllib.urlencode({"houseNumber": housenumber, "street": data["address"]["streetName1"], "borough": bc, "app_id": app_id, "app_key": app_key})
 
                response = urllib2.urlopen(urlAddr)
                data = json.load(response)
                retCode = data["address"]["geosupportReturnCode"]
                if(retCode == "00"):
                    ret = '%s,%s,%s,%s,%s,%s,%s,%f,%f,%s,%s,%s\n' % (r.summonsnumber,housenumber,r.streetname,r.intersectingstreet,street1,street2,street3,data["address"]["latitude"],data["address"]["longitude"],data["address"]["policePrecinct"],data["address"]["geosupportReturnCode"],"")
                    #str= objid+","+data["intersection"]["latitude"]+","+data["intersection"]["longitude"]+","+data["intersection"]["policePrecionct"]+","+data["intersection"]["geosupportReturnCode"]
                elif(retCode == "01"):
                    ret = '%s,%s,%s,%s,%s,%s,%s,%f,%f,%s,%s,%s\n' % (r.summonsnumber,housenumber,r.streetname,r.intersectingstreet,street1,street2,street3,data["address"]["latitude"],data["address"]["longitude"],data["address"]["policePrecinct"],data["address"]["geosupportReturnCode"],data["address"]["message"].replace(',',' '))
                
                else:
                    ret = '%s,%s,%s,%s,%s,%s,%s,%f,%f,%s,%s,%s\n' % (r.summonsnumber,housenumber,r.streetname,r.intersectingstreet,street1,street2,street3,0.0,0.0,"00",data["address"]["geosupportReturnCode"],data["address"]["message"].replace(',',' '))

            elif(retCode == "42" and badAddrLon <> 0.0 ):
                ret = '%s,%s,%s,%s,%s,%s,%s,%f,%f,%s,%s,%s\n' % (r.summonsnumber,housenumber,r.streetname,r.intersectingstreet,street1,street2,badAddrLat,badAddrLon,"00",data["address"]["geosupportReturnCode"],data["address"]["message"].replace(',',' '))
                
            elif(retCode == "42" and street1 <> '' and street2 <> ''):
                urlInt  = 'https://api.cityofnewyork.us//geoclient//v1//intersection.json?' + urllib.urlencode({"crossStreetOne": streetname, "crossStreetTwo": intstreet, "borough": bc, "app_id": app_id, "app_key": app_key,"compassDirection": "S"})

                response = urllib2.urlopen(urlInt)
                data = json.load(response)
                retCode = data["intersection"]["geosupportReturnCode"]
                if(retCode == "00"):
                    ret = '%s,%s,%s,%s,%s,%s,%s,%f,%f,%s,%s,%s\n' % (r.summonsnumber,housenumber,r.streetname,r.intersectingstreet,street1,street2,street3,data["intersection"]["latitude"],data["intersection"]["longitude"],data["intersection"]["policePrecinct"],data["intersection"]["geosupportReturnCode"],"")
                    #str= objid+","+data["intersection"]["latitude"]+","+data["intersection"]["longitude"]+","+data["intersection"]["policePrecionct"]+","+data["intersection"]["geosupportReturnCode"]
                elif(retCode == "01"):
                    ret = '%s,%s,%s,%s,%s,%s,%s,%f,%f,%s,%s,%s\n' % (r.summonsnumber,housenumber,r.streetname,r.intersectingstreet,street1,street2,street3,data["intersection"]["latitude"],data["intersection"]["longitude"],data["intersection"]["policePrecinct"],data["intersection"]["geosupportReturnCode"],data["intersection"]["message"].replace(',',' '))
                elif(retCode == "EE"):
                    if(parseNameFromMessage(data["intersection"]["message"]) == streetname):
                        urlInt  = 'https://api.cityofnewyork.us//geoclient//v1//intersection.json?' + urllib.urlencode({"crossStreetOne": data["intersection"]["streetName1"], "crossStreetTwo": intstreet, "borough": bc, "app_id": app_id, "app_key": app_key,"compassDirection": "S"})
                    else:
                        urlInt  = 'https://api.cityofnewyork.us//geoclient//v1//intersection.json?' + urllib.urlencode({"crossStreetOne": streetname, "crossStreetTwo": data["intersection"]["streetName1"], "borough": bc, "app_id": app_id, "app_key": app_key,"compassDirection": "S"})

                    response = urllib2.urlopen(urlInt)
                    data = json.load(response)
                    retCode = data["intersection"]["geosupportReturnCode"]
                    if(retCode == "00"):
                        ret = '%s,%s,%s,%s,%s,%s,%s,%f,%f,%s,%s,%s\n' % (r.summonsnumber,housenumber,r.streetname,r.intersectingstreet,street1,street2,street3,data["intersection"]["latitude"],data["intersection"]["longitude"],data["intersection"]["policePrecinct"],data["intersection"]["geosupportReturnCode"],"")
                        #str= objid+","+data["intersection"]["latitude"]+","+data["intersection"]["longitude"]+","+data["intersection"]["policePrecionct"]+","+data["intersection"]["geosupportReturnCode"]
                    elif(retCode == "01"):
                        ret = '%s,%s,%s,%s,%s,%s,%s,%f,%f,%s,%s,%s\n' % (r.summonsnumber,housenumber,r.streetname,r.intersectingstreet,street1,street2,street3,data["intersection"]["latitude"],data["intersection"]["longitude"],data["intersection"]["policePrecinct"],data["intersection"]["geosupportReturnCode"],data["intersection"]["message"].replace(',',' '))
                   
                        
                    else:
                        ret = '%s,%s,%s,%s,%s,%s,%s,%f,%f,%s,%s,%s\n' % (r.summonsnumber,housenumber,r.streetname,r.intersectingstreet,street1,street2,street3,0.0,0.0,"00",data["intersection"]["geosupportReturnCode"],data["intersection"]["message"].replace(',',' '))

                else:
                    ret = '%s,%s,%s,%s,%s,%s,%s,%f,%f,%s,%s,%s\n' % (r.summonsnumber,housenumber,r.streetname,r.intersectingstreet,street1,street2,street3,0.0,0.0,"00",data["intersection"]["geosupportReturnCode"],data["intersection"]["message"].replace(',',' '))

                
            else:
                ret = '%s,%s,%s,%s,%s,%s,%s,%f,%f,%s,%s,%s\n' % (r.summonsnumber,housenumber,r.streetname,r.intersectingstreet,street1,street2,street3,0.0,0.0,"00",data["address"]["geosupportReturnCode"],data["address"]["message"].replace(',',' '))

        splitret = ret.split(',')
        if(len(splitret) <> 12):
            continue
        
        ofile.writelines(ret)
        
        i = i+1
       
        if(i%500 == 0):
          print i
          print time.time() - start, "seconds."
          time.sleep(5)
          start = time.time()
          
          
    print str(i)+' records processed'
    f.close()      # closing
    ofile.close()
except:
    print "Unexpected error:", sys.exc_info()[0]
    raise




