from sunlight import openstates
from sunlight import config

import pymysql.cursors

connection = pymysql.connect(host='localhost',
							 user='root',
							 passwd='engauge',
							 db='hackjersey',
							 charset='utf8mb4',
							 cursorclass=pymysql.cursors.DictCursor)
def saveLegislator(legislator):
	print "Writing legislator " + legislator['full_name'] + " to db" 
	global connection
	with connection.cursor() as cursor:
		sql = "INSERT INTO `Legislator` (`L_ID`, `openstates_ID`, `full_name`, `first_name`, `middle_name`, `last_name`, `suffixes`, `state`, `active`, `chamber`, `district`, `party`, `url`, `photo_url`, `email`, `created_at`, `updated_at`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
		cursor.execute(sql, (legislator['leg_id'],legislator['full_name'],legislator['first_name'],legislator['middle_name'],legislator['last_name'],legislator['suffixes'],legislator['state'],legislator['active'],legislator['chamber'],legislator['district'],legislator['party'],legislator['url'],legislator['photo_url'],legislator['email'],legislator['created_at'],legislator['updated_at'] ))
		
def getLegislators(state1):
	print "Working on legislators for " + state1
	config.API_KEY = 'bb78fe7f326944e0919fd4fafc778146'
	agro_legislators = openstates.legislators(state=state1)
	for legislator in agro_legislators:
		saveLegislator(legislator)
		
def main():
	global connection
	getLegislators('nj')
	connection.commit()


if __name__ == "__main__":
	main()
	
