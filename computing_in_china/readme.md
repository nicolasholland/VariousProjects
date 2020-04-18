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


