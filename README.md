# Intro
This repository contains all the tools needed to perform integration tests against a dockerized logstash.
In short, it will start a container, copy the logstash configuration files to there and run tests against it.

# Requirements
You will need to have `python` (v2.7 or 3.x), `docker` (v.18+) and `docker-compose` (v.1.24+) installed to run the project.

# How to run the tests
Logstash needs an input to read the events, filters to process the events and an output to specify where to send the
processed event.
In this project we only have the input and the output files, we don't have the filters. It's not added to the
repository because they are very specific to the needs of whoever uses logstash.

So, you will need to create a `filters` folder whith all your filters there. If you have more than one `.conf` file,
they will be loaded by logstash in an alphabetically order.

After that, you will need to change the `data/input.json` field to have the data that you want to use and test.

## input.json example
In the example that is commmited in this repo, we are providing logstash with an event with the value
```
log message
```

And 2 fields:
```
[field1]
[nested][field]
```

We have 2 expectations (the `expectations` array). These expectations will be tested against the values of
the 2 fields already mentioned. If one of them does not match, one of the scripts will return an error code with the
failure.

## tl;dr

* Create a `filters` folder;
* Add your logstash filter files to the folder, alphabetically ordered;
* Change the `data/input.json` file. 
