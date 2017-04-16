#!/usr/bin/python
import argparse
import gspread
import private
from oauth2client.service_account import ServiceAccountCredentials

INSERT = 'insert'
SEARCH = 'search'

ENCODING = 'encoding'
ASCII = "ascii"
BASE64 = "base64"

def parse_args():
    parser = argparse.ArgumentParser(prog='gspreadpython.py')
    parser.add_argument('-i','--insert', nargs='+', metavar="item")
    parser.add_argument('-s','--search', nargs='+', metavar="keyword")
    parser.add_argument('-e','--encoding', metavar="encoding [ascii|base64] ", choices=[ASCII,BASE64], required=True)
    args = vars(parser.parse_args())
    if not any(args.values()):
        parser.error('No arguments provided.')
    return args

def rank_rows(rows, keywords):
    rows_with_cnt = []

    def get_keywords_cnt(row):
        cnt = 0
        for kw in keywords:
            if kw.lower() in "".join(row).lower(): cnt += 1
        return cnt

    #get rows with keywords cnt > 0, sort in dsc order, remove num of keywords in the tuple
    for row in rows:
        rows_with_cnt.append((row, get_keywords_cnt(row)))
    rows_with_kw_cnt = filter(lambda x:x[1]>0, rows_with_cnt)
    rows_with_kw =map(lambda x:x[0],sorted(rows_with_kw_cnt, reverse=True, key=lambda x:x[1]))
    return rows_with_kw

def is_base64_encoded(s):
    '''
    Not a garrantee even if no exception is raised
    http://stackoverflow.com/a/12315449
    '''
    import binascii
    try:
        s.decode("base64")
        return True
    except binascii.Error:
        return False

def main():
    args = parse_args()

    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name(private.SECRET, scope)
    client = gspread.authorize(creds)
     
    sheet = client.open("gspreaddb").sheet1

    if args[INSERT]:
        #inserting encoding|link_or_cmd|cmd_or_comment|comments(optional)
        if args[ENCODING] == BASE64:
            if is_base64_encoded(args[INSERT][0]):#verify that the fisrt element in -i list should follow the ENCODING
                sheet.append_row([args[ENCODING]] + args[INSERT]) 
            else:
                print "string \033[1m%s\033[0m doesnot match the encoding \033[1m%s\033[0m" % (args[INSERT][0], args[ENCODING])

        else:#ascii encoding
            sheet.append_row([args[ENCODING]] + args[INSERT]) 

    if args[SEARCH]:
        keywords = args[SEARCH]
        rows = sheet.get_all_values()#might become a problem when the sheet gets larger

        rows = filter(lambda row:row[0] == args[ENCODING], rows)

        #decode base64 on the 2nd column (1st column is encoding)
        if args[ENCODING] == BASE64:
            for row in rows:
                row[1] = row[1].decode("base64")

        rows_ranked = rank_rows(rows, keywords)
        for i, row in enumerate(rows_ranked): 
            if i == 0: print "\033[1m"
            row_without_encoding = row[1:]
            print "\n\t".join(row_without_encoding)
            if i == 0: print "\033[0m"

if __name__ == "__main__":
    main() 
