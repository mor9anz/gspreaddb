#!/usr/bin/python
import argparse
import gspread
import private
from oauth2client.service_account import ServiceAccountCredentials

INSERT = 'insert'
SEARCH = 'search'

def parse_args():
    parser = argparse.ArgumentParser(prog='gspreadpython.py')
    parser.add_argument('-i','--insert', nargs='+', metavar="item")
    parser.add_argument('-s','--search', nargs='+', metavar="keyword")
    args = vars(parser.parse_args())
    if not any(args.values()):
        parser.error('No arguments provided.')
    return args

def main():
    args = parse_args()

    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name(private.SECRET, scope)
    client = gspread.authorize(creds)
     
    sheet = client.open("gspreaddb").sheet1

    if args[INSERT]:
        sheet.insert_row(args[INSERT])
    if args[SEARCH]:
        keywords = args[SEARCH]
        rows = sheet.get_all_values()
        for row in rows:
            if filter(lambda x:x in "".join(row), keywords):
                print "\n\t".join(row)

if __name__ == "__main__":
    main() 
