import argparse
import csv
import os
import config
from reporter.Reporter import Reporter
import pathlib



def handle_args():
    """
    Handles all arguments when executing the code using a parser

    @return: parser arguments and the parser itself
    """
    parser = argparse.ArgumentParser(description='Resource Reporter')
    parser.add_argument('-i', '--input', dest='input_path', help='Input location of csv exports', required=True)
    parser.add_argument('-o', '--output', dest='output_filename', help='Output filename of excel report', required=True)

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

    output_path = os.path.join(pathlib.Path(__file__).parent.parent.resolve(),config.OUTPUT_DIR)
    if not os.path.exists(output_path):
        os.mkdir(output_path)

    path = os.path.join(output_path,arguments.output_filename)
    reporter.save(path)

main()