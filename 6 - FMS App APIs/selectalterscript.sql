use erp_app;

desc production_details;

select * from user_registration;
select * from production_details;
select * from payment_details;

delete from user_registration where mobile_no=9976334383;
delete from user_credentials where user_name=9976334383;
delete from product_details where product_name='Drip Kit';

SET SQL_SAFE_UPDATES=0;
show tables;