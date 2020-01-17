build: data.json
	scp *.json griffin.tea-cats.co.uk:/srv/www/tea-cats/calendar/

data.json: calendar holidays tags
	clear
	./calendar.py

clean:
	rm $(wildcard *.json)
