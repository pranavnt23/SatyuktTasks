show databases;
use erp_app;
show tables;

/*select queries*/
select * from user_registration;
select * from user_credentials;

desc production_details;
select * from employee_details;
select * from payment_details;
select * from raw_materials;

SET SQL_SAFE_UPDATES=0;

/*delete queries*/
delete from user_registration where mobile_no=9976334382;
delete from payment_details where user_id=1;
delete from raw_materials where material_id='RM005';
DELETE FROM order_details;


/*desc commands*/
desc user_category_accountID;
desc product_details;
desc employee_details;