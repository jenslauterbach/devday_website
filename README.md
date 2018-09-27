# Dev Day website

The Dev Day website is built using [Django CMS](https://www.django-cms.org/).
And consists of a Django CMS content management part and some custom Django
apps for talk, attendee and speaker management.

## Running the development environment

You can run a local development environment easily with Docker and Docker Compose.  Make sure you have a current version both installed.

You can use [run.sh](./run.sh) to build, start and stop the Docker containers,
import a database dump, and purge all local data.

These commands are supported:

## `backup`: Create a backup

This creates a backup of the database and the media files. It creates a `db-`_timestamp_`.sql.gz` file with the database contents, and a `media-`_timestamp_`.tar.gz` file with the contents of the `devday/media` directory. Both are created in the backup directory; the _timestamp_ is the current date and time.

```
$ ./run.sh backup
*** Running backup
Starting devday_hp_db_1 ... done
+ cd /srv/devday/backup
++ date +%Y%m%d-%H%M%S%z
+ BACKUPDATE=20180913-141636+0000
+ pg_dump -U devday -h db -p 5432 devday
+ gzip
+ tar czf media-20180913-141636+0000.tar.gz -C /srv/devday/media .
```

## `build`: Build the necessary Docker images

This should only be necessary if Postgres, Django or other service and framework versions change.

```
$ ./run.sh build
Building db
Step 1/5 : FROM postgres
 ---> 978b82dc00dc

...

Step 5/5 : COPY httpd.conf /usr/local/apache2/conf/
 ---> Using cache
 ---> bb9f9690b35b
Successfully built bb9f9690b35b
Successfully tagged devday_hp_revproxy:latest
```

## `devdata`: Create database contents suitable for development

This will fill an empty database with pages, events, and attendees.

It also creates an admin user `admin@devday.de` with password `admin`.

```
$ ./run.sh devdata
    Starting containers
Creating network "devday_hp_default" with the default driver
Creating volume "devday_hp_devday_media" with default driver
Creating volume "devday_hp_devday_static" with default driver
...
```

## `logs`: Show Logs of the App Container

Tail the logs from the app container, which is running `manage.py runserver`.

```
$ ./run.sh log
Attaching to devday_hp_app_1
app_1    | Performing system checks...
app_1    |
app_1    | System check identified no issues (0 silenced).
app_1    |
app_1    | You have unapplied migrations; your app may not work properly until they are applied.
app_1    | Run 'python manage.py migrate' to apply them.
app_1    | September 27, 2018 - 19:48:29
app_1    | Django version 1.9.8, using settings 'devday.settings.dev'
app_1    | Starting development server at http://0.0.0.0:8000/
app_1    | Quit the server with CONTROL-C.
```

## `manage`: Run Django Admin

For development and maintenance tasks, run the Django Admin command inside the app container. This simply runs `python manage.py $@`.

```
$ ./run.sh manage migrate
```

## `restore`: Start the development environment and import a database dump.

Any preexisting volumes will be deleted first
```
$ ./run.sh -d backup/db-20180904-133216.sql.gz -m backup/media-20180904-133216.tar.gz restore
*** Importing database dump /Users/stbe/Downloads/devday/db-20180904-133216.sql.gz and media dump /Users/stbe/Downloads/devday/media-20180904-133216.tar.gz
    Deleting all containers and volumes
Removing network devday_hp_default
WARNING: Network devday_hp_default not found.
Removing volume devday_hp_devday_media
WARNING: Volume devday_hp_devday_media not found.

...

Applying filer.0009_auto_20171220_1635... OK
Applying filer.0010_auto_20180414_2058... OK
*** Import completed
```

## `purge`: Purge all containers and volumes

```
$ ./run.sh purge
*** Purge data
    Deleting all containers and volumes
Stopping devday_hp_revproxy_1 ... done
Stopping devday_hp_app_1      ... done
Stopping devday_hp_db_1       ... done
Removing devday_hp_revproxy_1 ... done
Removing devday_hp_app_1      ... done
Removing devday_hp_db_1       ... done
Removing network devday_hp_default
Removing volume devday_hp_devday_media
Removing volume devday_hp_devday_static
Removing volume devday_hp_pg_data
    Deleting media files
```

## `shell`: Run a shell in the app container
This command starts an interactive shell inside the app container, which contains the Python environment.

```
$ ./run.sh shell
*** Starting shell in app container
root@d46a19f94493:/srv/devday/devday# ls -l
total 80
drwxr-xr-x 20 root root   640 Sep 11 13:10 attendee
-rw-r--r--  1 root root    88 Sep 14 15:17 dev_requirements.txt
drwxr-xr-x 26 root root   832 Sep 13 17:00 devday
-rw-r--r--  1 root root 55935 Sep 14 15:16 devday.log
drwxr-xr-x 17 root root   544 Sep 14 11:02 event
-rw-r--r--  1 root root   249 Sep 11 12:55 manage.py
drwxr-xr-x  7 root root  4096 Sep 14 15:16 media
-rw-r--r--  1 root root   920 Sep 11 12:55 requirements.txt
-rw-r--r--  1 root root   206 Sep 11 12:55 setup.cfg
drwxr-xr-x  2 root root  4096 Sep 14 15:00 static
drwxr-xr-x 24 root root   768 Sep 11 14:49 talk
drwxr-xr-x 14 root root   448 Sep 11 14:49 twitterfeed
```


## `start`: Run the Django app
Start the development environment. Use existing volumes with data, or if they don't exist, with an empty data set, and run the Django app inside.

```
$ ./run.sh start
*** Starting all containers
Creating network "devday_hp_default" with the default driver
Creating devday_hp_db_1 ... done
Creating devday_hp_app_1 ... done
Creating devday_hp_revproxy_1 ... done
*** Running django app
Performing system checks...

System check identified no issues (0 silenced).
September 13, 2018 - 14:50:50
Django version 1.9.8, using settings 'devday.settings.dev'
Starting development server at http://0.0.0.0:8000/
Quit the server with CONTROL-C.
```

## `stop`: Stop the development environment

```
$ ./run.sh stop
Stopping devday_hp_revproxy_1 ... done
Stopping devday_hp_app_1      ... done
Stopping devday_hp_db_1       ... done
Removing devday_hp_revproxy_1 ... done
Removing devday_hp_app_1      ... done
Removing devday_hp_db_1       ... done
Removing network devday_hp_default
```


# URL Structure of the Dev Day Website

The site has been restructured to allow multiple events to be served concurrently.  Most URLs have been updated, and many of the existing views have been refactored.

## Public Information

* **/** Redirect to current event (as determined by Event.current_event())
* **/`event`/** Homepage, managed by DjangoCMS
* **/`event`/talk/** List of accepted talks for this event.  Once all accepted talks have been assigned a slot, this will show the session grid.
* **/`event`/talk/*slug*/`ID`** Detail page for an accepted talk, including speaker bio.

## Attendee And Speaker Management

Attendees, including speakers, can review and update their personal information.  People submitting a proposed talk will complete their attendee registration as part of the speaker registration, if they have not registered yet.

* **/account** Attendee account information.

## Speaker And Talk Information

* **/account/speaker** Speaker information; all registered users can input data here, but this is only required if the user wants to submit a talk proposal. The page also lists all talk proposals the user has made, and includes a link to submitting a new talk.  Talks are filtered by the current event (no past talks are shown).

## Committee Members

* **/committee/talks** Overview of all submitted talks, including links to speakers, talks.  The talks pages have the voting and comment functions.
(defined in `devday/talk/url-committee.py`)

## Special URLS

* **/schedule.xml** InfoBeamer data URL.
