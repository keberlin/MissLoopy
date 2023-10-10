import argparse
import csv

parser = argparse.ArgumentParser(description="Convert GeoIp IP Address csv File.")
parser.add_argument("file", nargs="+", help="a file for conversion")
parser.add_argument("-o", metavar="output", nargs=1, required=True, help="output file")
args = parser.parse_args()

with open(args.o[0], "w") as output:
    writer = csv.writer(output, delimiter=";")

    for file in args.file:
        print("Processing", file)
        with open(file, "r") as csvfile:
            reader = csv.reader(csvfile, delimiter=",", skipinitialspace=True)
            for row in reader:
                writer.writerow([int(row[2]), int(row[3]), row[4]])
