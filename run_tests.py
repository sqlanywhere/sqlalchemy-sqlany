from sqlalchemy.dialects import registry
registry.register('sqlalchemy_sqlany', 'sqlalchemy_sqlany.base', 'SQLAnyDialect')

from sqlalchemy.testing import runner

runner.main()
