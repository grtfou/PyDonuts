======
PyDonuts
======
Last Updated on **2014.10.27**

``beagle`` is a toolbox. It provides some APIs and tools.

Features
========

(PY): Python

* boxes

  + (PY) compression: Backup files and dictionaries

  + (PY) file_rename: Find files and reanme by regular expression

  + (PY) fileseeker: Find files by regular expression

  + (PY) mini_cache: Cache mechanism (support decorate format)

  + (PY) stock_agents: Stock selector for price/volume strategy (include crawler)

* utils

  + string:

    * (PY) chinese_num_converter: Chinese number <=> Arabic number

    * (PY) str_filter: truncate string if it has html tag, url, email etc.

  + security:

    * (PY) xtea.py: `wiki <http://en.wikipedia.org/wiki/XTEA>`_

    * (PY) password_generator.py: Generate password

  + web:

    * (PY) db: connection database apis (mysql, mongodb)

Requirements
============

* Python project

  + Python >= 2.6

  + **Optional** - ``lxml``

  + **Optional** - ``simplejson``

* Go

  + Go >= 1.3

LICENSE
=======
MIT license.
