# UdaConnect
## Overview
### Background
Conferences and conventions are hotspots for making connections. Professionals in attendance often share the same interests and can make valuable business and personal connections with one another. At the same time, these events draw a large crowd and it's often hard to make these connections in the midst of all of these events' excitement and energy. To help attendees make connections, we are building the infrastructure for a service that can inform attendees if they have attended the same booths and presentations at an event.

### Goal
You work for a company that is building a app that uses location data from mobile devices. Your company has built a [POC](https://en.wikipedia.org/wiki/Proof_of_concept) application to ingest location data named UdaTracker. This POC was built with the core functionality of ingesting location and identifying individuals who have shared a close geographic proximity.

Management loved the POC so now that there is buy-in, we want to enhance this application. You have been tasked to enhance the POC application into a [MVP](https://en.wikipedia.org/wiki/Minimum_viable_product) to handle the large volume of location data that will be ingested.

To do so, ***you will refactor this application into a microservice architecture using message passing techniques that you have learned in this course***. It’s easy to get lost in the countless optimizations and changes that can be made: your priority should be to approach the task as an architect and refactor the application into microservices. File organization, code linting -- these are important but don’t affect the core functionality and can possibly be tagged as TODO’s for now!

### Technologies
* [Flask](https://flask.palletsprojects.com/en/1.1.x/) - API webserver
* [SQLAlchemy](https://www.sqlalchemy.org/) - Database ORM
* [PostgreSQL](https://www.postgresql.org/) - Relational database
* [PostGIS](https://postgis.net/) - Spatial plug-in for PostgreSQL enabling geographic queries]
* [Vagrant](https://www.vagrantup.com/) - Tool for managing virtual deployed environments
* [VirtualBox](https://www.virtualbox.org/) - Hypervisor allowing you to run multiple operating systems
* [K3s](https://k3s.io/) - Lightweight distribution of K8s to easily develop against a local cluster

## Running the app
The project has been set up such that you should be able to have the project up and running with Kubernetes.

### Prerequisites
We will be installing the tools that we'll need to use for getting our environment set up properly.
1. [Install Docker](https://docs.docker.com/get-docker/)
2. [Set up a DockerHub account](https://hub.docker.com/)
3. [Set up `kubectl`](https://rancher.com/docs/rancher/v2.x/en/cluster-admin/cluster-access/kubectl/)
4. [Install VirtualBox](https://www.virtualbox.org/wiki/Downloads) with at least version 6.0
5. [Install Vagrant](https://www.vagrantup.com/docs/installation) with at least version 2.0
6. [4 GB RAM at a running VM environment is recommended] - At least 4 GB RAM is recommended (deployment of Kafka and other microservices on machine with less RAM leads to Karka broker pod restarts)

### Environment Setup
To run the application, you will need a K8s cluster running locally and to interface with it via `kubectl`. We will be using Vagrant with VirtualBox to run K3s.

#### Initialize K3s
In this project's root, run `vagrant up`. 
```bash
$ vagrant up
```
The command will take a while and will leverage VirtualBox to load an [openSUSE](https://www.opensuse.org/) OS and automatically install [K3s](https://k3s.io/). When we are taking a break from development, we can run `vagrant suspend` to conserve some ouf our system's resources and `vagrant resume` when we want to bring our resources back up. Some useful vagrant commands can be found in [this cheatsheet](https://gist.github.com/wpscholar/a49594e2e2b918f4d0c4).

#### Set up `kubectl`
After `vagrant up` is done, you will SSH into the Vagrant environment and retrieve the Kubernetes config file used by `kubectl`. We want to copy the contents of this file into our local environment so that `kubectl` knows how to communicate with the K3s cluster.
```bash
$ vagrant ssh
```
You will now be connected inside of the virtual OS. Run `sudo cat /etc/rancher/k3s/k3s.yaml` to print out the contents of the file. You should see output similar to the one that I've shown below. Note that the output below is just for your reference: every configuration is unique and you should _NOT_ copy the output I have below.

Copy the contents from the output issued from your own command into your clipboard -- we will be pasting it somewhere soon!
```bash
$ sudo cat /etc/rancher/k3s/k3s.yaml

apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUJWekNCL3FBREFnRUNBZ0VBTUFvR0NDcUdTTTQ5QkFNQ01DTXhJVEFmQmdOVkJBTU1HR3N6Y3kxelpYSjIKWlhJdFkyRkFNVFU1T1RrNE9EYzFNekFlRncweU1EQTVNVE13T1RFNU1UTmFGdzB6TURBNU1URXdPVEU1TVROYQpNQ014SVRBZkJnTlZCQU1NR0dzemN5MXpaWEoyWlhJdFkyRkFNVFU1T1RrNE9EYzFNekJaTUJNR0J5cUdTTTQ5CkFnRUdDQ3FHU000OUF3RUhBMElBQk9rc2IvV1FEVVVXczJacUlJWlF4alN2MHFseE9rZXdvRWdBMGtSN2gzZHEKUzFhRjN3L3pnZ0FNNEZNOU1jbFBSMW1sNXZINUVsZUFOV0VTQWRZUnhJeWpJekFoTUE0R0ExVWREd0VCL3dRRQpBd0lDcERBUEJnTlZIUk1CQWY4RUJUQURBUUgvTUFvR0NDcUdTTTQ5QkFNQ0EwZ0FNRVVDSVFERjczbWZ4YXBwCmZNS2RnMTF1dCswd3BXcWQvMk5pWE9HL0RvZUo0SnpOYlFJZ1JPcnlvRXMrMnFKUkZ5WC8xQmIydnoyZXpwOHkKZ1dKMkxNYUxrMGJzNXcwPQotLS0tLUVORCBDRVJUSUZJQ0FURS0tLS0tCg==
    server: https://127.0.0.1:6443
  name: default
contexts:
- context:
    cluster: default
    user: default
  name: default
current-context: default
kind: Config
preferences: {}
users:
- name: default
  user:
    password: 485084ed2cc05d84494d5893160836c9
    username: admin
```
Type `exit` to exit the virtual OS and you will find yourself back in your computer's session. Create the file (or replace if it already exists) `~/.kube/config` and paste the contents of the `k3s.yaml` output here.

Afterwards, you can test that `kubectl` works by running a command like `kubectl describe services`. It should not return any errors.

### Steps to deploy refactored application

1. `kubectl apply -f pre-deployment/` - Let's first set up DB and Kafka environment, please invoke all subsequent commands as root user or with sudo
2. `sh scripts/run_db_command.sh <POSTGRES_POD_NAME>` - Seed your database against the `postgres` pod. (`kubectl get pods` will give you that postgres pod's name)
3. `./scripts/check_locations_records.sh <POSTGRES_POD_NAME>` - Let's check 'location' table records (let's check it before we add new dummy records), sample output:
./scripts/check_locations_records.sh postgres-5f676c995d-9jvx2
id  | person_id |                 coordinate                 |    creation_time
-----+-----------+--------------------------------------------+---------------------
 29 |         1 | 010100000000ADF9F197925EC0FDA19927D7C64240 | 2020-08-18 10:37:06
 30 |         5 | 010100000097FDBAD39D925EC0D00A0C59DDC64240 | 2020-08-15 10:37:06
 31 |         5 | 010100000000ADF9F197925EC0FDA19927D7C64240 | 2020-08-15 10:37:06

...
 65 |         9 | 010100000097FDBAD39D925EC0D00A0C59DDC64240 | 2020-07-07 10:37:06
 66 |         5 | 010100000097FDBAD39D925EC0D00A0C59DDC64240 | 2020-07-07 10:37:06
 67 |         8 | 010100000097FDBAD39D925EC0D00A0C59DDC64240 | 2020-07-07 10:37:06
 68 |         6 | 010100000097FDBAD39D925EC0D00A0C59DDC64240 | 2020-08-15 10:37:06
(39 rows)

4. `export KAFKA_POD_NAME=$(kubectl get pods --namespace default -l "app.kubernetes.io/name=kafka,app.kubernetes.io/instance=kafka,app.kubernetes.io/component=kafka" -o jsonpath="{.items[0].metadata.name}")` - before we deploy apps we should set up Kafka services and create topic 'locations'
5. `kubectl exec -it $KAFKA_POD_NAME -- kafka-topics.sh --create --bootstrap-server kafka-headless:9092 --replication-factor 1 --partitions 1 --topic locations` - create 'locations' topic in Kafka
6. `kubectl exec -it $KAFKA_POD_NAME -- kafka-topics.sh --describe --topic locations --bootstrap-server kafka-headless:9092` - fetch the describe output of 'locations' topic
7. `kubectl exec -it $KAFKA_POD_NAME -- kafka-console-consumer.sh --topic locations --from-beginning --bootstrap-server localhost:9092` - for the purpose of initial testing let's start consumer client, preferably starting the separate cli ssh/console session, for the next 2 steps open an additional ssh/cli session
8. `export KAFKA_POD_NAME=$(kubectl get pods --namespace default -l "app.kubernetes.io/name=kafka,app.kubernetes.io/instance=kafka,app.kubernetes.io/component=kafka" -o jsonpath="{.items[0].metadata.name}")`
9. `kubectl exec -it $KAFKA_POD_NAME -- kafka-console-producer.sh --topic locations --bootstrap-server kafka-headless:9092` - and let's type some message like "hi, I am here" and in consumer cli session above we would see the corresponding output of a transmissioned message. Please, for the next tests stay consumer cli session opened, terminate that producer session by invoking "Ctrl+C" 
10. `kubectl apply -f deployment/` - after we ensured the Kafka services are up and set up, let's apply the main deployment apps' manifests
11. `kubectl get pods` - ensure all services are in Running state and the abovementioned consumer cli session is still working
12. `kubectl apply -f post-deployment/` - let's deploy and start injecting 6 sample location records by deploying 'locations-generator' microservice
13. Check the consumer cli session, it will show up 6 new records:
{"id": 100, "person_id": 9, "longitude": "-106.5719566", "latitude": "35.0585136", "creation_time": "2021-11-06T10:10:10"}
{"id": 101, "person_id": 9, "longitude": "-106.5719566", "latitude": "35.0585136", "creation_time": "2021-11-06T10:10:10"}
{"id": 102, "person_id": 9, "longitude": "-106.5719566", "latitude": "35.0585136", "creation_time": "2021-11-06T10:10:10"}
{"id": 103, "person_id": 9, "longitude": "-106.5719566", "latitude": "35.0585136", "creation_time": "2021-11-06T10:10:10"}
{"id": 104, "person_id": 9, "longitude": "-106.5719566", "latitude": "35.0585136", "creation_time": "2021-11-06T10:10:10"}
{"id": 105, "person_id": 9, "longitude": "-106.5719566", "latitude": "35.0585136", "creation_time": "2021-11-06T10:10:10"}

14. `./scripts/check_locations_records.sh <POSTGRES_POD_NAME>` - check if transmitted 6 location records are in DB 'locations' table, sample output:
./scripts/check_locations_records.sh postgres-5f676c995d-9jvx2
 id  | person_id |                 coordinate                 |    creation_time
-----+-----------+--------------------------------------------+---------------------
  29 |         1 | 010100000000ADF9F197925EC0FDA19927D7C64240 | 2020-08-18 10:37:06
  30 |         5 | 010100000097FDBAD39D925EC0D00A0C59DDC64240 | 2020-08-15 10:37:06
  31 |         5 | 010100000000ADF9F197925EC0FDA19927D7C64240 | 2020-08-15 10:37:06
...
  66 |         5 | 010100000097FDBAD39D925EC0D00A0C59DDC64240 | 2020-07-07 10:37:06
  67 |         8 | 010100000097FDBAD39D925EC0D00A0C59DDC64240 | 2020-07-07 10:37:06
  68 |         6 | 010100000097FDBAD39D925EC0D00A0C59DDC64240 | 2020-08-15 10:37:06
 100 |         9 | 0101000000842FA75F7D874140CEEEDAEF9AA45AC0 | 2021-11-06 10:10:10
 101 |         9 | 0101000000842FA75F7D874140CEEEDAEF9AA45AC0 | 2021-11-06 10:10:10
 102 |         9 | 0101000000842FA75F7D874140CEEEDAEF9AA45AC0 | 2021-11-06 10:10:10
 103 |         9 | 0101000000842FA75F7D874140CEEEDAEF9AA45AC0 | 2021-11-06 10:10:10
 104 |         9 | 0101000000842FA75F7D874140CEEEDAEF9AA45AC0 | 2021-11-06 10:10:10
 105 |         9 | 0101000000842FA75F7D874140CEEEDAEF9AA45AC0 | 2021-11-06 10:10:10
(45 rows)

-, and that it, Locations entity microservices worked out.


### Verifying it Works
Once the project is up and running, you should be able to see 7 deployments and 9 services in Kubernetes:
`kubectl get deployment` and `kubectl get services` - should return:
NAME                             READY   UP-TO-DATE   AVAILABLE   AGE
postgres                         1/1     1            1           21h
udaconnect-app                   1/1     1            1           14h
udaconnect-locations2kafka       1/1     1            1           14h
udaconnect-locations-kafka2db    1/1     1            1           14h
udaconnect-locations-generator   1/1     1            1           13h
udaconnect-connections-api       1/1     1            1           13h
udaconnect-persons-api           1/1     1            1           12h

NAME                         TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)                      AGE
kubernetes                   ClusterIP   10.43.0.1       <none>        443/TCP                      13d
kafka-zookeeper-headless     ClusterIP   None            <none>        2181/TCP,2888/TCP,3888/TCP   21h
kafka-zookeeper              ClusterIP   10.43.156.139   <none>        2181/TCP,2888/TCP,3888/TCP   21h
kafka-headless               ClusterIP   None            <none>        9092/TCP,9093/TCP            21h
kafka                        ClusterIP   10.43.234.173   <none>        9092/TCP                     21h
udaconnect-app               NodePort    10.43.56.185    <none>        3000:30000/TCP               21h
postgres                     NodePort    10.43.10.179    <none>        5432:32078/TCP               15h
udaconnect-connections-api   NodePort    10.43.43.82     <none>        5000:30002/TCP               14h
udaconnect-locations2kafka   NodePort    10.43.51.141    <none>        5005:30005/TCP               14h
udaconnect-persons-api       NodePort    10.43.251.107   <none>        30001:30001/TCP              13h



These pages should also load on your web browser:
* `http://localhost:30001/` - OpenAPI Documentation
* `http://localhost:30001/api/` - Base path for API
* `http://localhost:30000/` - Frontend ReactJS Application

