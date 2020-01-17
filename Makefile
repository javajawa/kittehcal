build: out/data.json
	scp $(wildcard out/*.json) griffin.tea-cats.co.uk:/srv/www/tea-cats/calendar/

out/data.json: $(wildcard data/*)
	mkdir -vp $(dir $@)
	clear
	bin/calendar.py

clean:
	rm $(wildcard out/*.json)
