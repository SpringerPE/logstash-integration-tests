# Official logstash release. Change the version accordingly
FROM docker.elastic.co/logstash/logstash:6.6.1

# Creating the /data folder with the right permissions
USER root
RUN mkdir /data
RUN chown -R logstash:logstash /data
USER logstash

# Need to disable xpack otherwise logstash won't start
ENV XPACK_MONITORING_ENABLED false

# Remove the default conf files
RUN rm -f /usr/share/logstash/pipeline/*.conf
# Adding the input, output and filters to logstash
ADD conf/ /usr/share/logstash/pipeline/
ADD filters/ /usr/share/logstash/pipeline/
# Add the input.log file, which will be used to consume events
ADD data/input.log /tmp/input.log
