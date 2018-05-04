from sqlalchemy.testing.requirements import SuiteRequirements

from sqlalchemy.testing import exclusions

class Requirements(SuiteRequirements):
    @property

    def intersect(self):
        return exclusions.open()

    @property
    def except_(self):
        return exclusions.open()

    @property
    def window_functions(self):
        return exclusions.open()

    @property
    def views(self):
        return exclusions.open()

    @property
    def reflects_pk_names(self):
        return exclusions.open()

    @property
    def datetime(self):
        """target dialect supports representation of Python
        datetime.datetime() objects."""

        return exclusions.closed()

    @property
    def datetime_microseconds(self):
        """target dialect supports representation of Python
        datetime.datetime() with microsecond objects."""

        return exclusions.closed()

    @property
    def datetime_historic(self):
        """target dialect supports representation of Python
        datetime.datetime() objects with historic (pre 1900) values."""

        return exclusions.closed()

    @property
    def date(self):
        """target dialect supports representation of Python
        datetime.date() objects."""

        return exclusions.closed()

    @property
    def date_historic(self):
        """target dialect supports representation of Python
        datetime.datetime() objects with historic (pre 1900) values."""

        return exclusions.closed()

    @property
    def time(self):
        """target dialect supports representation of Python
        datetime.time() objects."""

        return exclusions.closed()

    @property
    def time_microseconds(self):
        """target dialect supports representation of Python
        datetime.time() with microsecond objects."""

        return exclusions.closed()

    @property
    def order_by_col_from_union(self):
        """target database supports ordering by a column from a SELECT
        inside of a UNION
        E.g.  (SELECT id, ...) UNION (SELECT id, ...) ORDER BY id
        """

        return exclusions.closed()

    @property
    def cross_schema_fk_reflection(self):
        """target system must support reflection of inter-schema foreign keys
        """
        return exclusions.closed()

    @property
    def independent_connections(self):
        """target system must support simultaneous, independent database connections.
        """
        return exclusions.open()

    @property
    def temp_table_reflection(self):
        return exclusions.closed()

    @property
    def implicitly_named_constraints(self):
        return exclusions.open()

    @property
    def unique_constraint_reflection(self):
        return exclusions.closed()

    @property
    def floats_to_four_decimals(self):
        return exclusions.closed()
    
    @property
    def precision_generic_float_type(self):
        return exclusions.closed()
    
