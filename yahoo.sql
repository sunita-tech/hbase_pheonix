# this sql is creating table in phoenix to upload data from API for yahoo finance

drop table if exists yahoo;
create table if not exists yahoo (
    v_datetime varchar(20),
    v_OPEN decimal(10,2) not null,
    v_HIGH decimal(10,2),
    v_LOW  decimal(10,2),
    v_CLOSE decimal(10,2),
    v_VOLUME decimal(10,2)
        CONSTRAINT pk PRIMARY KEY (v_OPEN));                                        
