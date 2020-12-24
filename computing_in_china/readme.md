Computing in china
==================

DISCLAIMER: This is an ongoing project.
We use this readme to document our progress and "lessons learned".
Once this project is (hopefully) finished, we plan to make a blog post about it.


There are some things to regard when doing data processing in china.
E.g. the pypi index is blocked there. (At least it was last time we were there)

In this project we explore how many things we know about data processing
would work in china.


Cloud Service
-------------

Alibabacloud has several locations in mainland china including Shanghai, Beijing, Hangzhou and many more.
While cloud providers like gcp or aws offer services in cities like Taipeh
or Hongkong, they currently do not (or in case of aws only with separate accounts) in mainland China.
PRC law requires real name registration for server locations in mainland China.
We needed to provide a copy of our passport for real name registration which went over smooth and fast.


Fun fact: when we registered our account at aliyun, our bank blocked our credit card in
fear we could be victim of fraud.
After telling them about one of the world's largest e-commerce companies we got our card back :D


Similar to Boto3 (AWS) and google-cloud-python there is an open source python sdk for aliyun
on github called [aliyun-openapi-python-sdk](https://github.com/aliyun/aliyun-openapi-python-sdk).
Available on [pypi](https://pypi.org/project/aliyun-python-sdk-core/)

```
$ pip install aliyun-python-sdk-core
$ pip install aliyun-python-sdk-rds
$ pip install aliyun-python-sdk-ecs
```


Like most cloud service providers they have a lot of services to choose from.
We looked into two services that relate to the kind of work we're used to, the 
Elastic Compute Service and the TSDB Service (Time Series Database).

Elastic Compute Service:

Subscription based or "pay-as-you-go", e.g. 16GB, 4vCPUs machine available for either about 40$USD/month or 0.163$USD/hr. (Prices checked in April 2020, for shanghai location)

TSDB:

In their documentation they claim their tsdb has better performance then e.g. influxdb.



Docker
------

Check out and describe Daocloud docker hub.


Python Package Index
--------------------

Explain situation around pypi in china and the aliyun pypi mirror.


Deploying a flask app on ECS
----------------------------

Here are in short the steps to deploy a flask app eg. a website or api on ECS.
It is based on this [tutorial](https://www.alibabacloud.com/blog/setting-up-a-flask-application-on-alibaba-cloud-ecs-ubuntu-16-04_594502)

We're using an Aliyun Linux instance instead of Ubuntu.


* Start ECS instance, setup logon password and log in via ssh into the public ip,

```
$ ssh <username>@<Internet IP Address>
```

* Setting up an environment

The tutorial we were using made use of pyenv, we however choose to go with miniconda.

Then we installed Nginx

```
$ yum install epel-release
$ yum install nginx
```

* Point Domain name at internet ip addess.

We bought a domain fadianyuce.com and had it direct to the ip address of our server.

* Setting up uwsgi

Use uswgi_params from [here](https://github.com/nginx/nginx/blob/master/conf/uwsgi_params?spm=a2c65.11461447.0.0.4db8498eosHfx4)

We created a wsgi.py script which imports and runs our actuall application.
Then we created an .ini file descrbing how wsgi is to be used and implemented a systemd service that starts wsgi and creates a socket:

```
$ systemctl start app.service
```

* Setting up Nginx

Here is where we ran in some trouble as the tutorial we were following did not work for us.

First we were getting Nginx failures when trying to restart Nginx service, because its port was already in use.
Killing it before restarting helped:

```
$ pkill -f nginx 
$ systemctl restart nginx
```

Then we found that nginx did not have the correct permissions to read our wsgi socket, this fixed it:

```
$ chmod 666 /var/www/flaskapp/app.sock
```

Finally after modifying the nginx config to work as a proxy between the portand the wsgi socket we could restart nginx and the flask app was working.

* HTTPS

In order to serve our api on HTTPS we were following this [tutorial](https://medium.com/@nishankjaintdk/serving-a-website-on-a-registered-domain-with-https-using-nginx-and-lets-encrypt-8d482e01a682) in order to get an SSL certificate.
They have something called certbot to help installing a certificate.

```
certbot-auto --nginx -d fadianyuce.com -d www.fadianyuce.com --debug
```

* Landing Page

In order for the application to have something of a landing page we took a bootstrap
template from [here](https://getbootstrap.com/docs/3.4/getting-started/) and use it as our main page.



