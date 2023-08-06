Nagios sql
----------

Install:
========

From pip::

    pip3 install nagios_sql

From pip with github::

    pip3 install git+https://github.com/pablodav/nagios_sql.git

For development::

     # clone the repository
     python3 setup.py develop

Usage:
======

Get help and options::

    nagios_sql --help

    usage: nagios_sql [-h] [-H HOST]
                      [--test {db_state,logship_status,mirror_status,replication_status,sql_ping}]
                      [-U USER] [-P PASSWORD] [-v [VERSION]]

    optional arguments:
      -h, --help            show this help message and exit
      -H HOST, --host HOST  SQL Backup HOST to connect
      --test {db_state,logship_status,mirror_status,replication_status,sql_ping}, -t {db_state,logship_status,mirror_status,replication_status,sql_ping}
                            tests:
                              db_state
                              logship_status
                              mirror_status
                              replication_status
                              sql_ping
      -U USER, --user USER  User to auth to DB
      -P PASSWORD, --password PASSWORD
                            Password to auth to DB
      -v [VERSION], --version [VERSION]
                            Gets version number


Check replication_status::

    nagios_sql -H SERVERNAME -U 'USERNAME' -P 'PASSWORD' -t replication_status

    CRITICAL: Replication CRITICAL
    OK Pub:Test_Replication1 DB:Test_DB1 Status:Idle MaxLatency:31s
    CRITICAL Pub:Test_Replication1_2 DB:Test_DB1 Status:Failed MaxLatency:31s
    CRITICAL Pub:Test_Replication1_3 DB:Test_DB1 Status:Failed MaxLatency:31s
    OK Pub:Test_Replication1_4 DB:Test_DB1 Status:Idle MaxLatency:31s
    OK Pub:Test_Replication1_5 DB:Test_DB1 Status:Idle MaxLatency:31s
    CRITICAL Sub:SERVERNAME DB:Test_DB1_Reporting Status:Failed Latency:?s
    CRITICAL Sub:SERVERNAME DB:Test_DB1_Reporting Status:Failed Latency:?s
    OK Sub:SERVERNAME DB:Test_DB1_Reporting Status:Idle Latency:0s
    OK Sub:SERVERNAME DB:Test_DB1_Reporting Status:Idle Latency:0s
    OK Sub:SERVERNAME DB:Test_DB1_Reporting Status:Idle Latency:0s

Setup nagios command:
=====================

Configure you own `commands_nagios.cfg`::

    # standard way to define a command
    define command{
        command_name	check_nagios_sql
        command_line	nagios_sql -H $HOSTADDRESS$ -U $ARG1$ -P $ARG2 -t $ARG3
    }

    # this other custom settings will allow you to parse any argument
    # like:
    # command  check_nagios_sql_custom!"-U 'USERNAME' -P 'PASSWORD' -t replication_status"
    define command{
        command_name	check_nagios_sql_custom
        command_line	nagios_sql -H $HOSTADDRESS$ $ARG1$
    }

Automatic provisioned with ansible by: https://github.com/CoffeeITWorks/ansible_nagios4_server_plugins

Original author:
================

original code: http://code.activestate.com/recipes/577599-nagios-plugin-for-monitoring-database-servers/
Nagios_sql.py - Matt Keranen 2011 (mksql@yahoo.com)

Author:
=======

This script was refactored and also a python package was created by:

Pablo Estigarribia 201705 (pablodav at gmail)

Collaborators:
==============

--- put your name here ---

Troubleshooting replicas
========================

Some time when you are monitoring replicas, you can see some publication that doesn't exist anymore but they still
appears in `distribution` database.

The unique way to fix them is to drop the publication, but as it doesn't exist: SQL will fail trying to drop.
So here there are some steps to create and drop the publication:

This example is only for databases that already have some other publications working, but you need to create and drop
an missing publication that still appears in `distribution` database.

.. code-block:: sql

    -- Adding the transactional publication
    use [databasename]
    exec sp_addpublication @publication = N'MyReplPub',
    @description = N'Transactional publication of database ''databasename'' from Publisher ''servername''.',
    @sync_method = N'concurrent', @retention = 0, @allow_push = N'true', @allow_pull = N'true', @allow_anonymous = N'true',
    @enabled_for_internet = N'false', @snapshot_in_defaultfolder = N'true', @compress_snapshot = N'false', @ftp_port = 21,
    @ftp_login = N'anonymous', @allow_subscription_copy = N'false', @add_to_active_directory = N'false', @repl_freq = N'continuous',
    @status = N'active', @independent_agent = N'true', @immediate_sync = N'true', @allow_sync_tran = N'false',
    @autogen_sync_procs = N'false', @allow_queued_tran = N'false', @allow_dts = N'false', @replicate_ddl = 1,
    @allow_initialize_from_backup = N'false', @enabled_for_p2p = N'false', @enabled_for_het_sub = N'false'
    GO


    exec sp_droppublication @publication = N'MyReplPub'


Nice references:
================

https://www.mssqltips.com/sqlservertip/2710/steps-to-clean-up-orphaned-replication-settings-in-sql-server/
