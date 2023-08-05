.. contents::

GUILLOTINA_ELASTICSEARCH
========================


Configuration
-------------

config.json can include elasticsearch section::

    "elasticsearch": {
        "index_name_prefix": "guillotina-",
        "connection_settings": {
            "endpoints": ["localhost:9200"],
            "sniffer_timeout": 0.5
        }
    }


Installation on a site
----------------------

POST SITE_URL/@catalog

{}

Uninstall on a site
-------------------

DELETE SITE_URL/@catalog

{}

1.0.4 (2017-05-02)
------------------

- optimize reindex more
  [vangheem]


1.0.3 (2017-05-02)
------------------

- More memory efficient reindex
  [vangheem]


1.0.2 (2017-05-02)
------------------

- Fix reindexing content
  [vangheem]


1.0.1 (2017-04-25)
------------------

- Provide as async utility as it allows us to close connections when the object
  is destroyed
  [vangheem]


1.0.0 (2017-04-24)
------------------

- initial release


