from sunlight import openstates
from sunlight import config

import pymysql.cursors

L = []

def saveBill():
	with connection.cursor() as cursor:
        # Read a single record
		sql = "SELECT `C_ID`, `Name` FROM `category` ORDER BY `Name`"
		cursor.execute(sql)
	for row in cursor:
		print(row)
		
def getBills(category):
	if category != 'Other':
		print "Working on bills for category " + category
		global L
		config.API_KEY = 'bb78fe7f326944e0919fd4fafc778146'
		vt_agro_bills = openstates.bills(q=category,state='nj')
		for bill in vt_agro_bills:
			if bill['id'] not in L:
				L.append(bill['bill_id'])
			
def main():
	# Connect to the database
	connection = pymysql.connect(host='localhost',
								 user='root',
								 passwd='engauge',
								 db='hackjersey',
								 charset='utf8mb4',
								 cursorclass=pymysql.cursors.DictCursor)

	try:
		global L
		with connection.cursor() as cursor:
			# Read a single record
			sql = "SELECT `C_ID`, `Name` FROM `category` ORDER BY `Name`"
			cursor.execute(sql)
		for row in cursor:
			getBills(row['Name'])	
		print L
	finally:
		connection.close()

if __name__ == "__main__":
	main()
	
