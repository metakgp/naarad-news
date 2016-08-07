Naarad
======

Naarad aggregates all your KGP related news from facebook pages to one place.

## How does it work?

Naarad gets the content from the specified pages using Facebook's graph API. We
use [facepy](https://github.com/jgorset/facepy) as the python frontend for the
api.


## How to use Naarad

* Get a Facebook API token
* Install `facepy`
* Run `fbscraper.py` to create `feed.json`
* Run `frontend.py` to create the html file out of the `json`
* Run `deploy.sh` to push the changes to `gh-pages`.



## License

GPLv3
