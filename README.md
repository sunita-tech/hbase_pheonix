
Setting up Pheonix on Hbase with CDP DC 7.0.3 with tutorial and Demo

Summary:

          1> Setting up Phoenix
          2> Demo for Phoenix interective sql
          3> Demo for Phoenix script for bulk upload
          4> Demo for Phoenix spark script

1 > Setting up Phoenix:

          Steps

          Follow the steps as listed here : https://docs.cloudera.com/runtime/7.0.3/phoenix-access-data/topics/phoenix-mapping-schemas.html


1 > 

Locate the HBase service > Configuration tab > Scope > (Service-Wide) > HBase Service Advanced Configuration Snippet (Safety Valve) for hbase-site.xml

          Name: phoenix.schema.isNamespaceMappingEnabled
          Value: true
          
Description: Enables mapping of tables of a Phoenix schema to a non-default HBase namespace. To enable mapping of a schema to a non-default namespace, set the value of this property to true. The default setting for this property is false.

     Name: phoenix.schema.mapSystemTablesToNamespace
     Value: true
     
Description: With true setting (default): After namespace mapping is enabled with the other property, all system tables, if any, are migrated to a namespace called system. With false setting: System tables are associated with the default namespace.

2> 

Go to the HBase service > Configuration tab >Select Scope > Gateway > Locate the HBase Client Advanced Configuration Snippet (Safety Valve) for hbase-site.xml property or search for it by typing its name in the Search box.

Add the following property values:

     Name: phoenix.schema.isNamespaceMappingEnabled
     Value: true
Description: Enables mapping of tables of a Phoenix schema to a non-default HBase namespace. To enable mapping of the schema to a non-default namespace, set the value of this property to true. The default setting for this property is false.


     Name: phoenix.schema.mapSystemTablesToNamespace
     Value: true
Description: With true setting (default): After namespace mapping is enabled with the other property, all system tables, if any, are migrated to a namespace called system.With false setting: System tables are associated with the default namespace.

3> Restart the role and service when Cloudera Manager prompts you to restart.

4> check in Ranger if user exists under Hbase that will have permission to add/delete tables in Hbase:
 click on ranger webui > access manager > role based policies > click on cm_hbase > check "all - table, column-family, column"   >check under users > e.g. hbase,admin or clouder-scm (used in example below)



