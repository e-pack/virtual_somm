#https://schedule.readthedocs.io/en/stable/


# import schedule
# import time
# import bad_saint

# def job(t):
#     print "I'm working...", t
#     return

# schedule.every().day.at("01:00").do(job,'It is 01:00')

# while True:
#     schedule.run_pending()




import schedule
import time
import bad_saint

def run_badsaint():
	python bad_saint

def job():
	run_badsaint
    print(len(numberofreservations))

schedule.every().minute.at(":17").do(job)

while True:
    schedule.run_pending()
