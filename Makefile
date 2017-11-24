MSGS = $(notdir $(wildcard ../scammers/*.msg))
SCAMMERS = $(addprefix static/scammers/, $(MSGS:.msg=.html))

all: static/photos.html static/images.html spamkeywords.py $(SCAMMERS) gazetteer ipaddress

.FORCE:

# Scammers

static/scammers/%.html: ../scammers/%.msg scammer-html.py templates/scammer.html templates/template-panel.html templates/template.html templates/header.html templates/footer.html templates/social.html
	cat $< | ./scammer-html.py > $@

# Photos

static/photos.html: templates/template.html templates/static.html static.cgi .FORCE
	python list-new-photos.py | awk 'BEGIN {printf "<table>\n";} {if (n++%12==0) {printf "<tr>\n";} printf "<td align=\"center\"><a href=\"member?id=%s\"><img width=\"100px\" src=\"static/%s\"><br>%s</a></td>\n",$$1,$$2,$$1;} END {printf "</table>";}' | ./static.cgi -s 'Photos' > $@

# Images

static/images.html: templates/template.html templates/static.html static.cgi .FORCE
	python list-new-images.py | awk 'BEGIN {printf "<table>\n";} {if (n++%12==0) {printf "<tr>\n";} printf "<td align=\"center\"><img width=\"100px\" src=\"%s\"><br>%s</td>\n",$$2,$$1;} END {printf "</table>";}' | ./static.cgi -s 'Images' > $@

# Gazetteer DB

%.geo: %.txt geoconv.py admin1CodesASCII.txt admin2Codes.txt CountryCodes.csv
	./geoconv.py $< -o $@

gazetteer: gazreset.py allCountries.geo
	./gazreset.py allCountries.geo
	@touch $@

# IP Addresses DB

geolite2.txt: ip-geolite2.py GeoLite2-Country-Locations.csv GeoLite2-Country-Blocks-IPv4.csv
	./ip-geolite2.py -o $@

dbip.txt: ip-dbip.py dbip-country.csv
	./ip-dbip.py dbip-country.csv -o $@

ipaddress: ipreset.py geolite2.txt dbip.txt
	./ipreset.py geolite2.txt dbip.txt
	@touch $@

# Spam Keywords

spamkeywords.py: junk-auto.log junk-reported.log
	./analyse-junk.sh

tests: .FORCE
	nosetests #--with-coverage
