# init
1. pip3 install alembic
2. alembic init db
3. ```vim alembic.ini``` set ```sqlalchemy.url = sqlite:///db/database.db```

# use
1. create: ```alembic revision -m "create_users_table"```
2. update: ```alembic revision -m "alter_users_table"```
3. Write the SQL script with reference to the history file
4. Note that SQL must be able to be rolled back
5. Notice Historical files cannot be modified
6. migrate: ```alembic upgrade head```