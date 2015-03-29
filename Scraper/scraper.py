categories = {'EMERG MGMT': 'PUBLIC SAFETY - EMERGENCY MANAGEMENT',
              'HEALTH PROF': 'HEALTH - PROFESSIONALS',
              'SCH FACILITI': 'EDUCATION - SCHOOL FACILITIES',
              'PENSIONS TEA': 'PENSIONS - TEACHERS'}
''',
              'FISH': 'ENVIRONMENT - FISH AND WILDLIFE',
              'TEMP DISAB': 'LABOR - TEMPORARY DISABILITY',
              'HEALTH FAC': 'HEALTH - FACILITIES',
              'LABOR': 'LABOR',
              'ENVIRONMENT': 'ENVIRONMENT',
              'SITE REMED': 'ENVIRONMENT - SITE REMEDIATION AND BROWNFIELDS',
              'HOUSING FIN': 'HOUSING - FINANCE',
              'EMER SVCS': 'HEALTH - EMERGENCY MEDICAL SERVICES',
              'ED HEALTH': 'EDUCATION - HEALTH',
              'POLLUTION': 'ENVIRONMENT - AIR, NOISE AND WATER POLLUTION',
              'INCOME TAX': 'TAXATION - PERSONAL INCOME TAX',
              'BUS TAXES': 'TAXATION - BUSINESS TAXES',
              'CRIME VICTIM': 'CRIME VICTIMS',
              'HEALTH FINAN': 'HEALTH - FINANCE',
              'PENSIONS POL': 'PENSIONS - POLICE AND FIREFIGHTERS',
              'PUB SAFETY': 'PUBLIC SAFETY',
              'CRIM PROCED': 'CRIMINAL PROCEDURES',
              'TRANS PLAN': 'TRANSPORTATION - PLANNING, FINANCE AND ECONOMIC DEVELOPMENT',
              'SALES TAX': 'TAXATION - SALES TAX',
              'OPEN SPACE': 'ENVIRONMENT - PARKS, FORESTS AND OPEN SPACE',
              'SCH TRANS': 'EDUCATION - SCHOOL TRANSPORTATION',
              'TEACHERS': 'EDUCATION - TEACHERS AND SCHOOL EMPLOYEES',
              'LANDLORD': 'HOUSING - LANDLORD AND TENANT',
              'HOMELAND SEC': 'PUBLIC SAFETY - HOMELAND SECURITY',
              'FREIGHT RAIL': 'TRANSPORTATION - FREIGHT RAIL',
              'WASTEWATER': 'ENVIRONMENT - WASTEWATER AND STORMWATER', 'BEACHES': 'ENVIRONMENT - BEACHES AND SHORES',
              'PUB UTIL TAX': 'TAXATION - PUBLIC UTILITIES TAX', 'HIGHLANDS': 'ENVIRONMENT - HIGHLANDS AND PINELANDS',
              'TAXATION': 'TAXATION', 'ALCO TAXES': 'TAXATION - ALCOHOL, GASOLINE AND TOBACCO TAXES', 'POLICE': 'PUBLIC SAFETY - POLICE',
              'FIREFIGHTERS': 'PUBLIC SAFETY - FIREFIGHTERS', 'CRIMES': 'CRIMES AND PENALTIES', 'DISEASE': 'HEALTH - DISEASE',
              'HOUSING': 'HOUSING', 'CONSTR CODES': 'HOUSING - CONSTRUCTION CODES', 'WEAPONS': 'PUBLIC SAFETY - WEAPONS',
              'FLOOD': 'ENVIRONMENT - FLOODING, DAMS AND LAKES', 'AFFORD HOUS': 'HOUSING - AFFORDABLE HOUSING',
              'CURRICULA': 'EDUCATION - CURRICULA', 'SOLID WASTE': 'ENVIRONMENT - SOLID WASTE AND RECYCLING',
              'SEX OFFEND': 'PUBLIC SAFETY - SEX OFFENDERS', 'HOTELS': 'HOUSING - HOTELS AND MULTIPLE DWELLINGS',
              'PROPERTY TAX': 'TAXATION - PROPERTY TAX', 'HIGHWAYS': 'TRANSPORTATION - HIGHWAYS, ROADS AND BRIDGES',
              'WORKERS COMP': 'LABOR - WORKERS COMPENSATION', 'EDUC FINANCE': 'EDUCATION - FINANCE',
              'HAZ SUBSTANC': 'ENVIRONMENT - HAZARDOUS AND TOXIC SUBSTANCES', 'SCH BOARDS': 'EDUCATION - SCHOOL BOARDS AND DISTRICTS',
              'CONDOS': 'HOUSING - CONDOMINIUMS, COOPERATIVES AND MOBILE HOMES', 'UNEMPL COMP': 'LABOR - UNEMPLOYMENT COMPENSATION',
              'PHARMACEUTIC': 'HEALTH - PHARMACEUTICALS', 'PENSIONS': 'PENSIONS', 'WATER SUPPLY': 'ENVIRONMENT - WATER SUPPLY',
              'PENSIONS PUB': 'PENSIONS - PUBLIC EMPLOYEES', 'HEALTH': 'HEALTH', 'PAAD': 'HEALTH - PAAD AND SENIOR GOLD',
              'PUBLIC TRANS': 'TRANSPORTATION - PUBLIC TRANSIT', 'WAGES': 'LABOR - WAGES AND BENEFITS',
              'EDUCATION': 'EDUCATION',
              'TRANSPORT': 'TRANSPORTATION'
            }
            '''
              