2 > Demo for Phonix Interective SQL :

    SSH to Hbase node( look in cm for Hbase instance) with hbase user and goto Phoenix SQL 

     $sudo -u hbase -s /bin/bash 
     $kinit cloudera-scm/admin
     provide password eg Clouder20!
     cd ~
     $/usr/bin/phoenix-sqlline

     #For a successful to login to Phoenix SQL you will see something like below, before prompt as "jdbc:phoenix:>" 
          Building list of tables and columns for tab-completion (set fastconnect to true to skip)...
          134/134 (100%) Done
          Done
          sqlline version 1.2.0
          jdbc:phoenix:>

     1 > check existing tables, you should see something like below:

     jdbc:phoenix:> !tables
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
    4> Now insert some values to this table as below
    
      0: jdbc:phoenix:> upsert into  us_population VALUES ('NY', 'NEW YORK' , 8143179);
      1 row affected (0.066 seconds)
      0: jdbc:phoenix:> upsert into  us_population VALUES ('CA', 'LOS ANGELES' , 3844829);
      1 row affected (0.006 seconds)

    5> check the values 

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

     6> Now exit from check from hbase shell 

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

         You can see details of the us_population table in hbase

        hbase(main):005:0> scan 'US_POPULATION'
        ROW                                      COLUMN+CELL                                                                                                         
         CALOS ANGELES                           column=0:\x00\x00\x00\x00, timestamp=1584644064195, value=x                                                         
         CALOS ANGELES                           column=0:\x80\x0B, timestamp=1584644064195, value=\x80\x00\x00\x00\x00:\xAA\xDD                                     
         NYNEW YORK                              column=0:\x00\x00\x00\x00, timestamp=1584644008603, value=x                                                         
         NYNEW YORK                              column=0:\x80\x0B, timestamp=1584644008603, value=\x80\x00\x00\x00\x00|AK                                           
        2 row(s)

    Finally goto Phoenix and drop the us_population table
   
     0: jdbc:phoenix:> drop table us_population;
     No rows affected (1.126 seconds)

     Verify from hbase shell , with list command, you wont see the table in hbase.
     
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
            
           
     
     
     
 3 > Demo for Loading bult data using Phoenix SQL:

           1>  Download yahoo.sql
           2>  Download python script to generate bulk load in CSV format (yahoodata.py)
           3>  Execute script using phoenix script
 
          Output/s:
          
           File output sample from python code
           
           [hbase@ip-172-31-23-254 ~]$ python ydata.py > yahoo.csv
                                     $ cat yahoo.csv   ( Note : open file and remove header line)
            
                    Datetime,OPEN,HIGH,LOW,CLOSE,VOLUME
                    2020-03-20 06:30:00,7.074999809265137,7.139900207519531,6.989999771118164,7.099999904632568,489415.0
                    2020-03-20 06:31:00,7.059999942779541,7.079999923706055,6.909999847412109,6.956200122833252,27495.0
                    2020-03-20 06:32:00,6.909999847412109,7.039999961853027,6.889999866485596,7.000100135803223,15921.0
                    2020-03-20 06:33:00,7.150000095367432,7.150000095367432,7.139999866485596,7.139999866485596,25246.0
                    2020-03-20 06:34:00,7.150000095367432,7.210000038146973,7.110000133514404,7.150000095367432,32884.0
                    2020-03-20 06:35:00,7.170000076293945,7.320000171661377,7.159999847412109,7.293099880218506,69648.0
                    2020-03-20 06:36:00,7.28000020980835,7.28000020980835,7.099999904632568,7.110000133514404,41905.0
                    2020-03-20 06:37:00,7.099999904632568,7.129899978637695,6.940000057220459,6.949999809265137,39185.0
                    2020-03-20 06:38:00,6.960000038146973,7.0,6.840000152587891,6.909999847412109,45975.0
                    2020-03-20 06:39:00,6.929999828338623,7.039999961853027,6.929999828338623,7.03000020980835,31592.0
                    
                    Execute script output
                    
                    [hbase@ip-172-31-23-254 ~]$ /usr/bin/phoenix-psql yahoo.sql yahoo.csv
                                        SLF4J: Class path contains multiple SLF4J bindings.
                                       ........]
                                        
                                        no rows deleted
                                        Time: 1.096 sec(s)
                                        csv columns from database.
                                        CSV Upsert complete. 388 rows upserted
                                        Time: 0.109 sec(s)


                    Check the details in table:
                   
                     hbase@ip-172-31-23-254 ~]$ /usr/bin/phoenix-sqlline
                     
                     0: jdbc:phoenix:> select * from yahoo limit 5;
                    +----------------------+---------+---------+--------+----------+-----------+
                    |      V_DATETIME      | V_OPEN  | V_HIGH  | V_LOW  | V_CLOSE  | V_VOLUME  |
                    +----------------------+---------+---------+--------+----------+-----------+
                    | 2020-03-20 12:20:00  | 6.73    | 6.78    | 6.73   | 6.78     | 18054     |
                    | 2020-03-20 12:18:00  | 6.75    | 6.76    | 6.73   | 6.73     | 14187     |
                    | 2020-03-20 12:25:00  | 6.76    | 6.84    | 6.76   | 6.82     | 23605     |
                    | 2020-03-20 12:21:00  | 6.77    | 6.8     | 6.76   | 6.76     | 15863     |
                    | 2020-03-20 12:24:00  | 6.78    | 6.78    | 6.76   | 6.76     | 11962     |
                    +----------------------+---------+---------+--------+----------+-----------+
