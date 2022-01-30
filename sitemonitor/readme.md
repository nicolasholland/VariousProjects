Site Monitor
============

Set up
------

* Get Chrome

```
$ wget https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm
```

* On aliyun

```
$ sudo yum install ./google-chrome-stable_current_*.rpm
```

* On Ubuntu

```
$ sudo apt-get install alien
$ sudo alien google-chrome-stable_current_x86_64.rpm
$ sudo alien google-chrome-stable_current_x86_64.rpm
```


* Get Driver

```
$ wget https://chromedriver.storage.googleapis.com/97.0.4692.71/chromedriver_linux64.zip
```

```
$ unzip chromedriver_linux64.zip
```

Run monitor
-----------


Check all sites and write results into status.csv:

```
$ python monitor.py > status.csv
```

This can eg be done via a cronjob.


Publish results
---------------

This is done via a flask app:


```
$ python publish.py
```

Note that publish.py will look for the status.csv in the same folder.
If it is to be added to another flask app, simply make it importable there:


```
from flask import Flask
import publish

app = Flask(__name__)

app.add_url_rule('/sitemonitor', view_func=publish.check)
```

