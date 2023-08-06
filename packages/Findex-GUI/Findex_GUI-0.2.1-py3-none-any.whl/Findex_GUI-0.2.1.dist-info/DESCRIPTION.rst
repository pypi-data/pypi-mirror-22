Findex
========

is a file indexer for FTP, SMB and HTTP servers.

Features
--------
- Scalable/fast
- [Searching](http://i.imgur.com/WpTTkxx.png) (file name, category, size, extension)
- [File browsing](http://i.imgur.com/6UkGBzB.png)
- [IMDB powered 'popcorn' view](http://i.imgur.com/8nk8rbY.png) (release year, director, actors/actresses, genre)
- User login / registration
- Languages: Dutch/English
- Reverse proxying files from the (ftp/http) backend through the web interface

Stack
----------
[Postgres 9.5](https://www.postgresql.org/), [RabbitMQ](https://www.rabbitmq.com/), [ElasticSearch 1.7](https://www.elastic.co/), [ZomboDB](https://github.com/zombodb/zombodb), [Flask](http://flask.pocoo.org/),  [Twisted](https://twistedmatrix.com/trac/)

Requirements
------------
  - Linux (Debian >= **7** | Ubuntu >= **11** | CentOS >= **6**)
  - Python >= **3.5**
  - Postgres **9.5**
  - ElasticSearch **1.7.6**
  - RabbitMQ >= **3.5.4**


### Screenshot
[![pic](http://i.imgur.com/WpTTkxx.png)](w0w)

### Installation

Docker containers will be provided soon. For now, don't attempt to manually install. You've been warned! :)

```sh
apt-get install -y python3.5 python-virtualenv python3.5-dev libpq-dev git
virtualenv -p /usr/bin/python3.5 findex
cd $_
source bin/activate
git clone https://github.com/skftn/sqlalchemy_zdb.git
cd sqlalchemy_zdb
python setup.py develop
cd ..
pip install findex-gui
```

After that you can type `findex`.

### Streetcred
- Volkskrant (http://i.imgur.com/9oqlKU2.png) (dutch)
- Security.nl (dutch): [Duizenden openstaande FTP-servers in Nederland](https://www.security.nl/posting/440684)
- Motherboard (dutch) [440 terabytes aan Nederlandse privébestanden zijn nu makkelijk doorzoekbaar](https://motherboard.vice.com/nl/article/440-terabytes-aan-nederlandse-privbestanden-zijn-nu-makkelijk-doorzoekbaar)
- [@hdmoore](http://i.imgur.com/nyP0EEq.png)

