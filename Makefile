MSGS = $(notdir $(wildcard ../scammers/*.msg))
SCAMMERS = $(addprefix static/scammers/, $(MSGS:.msg=.html))

all: html .gazetteer .ipaddress .spam

html: static/new-photos.html static/new-images.html static/stats.html

.FORCE:

# Scammers

static/scammers/%.html: ../scammers/%.msg scammer-html.py templates/scammer.html templates/base-panel.html templates/base.html templates/header.html templates/footer.html templates/social.html
	cat $< | python scammer-html.py > $@

# Photos

static/new-photos.html: templates/base.html templates/new-photos.html .FORCE
	@python make-new-photos.py > $@

# Images

static/new-images.html: templates/base.html templates/new-images.html .FORCE
	@python make-new-images.py > $@

# Statistics

static/stats.html: templates/base.html templates/stats.html make-stats.py .FORCE
	@python make-stats.py > $@

# Gazetteer DB

%.geo: %.txt geoconv.py admin1CodesASCII.txt admin2Codes.txt CountryCodes.csv
	@python geoconv.py $< -o $@

.gazetteer: gaz-update.py allCountries.geo
	@python gaz-update.py allCountries.geo
	@touch $@

# IP Addresses DB

geolite2.txt: ip-geolite2.py GeoLite2-Country-Locations.csv GeoLite2-Country-Blocks-IPv4.csv
	@python ip-geolite2.py -o $@

dbip.txt: ip-dbip.py dbip-country-lite.csv
	@python ip-dbip.py dbip-country-lite.csv -o $@

.ipaddress: ip-update.py geolite2.txt dbip.txt
	@python ip-update.py geolite2.txt dbip.txt
	@touch $@

# Spam keywords

.spam: junk-auto.log junk-reported.log
	@./analyse-junk.sh
	@touch $@

tests: .FORCE
	nosetests tests #--with-coverage
