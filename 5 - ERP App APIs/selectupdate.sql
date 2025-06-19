show databases;
use erp_app;
show tables;

/*select queries*/
select * from user_registration;
select * from user_credentials;
select * from user_category_accountID;

select * from order_details;
select * from stock_details;
select * from product_details;
select * from employee_details;
select * from production_details;


/*delete queries*/
delete from user_registration where email='testuser@example.com';
delete from user_credentials where user_id=0006;
delete from user_category_accountID where userID=5;
DELETE FROM order_details;


/*dec commands*/
desc user_category_accountID;
desc production_details;
desc employee_details;