
Setting up Pheonix on Hbase with CDP DC 7.0.3 

Steps

Follow the steps as listed here : https://docs.cloudera.com/runtime/7.0.3/phoenix-access-data/topics/phoenix-mapping-schemas.html


1 > 

Go to the HBase service > Configuration tab > Scope > (Service-Wide) ,add following property
Name: phoenix.schema.isNamespaceMappingEnabled
Value: true
Description: Enables mapping of tables of a Phoenix schema to a non-default HBase namespace. To enable mapping of a schema to a non-default namespace, set the value of this property to true. The default setting for this property is false.

Name: phoenix.schema.mapSystemTablesToNamespace
Value: true
Description: With true setting (default): After namespace mapping is enabled with the other property, all system tables, if any, are migrated to a namespace called system. With false setting: System tables are associated with the default namespace.

2> 

Go to the HBase service > Configuration tab >Select Scope > Gateway.
Locate the HBase Client Advanced Configuration Snippet (Safety Valve) for hbase-site.xml property or search for it by typing its name in the Search box.
Add the following property values:

Name: phoenix.schema.isNamespaceMappingEnabled
Value: true
Description: Enables mapping of tables of a Phoenix schema to a non-default HBase namespace. To enable mapping of the schema to a non-default namespace, set the value of this property to true. The default setting for this property is false.




Name: phoenix.schema.mapSystemTablesToNamespace
Value: true
Description: With true setting (default): After namespace mapping is enabled with the other property, all system tables, if any, are migrated to a namespace called system.With false setting: System tables are associated with the default namespace.


3> Restart the role and service when Cloudera Manager prompts you to restart.


4> check in ranger if user exists unde Hbase that will have permission to add/delete tables in Hbase
goto ranger > access manager > role based policies > click on cm_hbase > check "	all - table, column-family, column" has users
eg hbase or clouder-scm assigned 


Now ssh to Hbase node( look in cm for Hbase instance) with hbase user

     sudo -u hbase -s /bin/bash to change to hbase unix user.
     kinit hbase user or cloudera-scm/admin
     provide password eg Clouder20!
     $/usr/bin/phoenix-sqlline

#if successful you will see below for phoenix
     Building list of tables and columns for tab-completion (set fastconnect to true to skip)...
     134/134 (100%) Done
     Done
     sqlline version 1.2.0

Phoenix Demo:

1 > check existing tables, you should see something like below:

                         0: jdbc:phoenix:> !tables

                         +------------+--------------+-------------+---------------+----------+------------+----------------------------+-----------------+--------------+-----------+
                         | TABLE_CAT  | TABLE_SCHEM  | TABLE_NAME  |  TABLE_TYPE   | REMARKS  | TYPE_NAME  | SELF_REFERENCING_COL_NAME  | REF_GENERATION  | INDEX_STATE  | IMMUTABLE |
                         +------------+--------------+-------------+---------------+----------+------------+----------------------------+-----------------+--------------+-----------+
                         |            | SYSTEM       | CATALOG     | SYSTEM TABLE  |          |            |                            |                 |              | false     |
                         |            | SYSTEM       | FUNCTION    | SYSTEM TABLE  |          |            |                            |                 |              | false     |
                         |            | SYSTEM       | LOG         | SYSTEM TABLE  |          |            |                            |                 |              | true      |
                         |            | SYSTEM       | SEQUENCE    | SYSTEM TABLE  |          |            |                            |                 |              | false     |
                         |            | SYSTEM       | STATS       | SYSTEM TABLE  |          |            |                            |                 |              | false     |
                         +------------+--------------+-------------+---------------+----------+------------+----------------------------+-----------------+--------------+-----------+

2> create table in phoenix

        0: jdbc:phoenix:> create table if not exists us_population(
        . . . . . . . . > state char(2) not null,
        . . . . . . . . > city varchar not null,
        . . . . . . . . > polulation bigint,
        . . . . . . . . > constraint my_pk primary key (state,city));
        No rows affected (1.321 seconds)