#!/usr/bin/python
import json
import urllib
import urllib2
import mechanize

br = mechanize.Browser()
br.set_handle_robots(False)   # ignore robots
br.set_handle_refresh(False)  # can sometimes hang without this
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]	      	# [('User-agent', 'Firefox')]
br.open("http://www.njleg.state.nj.us/bills/BillsBySubject.asp")
    
def getCategoryHtml(category):
    val = []
    val.append(category)
    br.select_form("Bills")
    br.set_all_readonly(False)
    br["ListSearch"] = val
    br["SearchText"] = category
    response = br.submit()
    html = response.read()
    htmlLst = html.split(' ')
    br.back()
    return htmlLst

def getBillNumLst(htmlLst):
    billnumLst = []
    for item in htmlLst:
        startsWith = item.startswith("href=\"javascript:ShowBill(\'")
        if startsWith == True:
            tmp = item[27:]
            billnumLst.append(tmp)
    return billnumLst

def getBillHtml(billNum):
    br.select_form("ShowBill")
    br.set_all_readonly(False)
    billNum = str(billNum)
    br["BillNumber"] = billNum
    response = br.submit()
    html = response.read()
    htmlLst = html.split(' ')
    br.back()
    return htmlLst

def getBillUrlLst(htmlList):
    billURLList = []
    firstHtml = True
    for i in htmlList:
        exists = i.find("/2014/Bills/")
        if exists != -1:
            idxofBeg = i.find("\"")+1
            idxofEnd = i.rfind("\"")
            tmp = i[idxofBeg:idxofEnd]
            if tmp.endswith(".PDF") == False and firstHtml == True:
                billURLList.append(tmp)
                firstHtml = False
                continue
    return billURLList

execfile("tokenize_bill_contents.py")

if __name__ == '__main__':
    #total bills for that category
    totalBills = []
    
    categoryItems = categories.items()
    for c in categoryItems:
        #print(c[0])
        htmlLst = getCategoryHtml(c[0])
        billNumLst = getBillNumLst(htmlLst)
        cate = [c[1]]
        totalBills.append(cate)
        for b in billNumLst:
            billHLst = getBillHtml(b)
            billUrlLst = getBillUrlLst(billHLst)
            totalBills.append(billUrlLst)

    with open("table_data.txt", "w") as f:
        for i in totalBills:
            if  len(i)>0 and i[0].endswith(".HTM")== True:
                tmpi = ''.join(i)
                tmpLst = grabMeasure(tmpi)
                Str1 = '---'.join(tmpLst)
                f.write(Str1+"\n")
            else:
                tmpi = ''.join(i)
                f.write(tmpi+"\n")   
    
