MSGS = $(notdir $(wildcard ../scammers/*.msg))
SCAMMERS = $(addprefix static/scammers/, $(MSGS:.msg=.html))

all: static/new-photos.html static/new-images.html static/stats.html spamkeywords.py $(SCAMMERS) gazetteer ipaddress

.FORCE:

# Scammers

static/scammers/%.html: ../scammers/%.msg scammer-html.py templates/scammer.html templates/template-panel.html templates/template.html templates/header.html templates/footer.html templates/social.html
	cat $< | /usr/local/bin/python2.7 scammer-html.py > $@

# Photos

static/new-photos.html: templates/template.html templates/new-photos.html .FORCE
	/usr/local/bin/python2.7 make-new-photos.py > $@

# Images

static/new-images.html: templates/template.html templates/new-images.html .FORCE
	/usr/local/bin/python2.7 make-new-images.py > $@

# Statistics

static/stats.html: templates/template.html templates/stats.html make-stats.py .FORCE
	/usr/local/bin/python2.7 make-stats.py > $@

# Gazetteer DB

%.geo: %.txt geoconv.py admin1CodesASCII.txt admin2Codes.txt CountryCodes.csv
	/usr/local/bin/python2.7 geoconv.py $< -o $@

gazetteer: gazreset.py allCountries.geo
	/usr/local/bin/python2.7 gazreset.py allCountries.geo
	@touch $@

# IP Addresses DB

geolite2.txt: ip-geolite2.py GeoLite2-Country-Locations.csv GeoLite2-Country-Blocks-IPv4.csv
	/usr/local/bin/python2.7 ip-geolite2.py -o $@

dbip.txt: ip-dbip.py dbip-country-lite.csv
	/usr/local/bin/python2.7 ip-dbip.py dbip-country-lite.csv -o $@

ipaddress: ipreset.py geolite2.txt dbip.txt
	/usr/local/bin/python2.7 ipreset.py geolite2.txt dbip.txt
	@touch $@

# Spam Keywords

spamkeywords.py: junk-auto.log junk-reported.log
	./analyse-junk.sh

tests: .FORCE
	nosetests #--with-coverage
