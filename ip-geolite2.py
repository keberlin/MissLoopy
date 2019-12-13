import argparse, csv

parser = argparse.ArgumentParser(description='Convert dbip IP Address csv File.')
parser.add_argument('-o', metavar='output', nargs=1, required=True, help='output file')
args = parser.parse_args()

def IpNumber(ip):
  s = ip.split('.')
  if len(s) < 4:
    raise Exception('Invalid IP address')
  return (int(s[0])<<24)+(int(s[1])<<16)+(int(s[2])<<8)+int(s[3])

with open(args.o[0], 'wb') as output:
  writer = csv.writer(output, delimiter=',')

  geonames = {}
  with open('GeoLite2-Country-Locations.csv','rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', skipinitialspace=True)
    first = True
    for row in reader:
      if first:
        first = False
        continue
      continent = row[3]
      country = row[4]
      geonames[row[0]] = country if country else continent

  with open('GeoLite2-Country-Blocks-IPv4.csv','rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', skipinitialspace=True)
    first = True
    for row in reader:
      if first:
        first = False
        continue
      ip = row[0]
      pos = ip.find('/')
      lower = IpNumber(ip[:pos])
      upper = lower + int(ip[pos+1:])
      country1 = row[1]
      country2 = row[2]
      if not country1 and not country2:
        print 'Ignoring:', row
        continue
      country = geonames[country2 if country2 else country1]
      writer.writerow([lower, upper, country])
