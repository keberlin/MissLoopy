import argparse
import csv

from gazetteer import *

MIN_POPULATION = 2000

parser = argparse.ArgumentParser(description="Create Geographical Gazetteer Database.")
parser.add_argument("file", nargs="+", help="a file for conversion")
parser.add_argument("-o", metavar="output", nargs=1, required=True, help="output file")
args = parser.parse_args()

with open(args.o[0], "wb") as output:
    writer = csv.writer(output, delimiter=";")

    mult_x = CIRCUM_X / 360.0
    mult_y = CIRCUM_Y / 360.0

    # Load the country table
    countries = {}
    with open("CountryCodes.csv", "rb") as csvfile:
        reader = csv.reader(csvfile, delimiter=",", quoting=csv.QUOTE_NONE, skipinitialspace=True)
        for row in reader:
            countries[row[0]] = row[1]

    # Load the region admin table
    admin = {}
    with open("admin1CodesASCII.txt", "rb") as csvfile:
        reader = csv.reader(csvfile, delimiter="\t", quoting=csv.QUOTE_NONE)
        for row in reader:
            admin[row[0]] = row[1]
    with open("admin2Codes.txt", "rb") as csvfile:
        reader = csv.reader(csvfile, delimiter="\t", quoting=csv.QUOTE_NONE)
        for row in reader:
            admin[row[0]] = row[1]

    def Region(code):
        if code in admin:
            return admin[code]
        return None

    def CountryCode(row):
        return countries[row[8]]

    def OutputRow(row):
        location = re.sub(r",.*", r"", row[1])  # Needed for Washington DC!
        reg3 = Region(row[8] + "." + row[10] + "." + row[11])
        if reg3:
            location += ", " + reg3
        reg2 = Region(row[8] + "." + row[10])
        if reg2:
            location += ", " + reg2
        location += ", " + CountryCode(row)
        # Remove any duplicate region names i.e. Oslo, Oslo, Oslo, Norway
        location = re.sub(r"(?P<name>[^,]+, )((?P=name))+", r"\g<name>", location)
        out = [location, int(float(row[5]) * mult_x), int(float(row[4]) * mult_y), row[17], row[14]]
        writer.writerow(out)

    for file in args.file:
        print("Processing", file)
        with open(file, "rb") as csvfile:
            reader = csv.reader(csvfile, delimiter="\t", quoting=csv.QUOTE_NONE, skipinitialspace=True)
            for row in reader:
                if row[8] == "US":
                    if (
                        row[6] == "P"
                        and row[7].startswith("PPL")
                        and row[7] != "PPLX"
                        and int(row[14]) > MIN_POPULATION
                    ):
                        if row[1].find("(balance)") != -1 or row[1].find("(Balance)") != -1:
                            continue
                        OutputRow(row)
                    continue
                elif row[8] == "GB":
                    if row[11] == "GLA":  # Special handling for Greater London Area
                        if row[6] == "A" and row[7] == "ADM3":
                            OutputRow(row)
                        elif row[6] == "P" and row[7] in ["PPLC", "PPLX"]:
                            OutputRow(row)
                    elif (
                        row[6] == "P"
                        and row[7].startswith("PPL")
                        and row[7] != "PPLX"
                        and int(row[14]) > MIN_POPULATION
                    ):
                        OutputRow(row)
                    continue
                elif row[8] == "FR" and row[11] == "75":  # Special handling for Paris
                    if row[6] == "P" and row[7] == "PPLX":
                        OutputRow(row)
                    elif row[6] == "P" and row[7] == "PPLC":
                        OutputRow(row)
                    continue
                if row[6] == "P" and row[7].startswith("PPL") and row[7] != "PPLX" and int(row[14]) > MIN_POPULATION:
                    OutputRow(row)

    print("Output written to", output.name)
