import sys, getopt
import sqlite3

def dict_factory(cursor, row): 
    d = {} 
    for idx, col in enumerate(cursor.description): 
        d[col[0]] = row[idx] 
    return d

def write_log_to_txt(file, log):
    with open(file, 'a') as f:
        f.write("<"+log["time"]+">----------->>>Recv Msg Is:\n")
        f.write("<"+log["time"]+">"+log["oper_req"]+"\n")
        f.write("<"+log["time"]+"-----------<<<Send Msg Is::\n")
        f.write("<"+log["time"]+">"+log["oper_rsp"]+"\n")
        f.close()

def main(argv):
    inputfile = ''
    outputfile = ''

    try:
        opts, args = getopt.getopt(argv, "h:i:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print('test.py -i <inputfile> -o <outputfile>')
        sys.exit(2)

    for opt, arg in opts:
        print(opt, ':', arg)
        if opt == '-h':
            print('test.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
    
    print('输入的文件：', inputfile)
    print('输出的文件：', outputfile)

    con = sqlite3.connect(inputfile);
    con.row_factory = dict_factory
    #2、创建数据游标
    cursor = con.cursor()
    #3、执行一些SQL操作
    cursor.execute("""select * from soap_log""")
    logs = cursor.fetchall()
    for log in logs:
        write_log_to_txt(outputfile, log)
    
    con.close()

if __name__ == "__main__":
    main(sys.argv[1:])

