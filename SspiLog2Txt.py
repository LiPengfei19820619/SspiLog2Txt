"""This script file converts sspi soap log sqlite3 database to text file"""

import os
import sys
import getopt
import sqlite3


def dict_factory(cursor, row):
    """dict factory"""
    log = {}
    for idx, col in enumerate(cursor.description):
        log[col[0]] = row[idx]
    return log

def trans_soap_log(inputfile):
    """trans soap log from sqlite3 to text file"""
    filecount = 10
    logcount = 20000

    con = sqlite3.connect(inputfile)
    con.row_factory = dict_factory

    cursor = con.cursor()

    if not os.path.exists("soap_log"):
        os.mkdir("soap_log")

    for fileindex in range(filecount):
        outputfile = r"soap_log\soap_log" + str(fileindex) + ".txt"
        print("write logs to text file: " + outputfile + "\n")

        offset = fileindex * logcount
        sql = "select * from soap_log limit " + str(offset) + "," + str(logcount)
        cursor.execute(sql)
        logs = cursor.fetchall()

        write_logs_to_txt(outputfile, logs)

    con.close()

def write_logs_to_txt(file, logs):
    """wirite log to text file"""
    with open(file, 'a') as logfile:
        for log in logs:
            logfile.write("<" + log["time"] + ">----------->>>From Socket(" + log["serial"] + "), ")
            logfile.write("Client(" + log["ipaddr"] + "), ")
            logfile.write("Soap Buffer Index(0), Recv Msg Is:\n")
            logfile.write("<" + log["time"] + ">" + log["oper_req"].replace("\r\n", "\n") + "\n")

            logfile.write("<" + log["time"] + ">-----------<<<To Socket(" + log["serial"] + "), ")
            logfile.write("Soap Buffer Index(0), Send Msg Is:\n")
            logfile.write("<" + log["time"] + ">" + log["oper_rsp"].replace("\r\n", "\n") + "\n")
        logfile.close()

def main(argv):
    """the main function"""
    inputfile = ''

    try:
        opts, args = getopt.getopt(argv, "hi:", ["ifile="])
    except getopt.GetoptError:
        print('test.py -i <inputfile>')
        sys.exit(2)

    for opt, arg in opts:
        print(opt, ':', arg)
        if opt == '-h':
            print('test.py -i <inputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg

    print('input sqlite3 file：', inputfile)

    trans_soap_log(inputfile)


if __name__ == "__main__":
    main(sys.argv[1:])
