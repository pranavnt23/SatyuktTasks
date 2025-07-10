create database fms_app;
use fms_app;

create table user_registration (
    full_name varchar(30),
    email varchar(30),
    mobile_no varchar(20) unique,
    country_code varchar(5),
    category varchar(30),
    registration_date timestamp default current_timestamp
);

create table user_credentials (
    user_id int(3) unsigned zerofill auto_increment primary key,
    user_name varchar(20) unique, 
    password varchar(50),
    api_key varchar(70)
);

create table product_details (
    product_id int(5) unsigned zerofill auto_increment,
    user_id int(3) unsigned zerofill,
    product_name varchar(50),
    quantity int,
    price decimal(10,2),
    timestamp timestamp default current_timestamp,
    foreign key (user_id) references user_credentials(user_id)
);


