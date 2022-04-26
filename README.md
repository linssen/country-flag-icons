Scraped flags of the world
==============================================================================

Since I couldn't find a replete resource of up to date SVG flags of the world
_with licenses_ I've scraped Wikipedia and saved them all here.

The script is intact if you'd care to use it. It was a hack so it might be
brittle. Should give you a constantly up to date set though.

Licenses have been saved into `licenses.csv`.

I've made no political decisions here - the country names, flags etc. are all
taken directly from the Wiki. Any changes should be made upstream therein.

![Flags](https://f.cloud.github.com/assets/67624/2029987/bf976a36-88ef-11e3-81bf-cbd1bb6966a9.png)

Installation
------------------------------------------------------------------------------

* Set up a [`virtualenv`](venv) for development to keep dependencies separate.
* Install python packages with `pip install -r requirements.txt`.

Running
------------------------------------------------------------------------------

* Get the flags with `python-from-virtual get_flags.py

License
------------------------------------------------------------------------------
[MIT license](http://en.wikipedia.org/wiki/MIT_License)
