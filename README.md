# runtrainer.com_export_to_gpx
Exports all your runs from runtrainer.com to separate gpx files.

## Prerequisites

For this to work you need the following packages:

[Scrappy](http://scrapy.org/)
[gpxpy -- GPX file parser](https://github.com/tkrajina/gpxpy)
[SRTM.py](https://github.com/tkrajina/srtm.py) (however not used at the moment)

## How to run

Clone this repositry and run it with scrappy

```
$ scrapy crawl runtrainer -a user=<username> -a password=<your_password>
```

It writes all your activities to separate gpx files. Those files can be uploaded to:
[Strava](http://strava.com)
[Runtastic](http://www.runtastic.com)

Probably also other, however I only tested those two

## License

This Scrapy spider is licensed under the [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0)

