# Project: 0x01. NoSQL

This repository contains a set of Python scripts that interact with a MongoDB database. The scripts perform various tasks related to managing data in a MongoDB database.

## Resources

### Read or watch:-

- [NoSQL Databases Explained](https://intranet.alxswe.com/rltoken/wweK7dOY4pf8haCqv9Iv6Q)
- [What is NoSQL ?](https://intranet.alxswe.com/rltoken/QqqNmgzgwopHBv305ki6bg)
- [MongoDB with Python Crash Course - Tutorial for Beginners](https://intranet.alxswe.com/rltoken/RyyP9OH1EMBWWYpTs4TqoA)
- [MongoDB Tutorial 2 : Insert, Update, Remove, Query](https://intranet.alxswe.com/rltoken/9__3tR-NimgXlmjPQwTF-Q)
- [Aggregation](https://intranet.alxswe.com/rltoken/ziEDeniRobC6owPE1_avAQ)
- [Introduction to MongoDB and Python](https://intranet.alxswe.com/rltoken/axwwF4CjO7FnK8Ecochqnw)
- [mongo Shell Methods](https://intranet.alxswe.com/rltoken/lUqnLwOHbbp9FK39ijNmDQ)
- [Mongosh](https://intranet.alxswe.com/rltoken/ipHIVVmAsezINqpk7W0eow)

## Learning Objectives

### General

- What NoSQL means
- What is difference between SQL and NoSQL
- What is ACID
- What is a document storage
- What are NoSQL types
- What are benefits of a NoSQL database
- How to query information from a NoSQL database
- How to insert/update/delete information from a NoSQL database
- How to use MongoDB

## Installation and Setup

Before running the scripts, ensure you have the following prerequisites:

- Python 3.7
- PyMongo 3.10
- MongoDB installed and running on your system
- Git (optional, for cloning the repository)

To install PyMongo, you can use `pip`:

```bash
pip install pymongo==3.10
```

## Install MongoDB 4.2 in Ubuntu 18.04

- [Official installation guide](https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-ubuntu/)

```bash
$ wget -qO - https://www.mongodb.org/static/pgp/server-4.2.asc | apt-key add -
$ echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.2 multiverse" > /etc/apt/sources.list.d/mongodb-org-4.2.list
$ sudo apt-get update
$ sudo apt-get install -y mongodb-org
...
$  sudo service mongod status
mongod start/running, process 3627
$ mongo --version
MongoDB shell version v4.2.8
git version: 43d25964249164d76d5e04dd6cf38f6111e21f5f
OpenSSL version: OpenSSL 1.1.1  11 Sep 2018
allocator: tcmalloc
modules: none
build environment:
    distmod: ubuntu1804
    distarch: x86_64
    target_arch: x86_64
$  
$ pip3 install pymongo
$ python3
>>> import pymongo
>>> pymongo.__version__
'3.10.1'
```

Potential issue if documents creation doesn’t work or this error: `Data directory /data/db not found., terminating` ([source](https://bryantson.medium.com/fixing-data-db-not-found-error-in-macos-x-when-starting-mongodb-d7b82abb2479) and [source](https://stackoverflow.com/questions/37702957/mongodb-data-db-not-found))

```bash
$ sudo mkdir -p /data/db
```

Or if `/etc/init.d/mongod` is missing, please find here an example of the file:

<details>
<summary>Click to expand/hide file contents</summary>

```bash

#!/bin/sh
### BEGIN INIT INFO
# Provides:          mongod
# Required-Start:    $network $local_fs $remote_fs
# Required-Stop:     $network $local_fs $remote_fs
# Should-Start:      $named
# Should-Stop:
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: An object/document-oriented database
# Description:       MongoDB is a high-performance, open source, schema-free
#                    document-oriented data store that's easy to deploy, manage
#                    and use. It's network accessible, written in C++ and offers
#                    the following features:
#
#                       * Collection oriented storage - easy storage of object-
#                         style data
#                       * Full index support, including on inner objects
#                       * Query profiling
#                       * Replication and fail-over support
#                       * Efficient storage of binary data including large
#                         objects (e.g. videos)
#                       * Automatic partitioning for cloud-level scalability
#
#                    High performance, scalability, and reasonable depth of
#                    functionality are the goals for the project.
### END INIT INFO

PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
DAEMON=/usr/bin/mongod
DESC=database

NAME=mongod
# Defaults.  Can be overridden by the /etc/default/$NAME
# Other configuration options are located in $CONF file. See here for more:
# http://dochub.mongodb.org/core/configurationoptions
CONF=/etc/mongod.conf
PIDFILE=/var/run/$NAME.pid
ENABLE_MONGOD=yes

# Include mongodb defaults if available.
# All variables set before this point can be overridden by users, by
# setting them directly in the defaults file. Use this to explicitly
# override these values, at your own risk.
if [ -f /etc/default/$NAME ] ; then
        . /etc/default/$NAME
fi

# Handle NUMA access to CPUs (SERVER-3574)
# This verifies the existence of numactl as well as testing that the command works
NUMACTL_ARGS="--interleave=all"
if which numactl >/dev/null 2>/dev/null && numactl $NUMACTL_ARGS ls / >/dev/null 2>/dev/null
then
    NUMACTL="`which numactl` -- $NUMACTL_ARGS"
    DAEMON_OPTS=${DAEMON_OPTS:-"--config $CONF"}
else
    NUMACTL=""
    DAEMON_OPTS="-- "${DAEMON_OPTS:-"--config $CONF"}
fi


if test ! -x $DAEMON; then
    echo "Could not find $DAEMON"
    exit 0
fi

if test "x$ENABLE_MONGOD" != "xyes"; then
    exit 0
fi

. /lib/lsb/init-functions

STARTTIME=1
DIETIME=10                  # Time to wait for the server to die, in seconds
                            # If this value is set too low you might not
                            # let some servers to die gracefully and
                            # 'restart' will not work

DAEMONUSER=${DAEMONUSER:-mongodb}
DAEMONGROUP=${DAEMONGROUP:-mongodb}

set -e

running_pid() {
# Check if a given process pid's cmdline matches a given name
    pid=$1
    name=$2
    [ -z "$pid" ] && return 1
    [ ! -d /proc/$pid ] &&  return 1
    cmd=`cat /proc/$pid/cmdline | tr "\000" "\n"|head -n 1 |cut -d : -f 1`
    # Is this the expected server
    [ "$cmd" != "$name" ] &&  return 1
    return 0
}

running() {
# Check if the process is running looking at /proc
# (works for all users)

    # No pidfile, probably no daemon present
    [ ! -f "$PIDFILE" ] && return 1
    pid=`cat $PIDFILE`
    running_pid $pid $DAEMON || return 1
    return 0
}

start_server() {
            # Start the process using the wrapper
            start-stop-daemon --background --start --quiet --pidfile $PIDFILE \
                        --make-pidfile --chuid $DAEMONUSER:$DAEMONGROUP \
                        --exec $NUMACTL $DAEMON $DAEMON_OPTS
            errcode=$?
        return $errcode
}

stop_server() {
# Stop the process using the wrapper
            start-stop-daemon --stop --quiet --pidfile $PIDFILE \
                        --retry 300 \
                        --user $DAEMONUSER \
                        --exec $DAEMON
            errcode=$?
        return $errcode
}

force_stop() {
# Force the process to die killing it manually
        [ ! -e "$PIDFILE" ] && return
        if running ; then
                kill -15 $pid
        # Is it really dead?
                sleep "$DIETIME"s
                if running ; then
                        kill -9 $pid
                        sleep "$DIETIME"s
                        if running ; then
                                echo "Cannot kill $NAME (pid=$pid)!"
                                exit 1
                        fi
                fi
        fi
        rm -f $PIDFILE
}


case "$1" in
  start)
        log_daemon_msg "Starting $DESC" "$NAME"
        # Check if it's running first
        if running ;  then
            log_progress_msg "apparently already running"
            log_end_msg 0
            exit 0
        fi
        if start_server ; then
            # NOTE: Some servers might die some time after they start,
            # this code will detect this issue if STARTTIME is set
            # to a reasonable value
            [ -n "$STARTTIME" ] && sleep $STARTTIME # Wait some time
            if  running ;  then
                # It's ok, the server started and is running
                log_end_msg 0
            else
                # It is not running after we did start
                log_end_msg 1
            fi
        else
            # Either we could not start it
            log_end_msg 1
        fi
        ;;
  stop)
        log_daemon_msg "Stopping $DESC" "$NAME"
        if running ; then
            # Only stop the server if we see it running
                        errcode=0
            stop_server || errcode=$?
            log_end_msg $errcode
        else
            # If it's not running don't do anything
            log_progress_msg "apparently not running"
            log_end_msg 0
            exit 0
        fi
        ;;
  force-stop)
        # First try to stop gracefully the program
        $0 stop
        if running; then
            # If it's still running try to kill it more forcefully
            log_daemon_msg "Stopping (force) $DESC" "$NAME"
                        errcode=0
            force_stop || errcode=$?
            log_end_msg $errcode
        fi
        ;;
  restart|force-reload)
        log_daemon_msg "Restarting $DESC" "$NAME"
                errcode=0
        stop_server || errcode=$?
        # Wait some sensible amount, some server need this
        [ -n "$DIETIME" ] && sleep $DIETIME
        start_server || errcode=$?
        [ -n "$STARTTIME" ] && sleep $STARTTIME
        running || errcode=$?
        log_end_msg $errcode
        ;;
  status)

        log_daemon_msg "Checking status of $DESC" "$NAME"
        if running ;  then
            log_progress_msg "running"
            log_end_msg 0
        else
            log_progress_msg "apparently not running"
            log_end_msg 1
            exit 1
        fi
        ;;
  # MongoDB can't reload its configuration.
  reload)
        log_warning_msg "Reloading $NAME daemon: not implemented, as the daemon"
        log_warning_msg "cannot re-read the config file (use restart)."
        ;;

  *)
        N=/etc/init.d/$NAME
        echo "Usage: $N {start|stop|force-stop|restart|force-reload|status}" >&2
        exit 1
        ;;
esac

exit 0
    
```

</details>

## Tasks

### 0. [List all databases](./0-list_databases) :-

Write a script that lists all databases in MongoDB.

```bash
guillaume@ubuntu:~/0x01$ cat 0-list_databases | mongo
MongoDB shell version v3.6.3
connecting to: mongodb://127.0.0.1:27017
MongoDB server version: 3.6.3
admin        0.000GB
config       0.000GB
local        0.000GB
logs         0.005GB
bye
guillaume@ubuntu:~/0x01$
```

### 1. [Create a database](./1-use_or_create_database) :-

Write a script that creates or uses the database `my_db`:

```bash
guillaume@ubuntu:~/0x01$ cat 0-list_databases | mongo
MongoDB shell version v3.6.3
connecting to: mongodb://127.0.0.1:27017
MongoDB server version: 3.6.3
admin        0.000GB
config       0.000GB
local        0.000GB
logs         0.005GB
bye
guillaume@ubuntu:~/0x01$
guillaume@ubuntu:~/0x01$ cat 1-use_or_create_database | mongo
MongoDB shell version v3.6.3
connecting to: mongodb://127.0.0.1:27017
MongoDB server version: 3.6.3
switched to db my_db
bye
guillaume@ubuntu:~/0x01$
```

### 2. [Insert document](./2-insert) :-

Write a script that inserts a document in the collection `school`:

- The document must have one attribute `name` with value “Holberton school”
- The database name will be passed as option of `mongo` command

```bash
guillaume@ubuntu:~/0x01$ cat 2-insert | mongo my_db
MongoDB shell version v3.6.3
connecting to: mongodb://127.0.0.1:27017/my_db
MongoDB server version: 3.6.3
WriteResult({ "nInserted" : 1 })
bye
guillaume@ubuntu:~/0x01$
```

### 3. [All documents](./3-all) :-

Write a script that lists all documents in the collection `school`:

- The database name will be passed as option of `mongo` command

```bash
guillaume@ubuntu:~/0x01$ cat 3-all | mongo my_db
MongoDB shell version v3.6.3
connecting to: mongodb://127.0.0.1:27017/my_db
MongoDB server version: 3.6.3
{ "_id" : ObjectId("5a8fad532b69437b63252406"), "name" : "Holberton school" }
bye
guillaume@ubuntu:~/0x01$
```

### 4. [All matches](./4-match) :-

Write a script that lists all documents with `name="Holberton school"` in the collection `school`:

- The database name will be passed as option of `mongo` command

```bash
guillaume@ubuntu:~/0x01$ cat 4-match | mongo my_db
MongoDB shell version v3.6.3
connecting to: mongodb://127.0.0.1:27017/my_db
MongoDB server version: 3.6.3
{ "_id" : ObjectId("5a8fad532b69437b63252406"), "name" : "Holberton school" }
bye
guillaume@ubuntu:~/0x01$
```

### 5. [Count](./5-count) :-


| Task | File |
| ---- | ---- |
| 5. Count | [5-count](./5-count) |
| 6. Update | [6-update](./6-update) |
| 7. Delete by match | [7-delete](./7-delete) |
| 8. List all documents in Python | [8-all.py](./8-all.py) |
| 9. Insert a document in Python | [9-insert_school.py](./9-insert_school.py) |
| 10. Change school topics | [10-update_topics.py](./10-update_topics.py) |
| 11. Where can I learn Python? | [11-schools_by_topic.py](./11-schools_by_topic.py) |
| 12. Log stats | [12-log_stats.py](./12-log_stats.py) |