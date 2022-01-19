import argparse
import csv
import os
import config
from ReportMaker.Reporter import Reporter


def handle_args():
    """
    Handles all arguments when executing the code using a parser

    @return: parser arguments and the parser itself
    """
    parser = argparse.ArgumentParser(description='Resource Reporter')
    parser.add_argument('-i', '--input', dest='input_path', help='Input location of csv exports', required=True)
    parser.add_argument('-o', '--output', dest='output_path', help='Output location and filename', required=True)

    return parser.parse_args(), parser

def get_files(path):
    files = []
    filenames = []
    for filename in os.listdir(path):
        if filename.endswith(".csv"):
            filenames.append(filename)
            files.append(os.path.join(path, filename))

    return files,filenames

def main():
    arguments, parser = handle_args()
    data_files,filenames = get_files(arguments.input_path)
    reporter = Reporter()
    for file_path,filename in zip(data_files,filenames):
        reporter.write(file_path,filename)

    if not os.path.exists(config.OUTPUT_DIR):
        os.mkdir(config.OUTPUT_DIR)
    path = os.path.join(config.OUTPUT_DIR,arguments.output_path)
    reporter.save(path)

main()