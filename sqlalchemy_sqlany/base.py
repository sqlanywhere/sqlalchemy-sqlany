# Copyright 2014 SAP AG or an SAP affiliate company.
# 

import operator
import re

from sqlalchemy.sql import compiler, expression, text, bindparam
from sqlalchemy.engine import default, base, reflection, url
from sqlalchemy import types as sqltypes
from sqlalchemy.sql import operators as sql_operators
from sqlalchemy import schema as sa_schema
from sqlalchemy import util, sql, exc

from sqlalchemy.types import CHAR, VARCHAR, TIME, NCHAR, NVARCHAR,\
                            TEXT, DATE, DATETIME, FLOAT, NUMERIC,\
                            BIGINT, INT, INTEGER, SMALLINT, BINARY,\
                            VARBINARY, DECIMAL, TIMESTAMP, Unicode,\
                            UnicodeText, REAL

RESERVED_WORDS = set([
    "add", "all", "alter", "and",
    "any", "array", "as", "asc", "attach", "backup",
    "begin", "between", "bigint", "binary",
    "bit", "bottom", "break", "by",
    "call", "capability", "cascade", "case",
    "cast", "char", "char_convert", "character",
    "check", "checkpoint", "close", "comment",
    "commit", "compressed", "conflict", "connect", "constraint", "contains",
    "continue", "convert", "create", "cross",
    "cube", "current", "current_timestamp", "current_user",
    "cursor", "date", "datetimeoffse", "dbspace", "deallocate",
    "dec", "decimal", "declare", "default",
    "delete", "deleting", "desc", "detach", "distinct",
    "do", "double", "drop", "dynamic",
    "else", "elseif", "encrypted", "end",
    "endif", "escape", "except", "exception",
    "exec", "execute", "existing", "exists",
    "externlogin", "fetch", "first", "float",
    "for", "force", "foreign", "forward",
    "from", "full", "goto", "grant",
    "group", "having", "holdlock", "identified",
    "if", "in", "index", 
    "inner", "inout", "insensitive", "insert",
    "inserting", "install", "instead", "int",
    "integer", "integrated", "intersect", "into",
    "is", "isolation", "join", "json", "kerberos",
    "key", "lateral", "left", "like", "limit",
    "lock", "login", "long", "match",
    "membership", "merge", "message", "mode", "modify",
    "natural", "nchar", "new", "no", "noholdlock",
    "not", "notify", "null", "numeric", "nvarchar",
    "of", "off", "on", "open", "openstring", "openxml",
    "option", "options", "or", "order",
    "others", "out", "outer", "over",
    "passthrough", "precision", "prepare", "primary",
    "print", "privileges", "proc", "procedure",
    "publication", "raiserror", "readtext", "real",
    "reference", "references", "refresh", "release", "remote",
    "remove", "rename", "reorganize", "resource",
    "restore", "restrict", "return", "revoke",
    "right", "rollback", "rollup", "row", "rowtype", "save",
    "savepoint", "scroll", "select", "sensitive",
    "session", "set", "setuser", "share",
    "smallint", "some", "spatial", "sqlcode", "sqlstate",
    "start", "stop", "subtrans", "subtransaction",
    "synchronize", "table", "temporary",
    "then", "time", "timestamp", "tinyint",
    "to", "top", "tran", "treat", "trigger",
    "truncate", "tsequal", "unbounded", "union",
    "unique", "uniqueidentifier", "unknown", "unnest", "unsigned", "update",
    "updating", "user", "using", "validate",
    "values", "varbinary", "varbit", "varchar", "variable", "varray",
    "varying", "view", "wait", "waitfor",
    "when", "where", "while", "window",
    "with",
    "within", "work", "writetext", "xml"
    ])


class _SQLAnyUnitypeMixin(object):
    """these types appear to return a buffer object."""

    def result_processor(self, dialect, coltype):
        def process(value):
            if value is not None:
                return str(value)
            else:
                return None
        return process


class UNICHAR(_SQLAnyUnitypeMixin, sqltypes.Unicode):
    __visit_name__ = 'UNICHAR'


class UNIVARCHAR(_SQLAnyUnitypeMixin, sqltypes.Unicode):
    __visit_name__ = 'UNIVARCHAR'


class UNITEXT(_SQLAnyUnitypeMixin, sqltypes.UnicodeText):
    __visit_name__ = 'UNITEXT'


class TINYINT(sqltypes.Integer):
    __visit_name__ = 'TINYINT'


