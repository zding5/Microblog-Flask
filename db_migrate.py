#!flask/bin/python

# This file is for RECORDING db migrating

# We will consider any changes to the structure
# of the app database a migration, including 
# from empty to something.

import imp
# This module provides an interface to the
# mechanisms used to implement the import statement.
# What ???

from migrate.versioning import api
from app import db
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO
# Same imports as in db_create.py

v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
# Get the version of our db

migration = SQLALCHEMY_MIGRATE_REPO + ('/versions/%03d_migration.py' % (v+1))
# Migration records ( through which you can do or undo migration I think ... )
# Look like "db_repository/versions/001_migration.py"

tmp_module = imp.new_module('old_model')
# Return a new empty module object called 'old_model'.
# ???

old_model = api.create_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
exec(old_model, tmp_module.__dict__)
# Snapshotting current version I think ... ???

script = api.make_update_script_for_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, tmp_module.meta, db.metadata)
open(migration, "wt").write(script)
# Generate migration.py's

api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
# Change db version

print('New migration saved as ' + migration)
print('Current database version: ' + str(v))

