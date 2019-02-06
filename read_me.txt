# --- MSR File Generator READ ME --- #

1. Requirements:
	-Python 2.7.x

2. Usage instructions:
	2.1 - Before running the MSR File Generator, we need the proper supporting files. In Foothold, download the proper reports (2 profile, 2 services):
	
	For Profile Data:
	-Navigate to the Demographics Report Builder and select program (Vermont CRT or Vermont FFS)
	-Select appropriate date range (Spanning the month for which we're running the report)
	-Check the checkbox labelled "Provide ExportBuilder Options"
	-From "Select a saved export format" select "TK's MSR Demographic Data Export 0.1"
	-Uncheck the checkbox labelled "Provide option to modify settings o saved export format"
	-Click "Continue"
	-Click the "Download CSV file" link in the top center of the screen
	-Rename downloaded file in this format: [program]profile[month][year] (for example: a CRT file from December, 2018 would look like crtprofile1218)
	-Perform those same steps again for the other set of data (CRT or FFS, whichever you didn't choose first!)

	For Services Data:
	-Navigate to the Service Contacts Report Builder
	-Select program (Vermont CRT or Vermont FFS)
	-Select appropriate date range for "Roster Date Range" and "Services Dates"(Spanning the month for which we're running the report)
	-Check the checkbox labelled "Provide ExportBuilder Options"
	-From "Select a saved export format" select "TK's MSR Service Report 3.0"
	-Click the "Download CSV file" link in the top center of the screen
	-Rename downloaded file in this format: [program]services[month][year] (for example: an FFS file from July, 2018 would look like ffsservices0718)
	-Perform those same steps again for the other set of data (CRT or FFS, whichever you didn't choose first!)
		
	2.2 - Open a command prompt and navigate to the MSR folder which contains our program
		Example: if your folder is on your desktop, at the console type "cd desktop/msr" (you can leave out the quotes)
	2.3 - While in a command prompt, within your MSR folder, type the command "python app.py" to run the program

	2.4 - Your first step with the program is to run a profile check, if you're not sure about the integrity of your data (Always run one first!) -- follow the prompts on the console and you'll receive a report of which service recipients have problematic data. Go back to Foothold and correct this (yawn, I know!) -- then re-download the profile data for that particular program affected by individual(s). 

	2.5 - Presuming we've checked our profile data and it looks good, let's run the program again and choose to run the "MSR file writer" this time! Follow the console prompts and your file will be written
	
3. Support:
	Contact Tom Kimball, tomk@pathwaysvermont.org with questions or to report bugs.