class BIT(sqltypes.TypeEngine):
    __visit_name__ = 'BIT'


class MONEY(sqltypes.TypeEngine):
    __visit_name__ = "MONEY"


class SMALLMONEY(sqltypes.TypeEngine):
    __visit_name__ = "SMALLMONEY"


class UNIQUEIDENTIFIER(sqltypes.TypeEngine):
    __visit_name__ = "UNIQUEIDENTIFIER"


class IMAGE(sqltypes.LargeBinary):
    __visit_name__ = 'IMAGE'


class SQLAnyTypeCompiler(compiler.GenericTypeCompiler):
    def visit_large_binary(self, type_):
        return self.visit_IMAGE(type_)

    def visit_boolean(self, type_):
        return self.visit_BIT(type_)

    def visit_unicode(self, type_):
        return self.visit_NVARCHAR(type_)

    def visit_UNICHAR(self, type_):
        return "UNICHAR(%d)" % type_.length

    def visit_UNIVARCHAR(self, type_):
        return "UNIVARCHAR(%d)" % type_.length

    def visit_UNITEXT(self, type_):
        return "UNITEXT"

    def visit_TINYINT(self, type_):
        return "TINYINT"

    def visit_IMAGE(self, type_):
        return "IMAGE"

    def visit_BIT(self, type_):
        return "BIT"

    def visit_MONEY(self, type_):
        return "MONEY"

    def visit_SMALLMONEY(self, type_):
        return "SMALLMONEY"

    def visit_UNIQUEIDENTIFIER(self, type_):
        return "UNIQUEIDENTIFIER"

ischema_names = {
    'bigint': BIGINT,
    'int': INTEGER,
    'integer': INTEGER,
    'smallint': SMALLINT,
    'tinyint': TINYINT,
    'unsigned bigint': BIGINT,  # TODO: unsigned flags
    'unsigned int': INTEGER,  # TODO: unsigned flags
    'unsigned smallint': SMALLINT,  # TODO: unsigned flags
    'numeric': NUMERIC,
    'decimal': DECIMAL,
    'dec': DECIMAL,
    'float': FLOAT,
    'double': NUMERIC,  # TODO
    'double precision': NUMERIC,  # TODO
    'real': REAL,
    'smallmoney': SMALLMONEY,
    'money': MONEY,
    'smalldatetime': DATETIME,
    'datetime': DATETIME,
    'date': DATE,
    'time': TIME,
    'char': CHAR,
    'character': CHAR,
    'varchar': VARCHAR,
    'character varying': VARCHAR,
    'char varying': VARCHAR,
    'unichar': UNICHAR,
    'unicode character': UNIVARCHAR,
    'nchar': NCHAR,
    'national char': NCHAR,
    'national character': NCHAR,
    'nvarchar': NVARCHAR,
    'nchar varying': NVARCHAR,
    'national char varying': NVARCHAR,
    'national character varying': NVARCHAR,
    'text': TEXT,
    'unitext': UNITEXT,
    'binary': BINARY,
    'varbinary': VARBINARY,
    'image': IMAGE,
    'bit': BIT,

# not in documentation for ASE 15.7
    'long varchar': TEXT,  # TODO
    'timestamp': TIMESTAMP,
    'uniqueidentifier': UNIQUEIDENTIFIER,

}


class SQLAnyInspector(reflection.Inspector):

    def __init__(self, conn):
        reflection.Inspector.__init__(self, conn)

    def get_table_id(self, table_name, schema=None):
        """Return the table id from `table_name` and `schema`."""

        return self.dialect.get_table_id(self.bind, table_name, schema,
                                         info_cache=self.info_cache)


class SQLAnyExecutionContext(default.DefaultExecutionContext):
    def set_ddl_autocommit(self, connection, value):
        """Must be implemented by subclasses to accommodate DDL executions.

        "connection" is the raw unwrapped DBAPI connection.   "value"
        is True or False.  when True, the connection should be configured
        such that a DDL can take place subsequently.  when False,
        a DDL has taken place and the connection should be resumed
        into non-autocommit mode.

        """
        pass

    def pre_exec(self):
        if self.isinsert:
            tbl = self.compiled.statement.table
            seq_column = tbl._autoincrement_column
            insert_has_sequence = seq_column is not None

        if self.isddl:
            if not self.should_autocommit:
                raise exc.InvalidRequestError(
                        "The SQLAny dialect only supports "
                        "DDL in 'autocommit' mode at this time.")

            self.set_ddl_autocommit(
                        self.root_connection.connection.connection,
                        True)

    def post_exec(self):
        if self.isddl:
            self.set_ddl_autocommit(self.root_connection, False)

    def get_lastrowid(self):
        cursor = self.create_cursor()
        cursor.execute("SELECT @@identity AS lastrowid")
        lastrowid = cursor.fetchone()[0]
        cursor.close()
        return lastrowid


