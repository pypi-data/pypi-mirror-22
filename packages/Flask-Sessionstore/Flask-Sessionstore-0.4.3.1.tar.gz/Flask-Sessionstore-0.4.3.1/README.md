Flask-Sessionstore
==================
[![Build Status](https://travis-ci.org/mcrowson/flask-sessionstore.svg?branch=master)](https://travis-ci.org/mcrowson/flask-sessionstore)
[![Documentation Status](https://readthedocs.org/projects/flask-sessionstore/badge/?version=latest)](http://flask-sessionstore.readthedocs.io/en/latest/?badge=latest)
[![Coverage Status](https://coveralls.io/repos/github/mcrowson/flask-session/badge.svg)](https://coveralls.io/github/mcrowson/flask-session) 


[![Code Issues](https://www.quantifiedcode.com/api/v1/project/df2c3cad886341899a8e5e2c0fd1a047/badge.svg)](https://www.quantifiedcode.com/app/project/df2c3cad886341899a8e5e2c0fd1a047)


This project is a hard fork of the orphaned Flask-Session project at https://github.com/fengsp/flask-session that aims to provide 
python2 and python3 support for a growing number of session backends.


Flask-Sessionstore is an extension for Flask that adds support for Server-side Session to your application.

Please see the [Documentation](flask-sessionstore.rtfd.io) for implementation and configuration instruction. 

```bash
pip install flask-sessionstore
```

## Testing
Tests require a running version of MongoDB, Redis, and Memcached. The easiest way to get those 
is via docker-compose. 
```bash
$ docker-compose up -d
$ nosetests --with-timer
$ docker-compose down
```
