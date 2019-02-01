days_in_month = {
	'01':'31',
	'02':'28',
	'03':'31',
	'04':'30',
	'05':'31',
	'06':'30',
	'07':'31',
	'08':'31',
	'09':'30',
	'10':'31',
	'11':'30',
	'12':'31'
	}

def begin_month(x,y):
	month = x
	year = y[2:]
	if len(x) < 2:
		month = '0' + x
	return ('%s%s%s' % (year,month,'01'))

def last_month(x,y):
	month = x
	year = y[2:]
	if len(x) < 2:
		month = '0' + x
	day = days_in_month[month]
	if int(year) % 4 == 0 and month == '02':
		day = '29'
	return ('%s%s%s' % (year, month, day))
	
def year_month(x,y):
	month = x
	year = y[2:]
	if len(x) < 2:
		month = '0' + x
	return ('%s%s' % (year, month))