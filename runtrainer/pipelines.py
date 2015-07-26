# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import srtm as mod_srtm
import gpxpy
import gpxpy.gpx
from datetime import datetime,timedelta,time

def seconds(dhms):
    """Convert a time string "[[[DD:]HH:]MM:]SS" to seconds.
    """
    components = [int(i) for i in dhms.split(':')]
    pad = 4 - len(components)
    if pad < 0:
        raise ValueError('Too many components to match [[[DD:]HH:]MM:]SS')
    components = [0] * pad + components
    return sum(i * j for i, j in zip((86400, 3600, 60, 1), components))

class RuntrainerPipeline(object):
    def process_item(self, item, spider):
        return item

class GpxFileOutput(object):
     def process_item(self, item, spider):
       
        #start time is always on the day at 12:00
        start_time = datetime.strptime(item["date"], '%d-%B-%Y')
        start_time = start_time + timedelta(hours=12)
        
        #Create time object from duration
        #print "duration %s " % (item["time"])
        duration_sec = float(seconds(item["time"]))
        #print "duration_sec %s" % duration_sec 
        #Count number of points, this to calculate timedelta for every point based on the speed
        points = float(len(item["Lat"]))
         
        #time delta at every point should be points / seconds 
        time_per_point_sec = (duration_sec / points)
        time_per_point = round(time_per_point_sec * 1000,0)  #in Milliseconds
        #print int(time_per_point)
        #create time object from it
        time_delta = datetime.strptime(str(int(time_per_point)), '%f')
        
        activityname = "Run at " + start_time.strftime('%d-%m-%Y')
        gpx = gpxpy.gpx.GPX()

        # Create first track in our GPX:
        gpx_track = gpxpy.gpx.GPXTrack(name=activityname)
        gpx.tracks.append(gpx_track)

        # Create first segment in our GPX track:
        gpx_segment = gpxpy.gpx.GPXTrackSegment()
        gpx_track.segments.append(gpx_segment)
 
        # Create points:
        for i,lat in enumerate(item ["Lat"]):
            #print "lat nr %s is %s " % (i , lat)
            lng = item ["Lng"][i]
            #print "lng nr %s is %s  " % (i , lng) 
            start_time = start_time + timedelta(seconds=time_per_point_sec)
            #elevation_data = mod_srtm.get_data()
            #meter = elevation_data.get_elevation(lat,lng)
            gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(lat, lng, elevation=None, time=start_time ))
        
        filename = "gps_track" + item["date"] + ".gpx"
        print " number of points %s in file %s " % (points, filename)
        file = open(filename, "w")
        file.write(gpx.to_xml())
        file.close()