class SQLAnySQLCompiler(compiler.SQLCompiler):
    ansi_bind_rules = True

    extract_map = util.update_copy(
        compiler.SQLCompiler.extract_map,
        {
        'doy': 'dayofyear',
        'dow': 'weekday',
        'milliseconds': 'millisecond'
    })

    def get_select_precolumns(self, select):
        s = "DISTINCT" if select._distinct else ""
        if select._limit:
            if select._limit == 1:
                s += "FIRST "
            else:
                s += "TOP %s " % select._limit
        if select._offset:
            if not select._limit:
                # SQL Anywhere doesn't allow "start at" without "top n"
                s += "TOP ALL "
            s += "START AT %s " % (select._offset + 1,)
        return s

    def get_from_hint_text(self, table, text):
        return text

    def limit_clause(self, select):
        # Limit in sybase is after the select keyword
        return ""

    def visit_extract(self, extract, **kw):
        field = self.extract_map.get(extract.field, extract.field)
        return 'DATEPART("%s", %s)' % (
                            field, self.process(extract.expr, **kw))

    def visit_now_func(self, fn, **kw):
        return "NOW()"

    def for_update_clause(self, select):
        # "FOR UPDATE" is only allowed on "DECLARE CURSOR"
        # which SQLAlchemy doesn't use
        return ''

    def order_by_clause(self, select, **kw):
        kw['literal_binds'] = True
        order_by = self.process(select._order_by_clause, **kw)

        if order_by:
            return " ORDER BY " + order_by
        else:
            return ""


class SQLAnyDDLCompiler(compiler.DDLCompiler):
    def get_column_specification(self, column, **kwargs):
        colspec = self.preparer.format_column(column) + " " + \
                        self.dialect.type_compiler.process(column.type)

        if column.table is None:
            raise exc.CompileError(
                        "The SQLAny dialect requires Table-bound "
                       "columns in order to generate DDL")
        seq_col = column.table._autoincrement_column

        # install a IDENTITY Sequence if we have an implicit IDENTITY column
        if seq_col is column:
            sequence = isinstance(column.default, sa_schema.Sequence) \
                                    and column.default
            if sequence:
                start, increment = sequence.start or 1, \
                                    sequence.increment or 1
            else:
                start, increment = 1, 1
            if (start, increment) == (1, 1):
                colspec += " IDENTITY"
            else:
                # TODO: need correct syntax for this
                colspec += " IDENTITY(%s,%s)" % (start, increment)
        else:
            default = self.get_column_default_string(column)
            if default is not None:
                colspec += " DEFAULT " + default

            if column.nullable is not None:
                if not column.nullable or column.primary_key:
                    colspec += " NOT NULL"
                else:
                    colspec += " NULL"

        return colspec

    def visit_drop_index(self, drop):
        index = drop.element
        return "\nDROP INDEX %s.%s" % (
            self.preparer.quote_identifier(index.table.name),
            self._prepared_index_name(drop.element,
                                        include_schema=False)
            )

class SQLAnyIdentifierPreparer(compiler.IdentifierPreparer):
    reserved_words = RESERVED_WORDS

