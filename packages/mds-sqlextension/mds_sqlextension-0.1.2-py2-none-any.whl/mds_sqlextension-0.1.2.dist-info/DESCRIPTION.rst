sqlextension
=================
This module makes some SQL commands available for use with python-sql.

Install
=======
pip install mds-sqlextension

Available SQL commands
======================

- StringAgg (string_agg)
- Ascii (ascii)
- Concat2 (concat)
- RPad (rpad)
- Lower (lower)
- ArrayAgg (array_agg)
- Replace (replace)
- AnyInArray (any)
- FuzzyEqal (%)

To make FuzzyEqual work, call *CREATE EXTENSION pg_trgm;* in PostgreSQL.

Requires
========
- python-sql

Changes
=======

*0.1.2 - 06/09/2017*

- import optimized

*0.1.1 - 06/09/2017*

- first public version


