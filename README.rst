======
PyDonuts
======
Last Updated on **2014.10.27**

``PyDonuts`` is a toolbox. It provides some APIs and tools.

Features
========

* boxes

  + compression: Backup files and dictionaries

  + file_rename: Find files and reanme by regular expression

  + fileseeker: Find files by regular expression

  + mini_cache: Cache mechanism (support decorate format)

  + stock_agents: Stock selector for price/volume strategy (include crawler)

* utils

  + string:

    * chinese_num_converter: Chinese number <=> Arabic number

    * str_filter: truncate string if it has html tag, url, email etc.

  + security:

    * xtea.py: `wiki <http://en.wikipedia.org/wiki/XTEA>`_

    * password_generator.py: Generate password

  + web:

    * (PY) db: connection database apis (mysql, mongodb)

Requirements
============

* Python project

  + Python >= 2.6

  + **Optional** - ``lxml``

  + **Optional** - ``simplejson``

LICENSE
=======
MIT license.