class SQLAnyDialect(default.DefaultDialect):
    name = 'sqlany'
    supports_unicode_statements = False
    supports_sane_rowcount = False
    supports_sane_multi_rowcount = False

    supports_native_boolean = False
    supports_unicode_binds = False
    postfetch_lastrowid = True
    supports_multivalues_insert = True

    @classmethod
    def dbapi(self):
        import sqlanydb
        return sqlanydb

    @property
    def driver(self):
        import sqlanydb
        return sqlanydb

    def create_connect_args(self, url):
        opts = url.translate_connect_args(username='uid', password='pwd',
                                          database='dbn' )
        keys = list(opts.keys())
        if 'host' in keys and 'port' in keys:
            opts['host'] += ':%s' % opts['port']
            del opts['port']
        #
        return ([], opts)
    #

    colspecs = {}
    ischema_names = ischema_names

    type_compiler = SQLAnyTypeCompiler
    statement_compiler = SQLAnySQLCompiler
    ddl_compiler = SQLAnyDDLCompiler
    preparer = SQLAnyIdentifierPreparer
    inspector = SQLAnyInspector
    execution_ctx_cls = SQLAnyExecutionContext

    def _get_default_schema_name(self, connection):
        return connection.scalar(
                     text("SELECT current user",
                     typemap={'user_name': Unicode})
             )

    def initialize(self, connection):
        super(SQLAnyDialect, self).initialize(connection)
        self.max_identifier_length = 128

    def get_table_id(self, connection, table_name, schema=None, **kw):
        """Fetch the id for schema.table_name.

        Several reflection methods require the table id.  The idea for using
        this method is that it can be fetched one time and cached for
        subsequent calls.

        """

        table_id = None
        if schema is None:
            schema = self.default_schema_name
        TABLEID_SQL = text("""
          SELECT t.table_id AS id
          FROM sys.systab t JOIN dbo.sysusers u ON t.creator=u.uid
          WHERE u.name = :schema_name
              AND t.table_name = :table_name
              AND t.table_type in (1, 3, 4, 21)
        """)

        # Py2K
        if isinstance(schema, str):
            schema = schema.encode("ascii")
        if isinstance(table_name, str):
            table_name = table_name.encode("ascii")
        # end Py2K
        result = connection.execute(TABLEID_SQL,
                                    schema_name=schema,
                                    table_name=table_name)
        table_id = result.scalar()
        if table_id is None:
            raise exc.NoSuchTableError(table_name)
        return table_id

    @reflection.cache
    def get_columns(self, connection, table_name, schema=None, **kw):
        table_id = self.get_table_id(connection, table_name, schema,
                                     info_cache=kw.get("info_cache"))

        COLUMN_SQL = text("""
          SELECT col.column_name AS name,
                 t.domain_name AS type,
                 if col.nulls ='Y' then 1 else 0 endif AS nullable,
                 if col."default" = 'autoincrement' then 1 else 0 endif AS autoincrement,
                 col."default" AS "default",
                 col.width AS "precision",
                 col.scale AS scale,
                 col.width AS length
          FROM sys.sysdomain t join sys.systabcol col on t.domain_id=col.domain_id
          WHERE col.table_id = :table_id
          ORDER BY col.column_id
        """)

        results = connection.execute(COLUMN_SQL, table_id=table_id)

        columns = []
        for (name, type_, nullable, autoincrement, default, precision, scale,
             length) in results:
            col_info = self._get_column_info(name, type_, bool(nullable),
                             bool(autoincrement), default, precision, scale,
                             length)
            columns.append(col_info)

        return columns

    def _get_column_info(self, name, type_, nullable, autoincrement, default,
            precision, scale, length):

        coltype = self.ischema_names.get(type_, None)

        kwargs = {}

        if coltype in (NUMERIC, DECIMAL):
            args = (precision, scale)
        elif coltype == FLOAT:
            args = (precision,)
        elif coltype in (CHAR, VARCHAR, UNICHAR, UNIVARCHAR, NCHAR, NVARCHAR):
            args = (length,)
        else:
            args = ()

        if coltype:
            coltype = coltype(*args, **kwargs)
            #is this necessary
            #if is_array:
            #     coltype = ARRAY(coltype)
        else:
            util.warn("Did not recognize type '%s' of column '%s'" %
                      (type_, name))
            coltype = sqltypes.NULLTYPE

        if default:
            default = re.sub("DEFAULT", "", default).strip()
            default = re.sub("^'(.*)'$", lambda m: m.group(1), default)
        else:
            default = None

        column_info = dict(name=name, type=coltype, nullable=nullable,
                           default=default, autoincrement=autoincrement)
        return column_info

    @reflection.cache
    def get_foreign_keys(self, connection, table_name, schema=None, **kw):

        table_id = self.get_table_id(connection, table_name, schema,
                                     info_cache=kw.get("info_cache"))

        table_cache = {}
        column_cache = {}
        foreign_keys = []

        table_cache[table_id] = {"name": table_name, "schema": schema}

        COLUMN_SQL = text("""
          SELECT c.column_id AS id, c.column_name AS name
          FROM sys.systabcol c
          WHERE c.table_id = :table_id
        """)

        results = connection.execute(COLUMN_SQL, table_id=table_id)
        columns = {}
        for col in results:
            columns[col["id"]] = col["name"]
        column_cache[table_id] = columns

        REFCONSTRAINT_SQL = text("""
          SELECT pt.table_name AS name, pt.table_id AS reftable_id
          FROM sys.sysfkey fk
          join sys.systab pt on fk.primary_table_id = pt.table_id
          WHERE fk.foreign_table_id = :table_id
        """)
        referential_constraints = connection.execute(REFCONSTRAINT_SQL,
                                                     table_id=table_id)

        REFTABLE_SQL = text("""
          SELECT t.table_name AS name, u.name AS "schema"
          FROM sys.systab t JOIN dbo.sysusers u ON t.creator = u.uid
          WHERE t.table_id = :table_id
        """)

        for r in referential_constraints:
            reftable_id = r["reftable_id"]

            if reftable_id not in table_cache:
                c = connection.execute(REFTABLE_SQL, table_id=reftable_id)
                reftable = c.fetchone()
                c.close()
                table_info = {"name": reftable["name"], "schema": None}
                if (schema is not None or
                        reftable["schema"] != self.default_schema_name):
                    table_info["schema"] = reftable["schema"]

                table_cache[reftable_id] = table_info
                results = connection.execute(COLUMN_SQL, table_id=reftable_id)
                reftable_columns = {}
                for col in results:
                    reftable_columns[col["id"]] = col["name"]
                column_cache[reftable_id] = reftable_columns

            reftable = table_cache[reftable_id]
            reftable_columns = column_cache[reftable_id]

            constrained_columns = []
            referred_columns = []
            REFCOLS_SQL = text("""SELECT 
            ic.column_id as fokey,
            pic.column_id as refkey
            FROM sys.sysfkey fk
            join sys.sysidxcol ic on (fk.foreign_index_id=ic.index_id and fk.foreign_table_id=ic.table_id)
            join sys.sysidxcol pic on (fk.primary_index_id=pic.index_id and fk.primary_table_id=pic.table_id)
            WHERE fk.primary_table_id = :reftable_id
            and fk.foreign_table_id = :table_id
            """)
            ref_cols = connection.execute(REFCOLS_SQL,
                                          table_id=table_id,
                                          reftable_id=reftable_id)
            for rc in ref_cols:
                constrained_columns.append(columns[rc["fokey"]])
                referred_columns.append(reftable_columns[rc["refkey"]])

            fk_info = {
                    "constrained_columns": constrained_columns,
                    "referred_schema": reftable["schema"],
                    "referred_table": reftable["name"],
                    "referred_columns": referred_columns,
                    "name": r["name"]
                }

            foreign_keys.append(fk_info)

        return foreign_keys

    @reflection.cache
    def get_indexes(self, connection, table_name, schema=None, **kw):
        table_id = self.get_table_id(connection, table_name, schema,
                                     info_cache=kw.get("info_cache"))

        # index_category=3 -> not primary key, not foreign key, not text index
        # unique=1 -> unique index, 2 -> unique constraint, 5->unique index with
        # nulls not distinct
        INDEX_SQL = text("""
          SELECT i.index_id as index_id, i.index_name AS name,
                 if i."unique" in (1,2,5) then 1 else 0 endif AS "unique"
          FROM sys.sysidx i join sys.systab t on i.table_id=t.table_id
          WHERE t.table_id = :table_id and i.index_category = 3
        """)

        results = connection.execute(INDEX_SQL, table_id=table_id)
        indexes = []
        for r in results:
            INDEXCOL_SQL = text("""
             select tc.column_name as col
             FROM sys.sysidxcol ic
             join sys.systabcol tc on (ic.table_id=tc.table_id and ic.column_id=tc.column_id)
             WHERE ic.index_id = :index_id and ic.table_id = :table_id
             ORDER BY ic.sequence ASC
            """)
            idx_cols = connection.execute(INDEXCOL_SQL, index_id=r["index_id"],
                                          table_id=table_id)
            column_names = [ic["col"] for ic in idx_cols]
            index_info = {"name": r["name"],
                          "unique": bool(r["unique"]),
                          "column_names": column_names}
            indexes.append(index_info)

        return indexes

    @reflection.cache
    def get_pk_constraint(self, connection, table_name, schema=None, **kw):
        table_id = self.get_table_id(connection, table_name, schema,
                                     info_cache=kw.get("info_cache"))

        # index_category=1 -> primary key
        PK_SQL = text("""
          SELECT t.table_name AS table_name, i.index_id as index_id,
                 i.index_name AS name
          FROM sys.sysidx i join sys.systab t on i.table_id=t.table_id
          WHERE t.table_id = :table_id and i.index_category = 1
        """)

        results = connection.execute(PK_SQL, table_id=table_id)
        pks = results.fetchone()
        results.close()

        PKCOL_SQL = text("""
             select tc.column_name as col
             FROM sys.sysidxcol ic
             join sys.systabcol tc on (ic.table_id=tc.table_id and ic.column_id=tc.column_id)
             WHERE ic.index_id = :index_id and ic.table_id = :table_id
            """)
        pk_cols = connection.execute(PKCOL_SQL, index_id=pks["index_id"],
                                     table_id=table_id )
        column_names = [pkc["col"] for pkc in pk_cols]
        return {"constrained_columns": column_names,
                "name": pks["name"]}

    @reflection.cache
    def get_unique_constraints(self, connection, table_name, schema=None, **kw):
        # Same as get_indexes except only for "unique"=2
        table_id = self.get_table_id(connection, table_name, schema,
                                     info_cache=kw.get("info_cache"))

        # unique=2 -> unique constraint
        INDEX_SQL = text("""
          SELECT i.index_id as index_id, i.index_name AS name
          FROM sys.sysidx i join sys.systab t on i.table_id=t.table_id
          WHERE t.table_id = :table_id and i.index_category = 3 and i."unique"=2
        """)

        results = connection.execute(INDEX_SQL, table_id=table_id)
        indexes = []
        for r in results:
            INDEXCOL_SQL = text("""
             select tc.column_name as col
             FROM sys.sysidxcol ic
             join sys.systabcol tc on (ic.table_id=tc.table_id and ic.column_id=tc.column_id)
             WHERE ic.index_id = :index_id and ic.table_id = :table_id
             ORDER BY ic.sequence ASC
            """)
            idx_cols = connection.execute(INDEXCOL_SQL, index_id=r["index_id"],
                                          table_id=table_id)
            column_names = [ic["col"] for ic in idx_cols]
            index_info = {"name": r["name"],
                          "column_names": column_names}
            indexes.append(index_info)

        return indexes       

    @reflection.cache
    def get_schema_names(self, connection, **kw):

        SCHEMA_SQL = text("SELECT u.name AS name FROM dbo.sysusers u")

        schemas = connection.execute(SCHEMA_SQL)

        return [s["name"] for s in schemas]

    @reflection.cache
    def get_table_names(self, connection, schema=None, **kw):
        if schema is None:
            schema = self.default_schema_name

        TABLE_SQL = text("""
          SELECT t.table_name AS name
          FROM sys.systab t JOIN dbo.sysusers u ON t.creator = u.uid
          WHERE u.name = :schema_name and table_type <> 21
        """)

        # Py2K
        if isinstance(schema, str):
            schema = schema.encode("ascii")
        # end Py2K
        tables = connection.execute(TABLE_SQL, schema_name=schema)

        return [t["name"] for t in tables]

    @reflection.cache
    def get_view_definition(self, connection, view_name, schema=None, **kw):
        if schema is None:
            schema = self.default_schema_name

        VIEW_DEF_SQL = text("""
          SELECT v.view_def as text
          FROM sys.sysview v JOIN sys.sysobject o ON v.view_object_id = o.object_id
          join sys.systab t on o.object_id=t.object_id
          WHERE t.table_name = :view_name
            AND t.table_type = 21
        """)

        # Py2K
        if isinstance(view_name, str):
            view_name = view_name.encode("ascii")
        # end Py2K
        view = connection.execute(VIEW_DEF_SQL, view_name=view_name)

        return view.scalar()

    @reflection.cache
    def get_view_names(self, connection, schema=None, **kw):
        if schema is None:
            schema = self.default_schema_name

        VIEW_SQL = text("""
          SELECT t.table_name AS name
          FROM sys.systab t JOIN dbo.sysusers u ON t.creator = u.uid
          WHERE u.name = :schema_name
            AND t.table_type = 21
        """)

        # Py2K
        if isinstance(schema, str):
            schema = schema.encode("ascii")
        # end Py2K
        views = connection.execute(VIEW_SQL, schema_name=schema)

        return [v["name"] for v in views]

    def has_table(self, connection, table_name, schema=None):
        try:
            self.get_table_id(connection, table_name, schema)
        except exc.NoSuchTableError:
            return False
        else:
            return True
