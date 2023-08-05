- v 0.9.12 Use UID instead of intid for storing SQL Items Folder
           as this might break relations if portal is renamed
           Fix virtual folder look for sql_virtual items only

- v 0.9.11 fix instance renaming by catching specific catalog mothods

- v 0.9.10 fix support of effective date and expiration date (field declared as "effective" but it looks for "effective_date"

- v 0.9.9 bug fix in dx sql type

- v 0.9.8 /@@data first search in catalog before creating objects on the fly

- v 0.9.7 added expire_on_commit=False to session maker to avoid SQLAlchemy DetachedInstanceError

- v 0.9.6 Catch sql connection errors on init so that the site doesn't break

- v 0.9.5 Register traverser with wrapped fti
    Fix wrong variable when saving sql folder attribute of dx type.

- v 0.9.4 Use custom sqlachemy table naming to be able to get more than one foreign key table between two same tables

- v 0.9.3 Fix 

- v 0.9.2 Use an unique name for relations as there can be multiple foreign keys linking the same two tables.
        Fix to be sure all sql_id are strings and not integers

- v 0.9.1 Fixed The SQLContent publisher to get Folder container from RelationValue. Get it from
        standard path might throw security issues.

- v 0.9 Use name instead of url to store sql_connection, so it's possible to change the url
        in saconnect without losing its reference in type definition.

- v 0.8 Allow SQL DX item to be added in site (ZODB) and get par of its content from SQL.
        Fix sqlalchemy session handling, several bug fixes

- v 0.7 Allow the use of relational table to get simple data as tuple (like keywords)

- v 0.4 Allow selection of all kind of columns for ID if SQL table type is a view

- v 0.3 Make possible the use of relations (Foreign Keys) many to one and many to many

