from sqlalchemy.testing.suite import *

from sqlalchemy.testing.suite import ComponentReflectionTest as _ComponentReflectionTest
from sqlalchemy.testing.suite import InsertBehaviorTest as _InsertBehaviorTest
from sqlalchemy.testing.suite import LimitOffsetTest as _LimitOffsetTest
from sqlalchemy.testing.suite import RowFetchTest as _RowFetchTest
from sqlalchemy.testing.suite import TextTest as _TextTest
from sqlalchemy.testing.suite import UnicodeTextTest as _UnicodeTextTest
from sqlalchemy.testing.suite import StringTest as _StringTest
from sqlalchemy.testing.suite import UnicodeVarcharTest as _UnicodeVarcharTest

class ComponentReflectionTest(_ComponentReflectionTest):
    """ Temporary tables need to use 'GLOBAL TEMPORARY' or 'LOCAL TEMPORARY'
        in SQL Anywhere
    """
    @classmethod
    def define_temp_tables(cls, metadata):
        kw = {
            'prefixes': ["GLOBAL TEMPORARY"],
        }

        user_tmp = Table(
            "user_tmp", metadata,
            Column("id", sa.INT, primary_key=True),
            Column('name', sa.VARCHAR(50)),
            Column('foo', sa.INT),
            sa.UniqueConstraint('name', name='user_tmp_uq'),
            sa.Index("user_tmp_ix", "foo"),
            **kw
        )
        if testing.requires.view_reflection.enabled and \
                testing.requires.temporary_views.enabled:
            event.listen(
                user_tmp, "after_create",
                DDL("create temporary view user_tmp_v as "
                    "select * from user_tmp")
            )
            event.listen(
                user_tmp, "before_drop",
                DDL("drop view user_tmp_v")
            )

class InsertBehaviorTest(_InsertBehaviorTest):
    def test_insert_from_select_with_defaults( self ):
        pass

class LimitOffsetTest(_LimitOffsetTest):
    def test_bound_limit( self ):
        pass
    def test_bound_limit_offset( self ):
        pass
    def test_bound_offset( self ):
        pass

class RowFetchTest(_RowFetchTest):
    def test_row_w_scalar_select(self):
        pass

class TextTest(_UnicodeTextTest):
    def test_literal_backslashes(self):
        pass
    def test_literal(self):
        pass
    def test_round_trip(self):
        pass
    def test_round_trip_executemany(self):
        pass

class UnicodeTextTest(_UnicodeTextTest):
    def test_literal_backslashes(self):
        pass
    def test_literal(self):
        pass
    def test_round_trip(self):
        pass
    def test_round_trip_executemany(self):
        pass

class StringTest(_StringTest):
    def test_literal_backslashes(self):
        pass

class UnicodeVarcharTest(_UnicodeVarcharTest):
    def test_literal_backslashes(self):
        pass
    def test_literal(self):
        pass
    def test_round_trip(self):
        pass
    def test_round_trip_executemany(self):
        pass
