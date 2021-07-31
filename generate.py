import os
import sys, argparse

class myevent():
	from datetime import datetime, timedelta
	t = datetime.now()
	dtstamp = t.strftime('%Y%m%dT%H%M%SZ')
	uu = int(t.strftime('%Y%j%H%M%S'))
	def __init__(self, text_line, year):
		z = text_line.split(' : ')
		x = z[0].split('-')
		date = myevent.datetime(int(year), int(x[0]), int(x[1]))
		self.name = z[1]
		self.datestart = date.strftime('%Y%m%d')
		self.dateend = (date + myevent.timedelta(1)).strftime('%Y%m%d')
		self.uid = "%s@github.com/shajilkrazy"%(hex(self.uu)[2:])
		myevent.uu += 1

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

def year_process(file_name, file_suffix):
	import re
	year = re.findall(r'\d{4}', file_name)[0]
	common_events = txt_process(f'data/common{file_suffix}',year)
	spec_events = txt_process(file_name, year)
	yearly_events = common_events + spec_events
	f = open(f"Malayalam_Holidays_{year}{file_suffix}.ics",'w')
	f.write("BEGIN:VCALENDAR\nVERSION:2.0\nCALSCALE:GREGORIAN\nMETHOD:PUBLISH\nPRODID:-//Malayalam//Holidays//ML\nX-WR-CALNAME:Malayalam Holidays\nX-WR-TIMEZONE:Asia/Kolkata\nBEGIN:VTIMEZONE\nTZID:Asia/Kolkata\nX-LIC-LOCATION:Asia/Kolkata\nBEGIN:STANDARD\nTZOFFSETFROM:+0530\nTZOFFSETTO:+0530\nTZNAME:IST\nDTSTART:19700101T000000\nEND:STANDARD\nEND:VTIMEZONE")
	for event in yearly_events:
		f.write("\nBEGIN:VEVENT\nDTSTART;VALUE=DATE:%s\nDTEND;VALUE=DATE:%s\nDTSTAMP:%s\nSUMMARY:%s\nUID:%s\nEND:VEVENT"%(event.datestart, event.dateend, event.dtstamp, event.name,event.uid))
	f.write("\nEND:VCALENDAR")
	f.close()

def main():
	languages = {'eng': {'file_suffix':'_eng'}, 'mal': {'file_suffix': ''}}
	description = "Generate iCal (.ics) files of Holidays in Kerala in Malayalam/English."

	parser = argparse.ArgumentParser(description=description)
	parser.add_argument("-y", "--year", type=int, nargs="+", default=None,
					help="calendar year to be generated")
	parser.add_argument("-l","--language", default='mal',
                    help=f"language of the calendar output. Use from {languages.keys()}")
	args = parser.parse_args()

	if args.language not in languages.keys():
		parser.error(f'-l language should be chosen from {languages.keys()}')
		return

	file_suffix = languages[args.language]["file_suffix"]
	if args.year is None:
		from glob import glob
		file_list = glob(f'data/*{file_suffix}.txt')
	else:
		import re
		file_list = []
		for year in args.year:
			file_list.append(f"data/{year}{file_suffix}.txt")
	for file_name in file_list:
		try:
			year_process(file_name, file_suffix)
		except FileNotFoundError:
			print('Calendar data not available for year %s'%(os.path.splitext(os.path.basename(file_name))[0]))
	print("\nCalendar generation completed!")

if __name__ == '__main__':
	main()
