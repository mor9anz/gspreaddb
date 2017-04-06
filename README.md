# gspreaddb
Google Spreadsheets and Python 
https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html

gspread API Reference http://gspread.readthedocs.io/en/latest/

#Format
Encoding|link\_or\_cmd|cmd\_or\_comment|comment(optional)

#Dependencies
pip install --user -r requirements.txt

#Sample usage:
`gspreadpython.py -e ascii -i "sudo apt-get install libffi-dev" "http://stackoverflow.com/questions/12982486/glib-compile-error-ffi-h-but-libffi-is-installed/17518165#17518165" "fatal error: ffi.h: No such file or directory"`

`gspreadpython.py -e ascii -s ffi.h`

To get one line base64: `cat gspreadpython.py | base64 | tr -d '\n'`
