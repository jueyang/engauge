categories=["EDUCATION", "CURRICULA", "ENVIRONMENT"]

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
    for i in htmlList:
        exists = i.find("/2014/Bills/")
        if exists != -1:
            idxofBeg = i.find("\"")+1
            idxofEnd = i.rfind("\"")
            tmp = i[idxofBeg:idxofEnd]
            if tmp.endswith(".PDF") == False:
                tmp = "http://www.njleg.state.nj.us"+tmp
                billURLList.append(tmp)
    return billURLList

if __name__ == '__main__':
    #total bills for that category
    totalBills = []

    for c in categories:
        htmlLst = getCategoryHtml(c)
        billNumLst = getBillNumLst(htmlLst)
        totalBills.append("Start Category Bill URLs")
        for b in billNumLst:
            billHLst = getBillHtml(b)
            billUrlLst = getBillUrlLst(billHLst)
            totalBills.append(billUrlLst)
    for t in totalBills:
        print(t)
