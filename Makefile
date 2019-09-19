MSGS = $(notdir $(wildcard ../scammers/*.msg))
SCAMMERS = $(addprefix static/scammers/, $(MSGS:.msg=.html))

all: static/new-photos.html static/new-images.html static/stats.html spamkeywords.py $(SCAMMERS) gazetteer ipaddress

.FORCE:

# Scammers

static/scammers/%.html: ../scammers/%.msg scammer-html.py templates/scammer.html templates/template-panel.html templates/template.html templates/header.html templates/footer.html templates/social.html
	cat $< | python scammer-html.py > $@

# Photos

static/new-photos.html: templates/template.html templates/new-photos.html .FORCE
	python make-new-photos.py > $@

# Images

static/new-images.html: templates/template.html templates/new-images.html .FORCE
	python make-new-images.py > $@

# Statistics

static/stats.html: templates/template.html templates/stats.html make-stats.py .FORCE
	python make-stats.py > $@

# Gazetteer DB

%.geo: %.txt geoconv.py admin1CodesASCII.txt admin2Codes.txt CountryCodes.csv
	python geoconv.py $< -o $@

gazetteer: gazreset.py allCountries.geo
	python gazreset.py allCountries.geo
	@touch $@

# IP Addresses DB

geolite2.txt: ip-geolite2.py GeoLite2-Country-Locations.csv GeoLite2-Country-Blocks-IPv4.csv
	python ip-geolite2.py -o $@

dbip.txt: ip-dbip.py dbip-country-lite.csv
	python ip-dbip.py dbip-country-lite.csv -o $@

ipaddress: ipreset.py geolite2.txt dbip.txt
	python ipreset.py geolite2.txt dbip.txt
	@touch $@

# Spam Keywords

spamkeywords.py: junk-auto.log junk-reported.log
	./analyse-junk.sh

tests: .FORCE
	nosetests tests #--with-coverage
