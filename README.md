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
