# Getting Started

Make sure you have installed kafka and java on your system and then open terminal and go into the directory where you have installed your kafka and then follow these commands:

write this command to start zookeeper:
`bin/zookeeper-server-start.sh config/zookeeper.properties`

Change the [server.properties](http://server.properties) file

open new terminal and again go to the same root path where you have installed kafka and write the below command to start kafka server
`bin/kafka-server-start.sh config/server.properties`

Now we need to create a new topic, and for our assignment we are going to use reddit topic name, so open new terminal and create new topic with following command:
`bin/kafka-topics.sh --create --topic reddit --bootstrap-server localhost:9092`

`bin/kafka-topics.sh --create --topic elk --bootstrap-server localhost:9092`

Now we have to start the listener, which will start listening from the publisher:
`bin/kafka-console-consumer.sh --topic reddit --from-beginning --bootstrap-server localhost:9092`

`bin/kafka-console-consumer.sh --topic elk --from-beginning --bootstrap-server localhost:9092`

Now start the python script which will read from the reddit streaming API and publish data to the kafka’s **reddit** topic, name of that python file is:

**reddit_api.py**

Now to start the structured_streaming_word_count, open new terminal into the virtual environment where you have already installed the below dependencies:

- spacy - pip3 install spacy
- model - **python3 -m spacy download en_core_web_sm**

then use this command to start the named_entity counter application on the cluster:

`spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1 /Users/dhairyapatel/Documents/Assignment_3/structured_named_entity_count.py localhost:9092 subscribe reddit topic elk /Users/dhairyapatel/Documents/Assignment_3`

Now installing elk:

First we need to have docker onto your system, try following this documentation from this link:

[https://docs.docker.com/desktop/install/mac-install/#install-and-run-docker-desktop-on-mac](https://docs.docker.com/desktop/install/mac-install/#install-and-run-docker-desktop-on-mac)

try cloning this repository:

`git clone https://github.com/deviantony/docker-elk`

then try to get into the folder:

`cd docker-elk`

change this configurations files before proceeding:

- firstly go into the folder (docker-elk) and try to change the file at the location (./logstash/pipeline/)
- replace the file `logstash.conf` with the file(`logstash.conf`) that we have provided into the assignment submission.

then write these below two commands to start running up docker container. You have to make sure that you have already installed docker dekstop and it should be running on your system.

`docker-compose up --build`

start your browser and copy this link to enter kibana:

[http:localhost:5601](http://localhost:5601/)

and login into kibana with these credentials:

**username** : elastic

**password** : changeme

Check into the elasticsearch indices, there should be one index created with the name of elk.

You can go into the the Analytics section and then using Visualize library you can create visualization with the use of elk index stored in the elastic search.

# Results in Kibana

At 15 Mins:
![15 mins Image](https://github.com/Harsh251299/Real-Time-Name-Entity-Analysis/blob/main/Results/15Min.png)

At 30 Mins:
![30 mins Image](https://github.com/Harsh251299/Real-Time-Name-Entity-Analysis/blob/main/Results/30Min.png)

At 45 Mins:
![45 mins Image](https://github.com/Harsh251299/Real-Time-Name-Entity-Analysis/blob/main/Results/45Min.png)
