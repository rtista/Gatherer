# Gatherer - Data Collection Web Application

HTTP API allows sending raw JSON formatted data into an ActiveMQ queue for later custom consumption. Consumers should be developed for each queue as each should save different data in a different way.

## System Dependencies

First you may need to install python dependencies on your system.

The table below shows which technologies require the packages whose installation is required.

Package | Required By
--------|------------
libev-devel | Bjoern HTTP Server
python2-devel | Bjoern HTTP Server
libpq-devel | Postgres SQL Driver (psycopg2)
mariadb-devel | MariaDB/MySQL Driver (mysqlclient)

On RedHat Based Distributions - Dnf

```bash
sudo dnf install libev-devel python3-devel libpq-devel mariadb-devel
```

On RedHat Based Distributions - Yum

```bash
sudo yum install libev-devel python3-devel libpq-devel mariadb-devel
```

On Debian Based Distributions - Apt

```bash
sudo apt-get install libev-devel python3-devel libpq-dev mariadb-dev
```

## Cloning

```bash
git clone git@github.com:rtista/Gatherer.git
```

## Pip Dependencies

```bash
cd Gatherer/
pip install -r requirements.txt
```

## Testing with dockers

You can test the application using dockers to provide architecture required systems (i.e. MariaDB, ActiveMQ, etc):

#### ActiveMQ

The following command will provide an ActiveMQ running on 127.0.0.1.
```bash
docker run --name activemq -p 8161:8161 -p 1883:1883 -p 5672:5672 -p 61613:61613 -p 61614:61614 -p 61616:61616 -d activemq
```

ActiveMQ provides a management graphical web interface which you can access onn http://127.0.0.1:8161/admin. In order to queue and dequeue messages you may use any of the following protocols:

Port | Protocol | Description
-----|----------|-------------
1883 | MQTT | Message Queuing Telemetry Transport
5672 | AMQP | ActiveMQ Messaging Protocol
61613 | Stomp | Simple/Streaming Text Oriented Message Protocol
61614 | WS | WebSocket
61616 | OpenWire | ActiveMQ Native Protocol

#### MariaDB

Run the following command and you may access the database on 127.0.0.1:3306 with the 'root' user and 'password' password.
```bash
docker run --name mariadb -p 3306:3306 -e MYSQL_ROOT_PASSWORD=password -d mariadb
```

#### Postgres

Run the following command and you may access the database on 127.0.0.1:5324 with the 'postgres' user and no password at the 'postgres' database.
```bash
docker run --name postgres -p 5432:5432 -d postgres
```
