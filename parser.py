import re
import os
import gzip
import sys

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)

def parse_file(filename):
    with open(filename, 'r') as in_file:
        stend = []
        lines = []
        start = 0
        middle = 0
        end = 0
        for idx, line in enumerate(in_file):
            if re.match(".*\d{4}-\d{2}-\d{2}.*", line.strip()):
                start = idx
            if re.match("<ReceiptDate/>", line.strip()) or re.match("></ReceiptDate", line.strip()):
                middle = idx
            if re.match(".*\[system-akka.*", line.strip()):
                end = idx
            if start < middle and middle < end:
                stend.append((start, end))
        chunks = []
        if len(stend) > 0:
            with open(filename) as f:
                content = f.readlines()
                for item in stend:
                    chunk = content[item[0]:item[1]+1]
                    chunks.extend(chunk)
            fh = open("./extracted/" + filename + ".txt", "w")
            fh.writelines(chunks)
            fh.close()
            print(filename)
            
def parse_folder():
    for filename in os.listdir(os.getcwd()):
        if filename.endswith(".log") and filename.startswith("backend"):
            parse_file(filename)
            
if __name__ == "__main__":
    createFolder('./extracted/')
    try:
        print("Parsing file: ")
        parse_file(sys.argv[1])
    except IndexError:
        print("Parsing files in current folder: ")
        parse_folder() 