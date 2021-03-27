# calendar-menu-py

Display calendar, world time and sun/moon information

Inspired by iStatMenus

Requires python3; pip: ephem

## TODO

Light mode color

Color in calendar, if SwiftBar fixes ANSI white color bug

![screenshot](https://user-images.githubusercontent.com/589440/112706422-ed76e800-8e9b-11eb-9e7f-19b052114621.png)

## Key

### Calendar

__\*d\*__	Today


__-d-__	Holiday (defined in script)


### Time, Sun & Moon

City, UTC offset, daylight hh:mm, difference from yesterday mm:ss

*below sorted by time*

(orange/blue)	current \*date\*/time, azimuth of sun, altitude of sun (if day)

(gray)		azimuth of moon, altitude of moon (if visible), age of moon (d), percent of illumination

sunrise		(dark blue) “blue hour” start, (yellow) “golden hour” start, (red) sunrise, azimuth, (yellow) “golden hour” end

noon		(red) time, azimuth

sunset	(yellow) “golden hour” start, (red) sunrise, azimuth, (yellow) “golden hour” end, (dark blue) “blue hour” end

(blue)	moonrise date/time, azimuth

(blue)	moonset date/time, azimuth

(gray)	next 5 phases of moon