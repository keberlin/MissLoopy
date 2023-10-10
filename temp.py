import csv

with open("bannedips.csv", "rb") as csvfile:
    lower = ""
    upper = ""
    country = ""
    reader = csv.reader(csvfile, delimiter=";", skipinitialspace=True)
    for row in reader:
        if row[0] == lower and row[1] == upper and row[2] != country:
            print(row)
        lower = row[0]
        upper = row[1]
        country = row[2]
