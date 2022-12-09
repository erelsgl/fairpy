# Fair and efficient with minimal sharing

To use the Spliddit data, you should first ask the team of [spliddit.org](https://spliddit.org/) to send you an SQL dump.
Then, convert it to an SQLITE database as follows:

    python mysql_to_sqlite.py <filename>.sql

It should create a file called `<filename>.db`.

Then, edit the file [spliddit.py](spliddit.py) and update the path to the db. Then verify that it works by running:

    python spliddit.py

