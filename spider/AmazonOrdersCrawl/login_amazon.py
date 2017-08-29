from AmazonManagerOrderCrawlFromOrderID import AmazonOrderManagerCrawlFromAsin_
from datetime import datetime
import pymysql
def amazon_login(zone):
	amzCrawl = AmazonOrderManagerCrawlFromAsin_(zone, 200)

	amzCrawl.dbconn = pymysql.connect(
            host="192.168.2.97",
			database="bi_system",
			user="lepython",
			password="qaz123456",
			port=3306,
			charset='utf8'
		)
	amzCrawl.cur = amzCrawl.dbconn.cursor()

	amzCrawl.url,amzCrawl.username,amzCrawl.password=amzCrawl.get_login_info()
	amzCrawl.cur.close()
	amzCrawl.dbconn.close()
	driver=amzCrawl.open_browser()
	driver.get(amzCrawl.url)
	amzCrawl.login(driver)

if __name__=="__main__":
	zone="CA"
	amazon_login(zone)
