# StackOverflow
Scripting Project

First Run [schema.sql](/schema.sql) file to create databases:

``` mysql -u root -p < schema.sql```

To Start the Server : 

``` python3 main.py```

[static](/static) directory contains static html files whose structure does not change. Dynamic html files (aka templates ) will be present in [templates](/templates) directory.


****NOTE:****   Push to master only when a certain feature is stable and working properly. Otherwise make a new branch and merge it when it becomes stable.
