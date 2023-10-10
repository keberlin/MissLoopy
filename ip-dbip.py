import argparse
import csv

parser = argparse.ArgumentParser(description="Convert dbip IP Address csv File.")
parser.add_argument("file", nargs="+", help="a file for conversion")
parser.add_argument("-o", metavar="output", nargs=1, required=True, help="output file")
args = parser.parse_args()


def IpNumber(ip):
    s = ip.split(".")
    if len(s) < 4:
        raise Exception("Invalid IP address")
    return (int(s[0]) << 24) + (int(s[1]) << 16) + (int(s[2]) << 8) + int(s[3])


with open(args.o[0], "wb") as output:
    writer = csv.writer(output, delimiter=",")

    for file in args.file:
        print("Processing", file)
        with open(file, "rb") as csvfile:
            reader = csv.reader(csvfile, delimiter=",", skipinitialspace=True)
            for row in reader:
                # Ignore IPv6 rows
                if row[0].find(":") != -1:
                    continue
                # Ignore any unknown countries
                if row[2] == "":
                    continue
                writer.writerow([IpNumber(row[0]), IpNumber(row[1]), row[2]])
