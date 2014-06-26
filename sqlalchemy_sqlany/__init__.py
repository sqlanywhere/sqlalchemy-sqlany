# Copyright 2014 SAP AG or an SAP affiliate company.
# 

__version__ = '1.0.1'

from sqlalchemy_sqlany import base

# default dialect
base.dialect = base.SQLAnyDialect

from .base import CHAR, VARCHAR, TIME, NCHAR, NVARCHAR,\
                 TEXT, DATE, DATETIME, FLOAT, NUMERIC,\
                 BIGINT, INT, INTEGER, SMALLINT, BINARY,\
                 VARBINARY, UNITEXT, UNICHAR, UNIVARCHAR,\
                 IMAGE, BIT, MONEY, SMALLMONEY, TINYINT,\
                 dialect


__all__ = (
    'CHAR', 'VARCHAR', 'TIME', 'NCHAR', 'NVARCHAR',
    'TEXT', 'DATE', 'DATETIME', 'FLOAT', 'NUMERIC',
    'BIGINT', 'INT', 'INTEGER', 'SMALLINT', 'BINARY',
    'VARBINARY', 'UNITEXT', 'UNICHAR', 'UNIVARCHAR',
    'IMAGE', 'BIT', 'MONEY', 'SMALLMONEY', 'TINYINT',
    'dialect'
)
