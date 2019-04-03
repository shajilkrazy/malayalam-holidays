from datetime import datetime
import sys, os

class myevent():
	def __init__(self, text_line, year):
		from datetime import datetime, timedelta
		z = text_line.split(' : ')
		x = z[0].split('-')
		date = datetime(int(year), int(x[0]), int(x[1]))
		self.name = z[1]
		self.datestart = date.strftime('%Y%m%d')
		self.dateend = (date + timedelta(1)).strftime('%Y%m%d')

def txt_process(file_name, year):
	f = open(file_name)
	s = f.read()
	f.close()
	while s[-1] == '\n':
		s = s[:-1]
	events = s.split('\n')
	events_list = []
	for event in events:
		m = myevent(event, year)
		events_list.append(m)
	return events_list

def year_process(file_name):
	dtstamp = datetime.now().strftime('%Y%m%dT%H%M%SZ')
	year = os.path.splitext(os.path.basename(file_name))[0]
	spec_events = txt_process(file_name, year)
	common_events = txt_process('data/common',year)
	yearly_events = common_events + spec_events
	f = open("Malayalam Holidays-%s.ics"%(year),'w')
	f.write("BEGIN:VCALENDAR\nVERSION:2.0\nCALSCALE:GREGORIAN\nMETHOD:PUBLISH\nX-WR-CALNAME:Malayalam Holidays\nX-WR-TIMEZONE:Asia/Kolkata\nBEGIN:VTIMEZONE\nTZID:Asia/Kolkata\nX-LIC-LOCATION:Asia/Kolkata\nBEGIN:STANDARD\nTZOFFSETFROM:+0530\nTZOFFSETTO:+0530\nTZNAME:IST\nDTSTART:19700101T000000\nEND:STANDARD\nEND:VTIMEZONE")
	for event in yearly_events:
		f.write("\nBEGIN:VEVENT\nDTSTART;VALUE=DATE:%s\nDTEND;VALUE=DATE:%s\nDTSTAMP:%s\nSUMMARY:%s\nEND:VEVENT"%(event.datestart, event.dateend, dtstamp, event.name))
	f.write("\nEND:VCALENDAR")
	f.close()

def main():
	try:
		years = []
		for year in sys.argv[1:]:
			years.append(int(year))
	except ValueError:
		print("Usage: python calender.py [years1] [year2]...")
		print("\te.g: python calender.py\t- Processes all available calendars.")
		print("\tor: python calender.py 2019 2018\t- Processes calendars of years 2019 and 2018.")
		quit()
	if len(years) == 0:
		from glob import glob
		file_list = glob('data/*.txt')
	else:
		file_list = []
		for year in years:
			file_list.append("data/%d.txt"%(year))
	for file_name in file_list:
		try:
			year_process(file_name)
		except FileNotFoundError:
			print('Calendar data not available for year %s'%(os.path.splitext(os.path.basename(file_name))[0]))
	print("\nCalendar generation completed!")

if __name__ == '__main__':
	main()
