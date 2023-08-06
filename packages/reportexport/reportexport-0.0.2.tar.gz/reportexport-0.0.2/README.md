Report Exporting Service
===============================

[![Build Status](https://travis-ci.org/mdalp/reportexport.svg?branch=master)](https://travis-ci.org/mdalp/reportexport)

version number: 0.0.1
author: Marcello Dalponte

Overview
--------

A Flask microservice that produces reports out of a database in xml and pdf format.

Installation / Usage
--------------------

To install use pip:

    $ pip install reportexport


Or clone the repo:

    $ git clone https://github.com/mdalp/reportexport.git
    $ python setup.py install

To run:

    $ REPORTEXPORT_DATABASE=postgresql://myuser:passwd@localhost/mydb make run

Contributing
------------

This is a sketch project as such it is open to a number of improvements, among which:

 1. Dinamically calculate the left indent space in the pdf report
 2. Add the currency to the prices in the report
 3. Improve the comparison between pdfs in the test utils to detect format changes

 To install requirements for dev:

    $ make devinstall

To run tests:

    $ make tests