3> check if table is created "us_population"
     0: jdbc:phoenix:> !tables
   0: jdbc:phoenix:> !tables
     +------------+--------------+----------------+---------------+----------+------------+----------------------------+-----------------+--------------+--------+
     | TABLE_CAT  | TABLE_SCHEM  |   TABLE_NAME   |  TABLE_TYPE   | REMARKS  | TYPE_NAME  | SELF_REFERENCING_COL_NAME  | REF_GENERATION  | INDEX_STATE  | IMMUTA |
     +------------+--------------+----------------+---------------+----------+------------+----------------------------+-----------------+--------------+--------+
     |            | SYSTEM       | CATALOG        | SYSTEM TABLE  |          |            |                            |                 |              | false  |
     |            | SYSTEM       | FUNCTION       | SYSTEM TABLE  |          |            |                            |                 |              | false  |
     |            | SYSTEM       | LOG            | SYSTEM TABLE  |          |            |                            |                 |              | true   |
     |            | SYSTEM       | SEQUENCE       | SYSTEM TABLE  |          |            |                            |                 |              | false  |
     |            | SYSTEM       | STATS          | SYSTEM TABLE  |          |            |                            |                 |              | false  |
     |            |              | US_POPULATION  | TABLE         |          |            |                            |                 |              | false  |
     +------------+--------------+----------------+---------------+----------+------------+----------------------------+-----------------+--------------+--------+
0
4> Now insert some values to this table as below

      0: jdbc:phoenix:> upsert into  us_population VALUES ('NY', 'NEW YORK' , 8143179);
      1 row affected (0.066 seconds)
      0: jdbc:phoenix:> upsert into  us_population VALUES ('CA', 'LOS ANGELES' , 3844829);
      1 row affected (0.006 seconds)

5 > check the values 

      SELECT * FROM US_POPULATION;
      +--------+--------------+-------------+
      | STATE  |     CITY     | POLULATION  |
      +--------+--------------+-------------+
      | CA     | LOS ANGELES  | 3844829     |
      | NY     | NEW YORK     | 8143179     |
      +--------+--------------+-------------+
      2 rows selected (0.024 seconds)
      0: jdbc:phoenix:> SELECT * FROM US_POPULATION WHERE STATE='CA';
      +--------+--------------+-------------+
      | STATE  |     CITY     | POLULATION  |
      +--------+--------------+-------------+
      | CA     | LOS ANGELES  | 3844829     |
      +--------+--------------+-------------+
      1 row selected (0.015 seconds)



6> 
Now exit from check from hbase shell 

      hbase(main):001:0> list
      TABLE                                                                                                                                                        
      SYSTEM:CATALOG                                                                                                                                               
      SYSTEM:FUNCTION                                                                                                                                              
      SYSTEM:LOG                                                                                                                                                   
      SYSTEM:MUTEX                                                                                                                                                 
      SYSTEM:SEQUENCE                                                                                                                                              
      SYSTEM:STATS                                                                                                                                                 
      ATLAS_ENTITY_AUDIT_EVENTS                                                                                                                                    
      US_POPULATION                                                                                                                                                
      atlas_janus                                                                                                                                                  
      test                                                                                                                                                         
10 row(s)
Took 0.2971 seconds                                                                                                                                          
=> ["SYSTEM:CATALOG", "SYSTEM:FUNCTION", "SYSTEM:LOG", "SYSTEM:MUTEX", "SYSTEM:SEQUENCE", "SYSTEM:STATS", "ATLAS_ENTITY_AUDIT_EVENTS", "US_POPULATION", "atlas_janus", "test"]

you can see the us_population table 


   hbase(main):005:0> scan 'US_POPULATION'
   ROW                                      COLUMN+CELL                                                                                                         
    CALOS ANGELES                           column=0:\x00\x00\x00\x00, timestamp=1584644064195, value=x                                                         
    CALOS ANGELES                           column=0:\x80\x0B, timestamp=1584644064195, value=\x80\x00\x00\x00\x00:\xAA\xDD                                     
    NYNEW YORK                              column=0:\x00\x00\x00\x00, timestamp=1584644008603, value=x                                                         
    NYNEW YORK                              column=0:\x80\x0B, timestamp=1584644008603, value=\x80\x00\x00\x00\x00|AK                                           
   2 row(s)

finally go to Phoenix and drop the us_population table
     0: jdbc:phoenix:> drop table us_population;
     No rows affected (1.126 seconds)

verify from hbase shell , with list command, you wont see the table in hbase.
   hbase(main):001:0> list
   TABLE                                                                                                                                                        
   SYSTEM:CATALOG                                                                                                                                               
   SYSTEM:FUNCTION                                                                                                                                              
   SYSTEM:LOG                                                                                                                                                   
   SYSTEM:MUTEX                                                                                                                                                 
   SYSTEM:SEQUENCE                                                                                                                                              
   SYSTEM:STATS                                                                                                                                                 
   ATLAS_ENTITY_AUDIT_EVENTS                                                                                                                                    
   atlas_janus                                                                                                                                                  
   test                                                                                                                                                         
   9 row(s)
