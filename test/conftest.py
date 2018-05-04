from sqlalchemy.dialects import registry

registry.register("sqlalchemy_sqlany", "sqlalchemy_sqlany.base", "dialect")

from sqlalchemy.testing.plugin.pytestplugin import *
