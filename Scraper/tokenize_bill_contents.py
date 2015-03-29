'''
Bugs listed below
billNumber, synopsis, sponsors, sponsorDistrict, statement, URL

BillNumber actual output = "ASSEMBLY, No.3064"
BillNumber Expected output = "3064"

Synopsis actual output = "    &nbsp;    "
Synopsis expected output = "Repeals anachronistic, superseded, or invalidated sections of statutory law."

sponsor actual = 'Assemblyman VINCENT MAZZEO\r\n\r\n'
sponsor expected = 'Assemblyman VINCENT MAZZEO'

sponsorDistrict -> Correct

statement -> Has unwanted strings like "&nbsp"

URL -> Correct
'''
def stripSpecials(string2strip):
    import re
    string2strip = re.sub(r'(?ms)\xA0',r'',string2strip)         # crossbar characters
    return string2strip

def stripClosingTag(string2strip):
    import re
    string2strip = re.sub(r'(?ms)<\x2f.{1,9}>',r'',string2strip) # closing tags 
    return string2strip

def stripMostTags(string2strip):
    import re
    string2strip = re.sub(r'(?ms)<.{1,129}>',r'',string2strip)   # other tags
    return string2strip

def undoSoftWrap(string2unwrap):
    import re
    string2unwrap = re.sub(r'(?ms)\n\x20',r"XA0GRAFX0A",string2unwrap) # anchor true graf
    string2unwrap = re.sub(r'(?ms)\n',r' ',string2unwrap)          # remove soft wraps
    string2unwrap = re.sub(r'(?ms)\r',r' ',string2unwrap)          # remove soft wraps
    string2unwrap = re.sub(r'(?ms)XA0GRAFX0A',r'\n',string2unwrap) # restore true grafs
    return string2unwrap


def grabMeasure(URL):
    import urllib
    import re
    grabbedLines = ''
    prefixURL = 'http://www.njleg.state.nj.us'
    URL = prefixURL + URL 
    numbersLink=urllib.urlopen(URL)
    rawHTMLbill = numbersLink.read()

    statement = rawHTMLbill
    synopsis = rawHTMLbill
    sponsors = rawHTMLbill
    billNumber = rawHTMLbill

    statement = re.sub(r'(?ms)(.*>)STATEMENT(.*)',r'\2',statement)
    statement = re.sub(r'(?ms)(.*>).nbsp.(.*)',r'\1\2',statement)
    statement = stripSpecials(statement)
    statement = stripClosingTag(statement)
    statement = stripMostTags(statement)
    statement = undoSoftWrap(statement)

    synopsis = re.sub(r'(?ms).*?SYNOPSIS(.*?)CURRENT VERSION.*',r'\1',synopsis)
    synopsis = stripSpecials(synopsis)
    synopsis = stripClosingTag(synopsis)
    synopsis = stripMostTags(synopsis)
    synopsis = undoSoftWrap(synopsis)

    sponsors = re.sub(r'(?ms).*(<div class.Section2.*?<.div>).*',r'\1',sponsors)
    sponsors = re.sub(r'(?ms).*?Sponsored by.*?bpuSponsor>(.*?)<.p>',r'\1',sponsors)

    sponsorDistrict = re.sub(r'(?ms).*(District \d*).*',r'\1',sponsors)
    sponsors = re.sub(r'(?ms)(.*?)<p.*',r'\1',sponsors)
    sponsors = stripSpecials(sponsors)

    billNumber = re.sub(r'(?ms).*(<p.class.bpuBill.*?<.p>).*',r'\1',billNumber)
    billNumber = stripClosingTag(billNumber)
    billNumber = stripMostTags(billNumber)

    return billNumber, synopsis, sponsors, sponsorDistrict, statement, URL

#lprint grabLines('S0500/354_I1.HTM')
#print grabLines('A0500/102_I1.HTM')
