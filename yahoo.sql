# this sql is creating table in phoenix to upload data from yahoo finance

drop table if exists yahoo;
create table if not exists yahoo (
    v_datetime TIMESTAMP,
    v_OPEN varchar(10,2) not null,
    v_HIGH varchar(10,2),
    v_LOW  varchar(10,2), 
    v_CLOSE varchar(10,2),
    v_VOLUME varchar(10,2),
	CONSTRAINT pk PRIMARY KEY (v_OPEN));
