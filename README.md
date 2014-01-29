Scraped flags of the world
==============================================================================

Since I couldn't find a replete resource of up to date SVG flags of the world
_with licenses_ I've scraped Wikipedia and saved them all here.

The script is intact if you'd care to use it. It was a hack so it might be
brittle. Should give you a constantly up to date set though.

Licenses have been saved into `licenses.csv`.

Installation
------------------------------------------------------------------------------

* Set up a [`virtualenv`](venv) for development to keep dependencies separate.
* Install python packages with `pip install -r requirements.txt`.
* Install node packages with `npm install`

Running
------------------------------------------------------------------------------

* Get the flags with `python-from-virtual get_flags.py`.
* Build the PNG and CSS data urls with `grunt`.

License
------------------------------------------------------------------------------
[MIT license](http://en.wikipedia.org/wiki/MIT_License)
