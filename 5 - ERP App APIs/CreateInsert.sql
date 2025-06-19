show databases;
use erp_app;
show tables;

/**/

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


SET SQL_SAFE_UPDATES = 0;

select * from stock_details;
ALTER TABLE stock_details 
MODIFY COLUMN product_id INT NOT NULL NOT AUTO_INCREMENT,
ADD PRIMARY KEY (product_id);

ALTER TABLE product_details MODIFY product_id INT NOT NULL;


/*Inserting queries*/

INSERT INTO user_registration (full_name, email, mobile_no, country_code)
VALUES ("test1", "emailtest1", 9976334385, 91);

INSERT INTO stock_details (product_id, product_name, quantity_available, unit_of_measure)
VALUES 
(1000, 'Organic Fertilizer', 120, 'kg'),
(1001, 'Neem Pesticide', 80, 'litre'),
(1002, 'Bio-Compost', 150, 'kg'),
(1003, 'Drip Irrigation Kit', 30, 'unit'),
(1004, 'Greenhouse Film', 50, 'roll'),
(1005, 'Cocopeat Block', 100, 'block'),
(1006, 'Seedling Tray', 75, 'tray'),
(1007, 'Vermicompost', 200, 'kg'),
(1008, 'Liquid Seaweed Extract', 60, 'litre'),
(1009, 'Tractor Engine Oil', 40, 'litre');

INSERT INTO order_details (
    user_id, product_name, quantity, amount, dispatch_address, order_status
) VALUES
(7, 'Organic Fertilizer', 5, 980, '123 Green Farm Road, Mysore, Karnataka - 570001', 'pending'),
(8, 'Pesticide Spray', 3, 450, '45 Rural Lane, Coimbatore, Tamil Nadu - 641001', 'dispatched'),
(9, 'Hybrid Seeds Pack', 10, 1200, '78 Harvest Ave, Pune, Maharashtra - 411001', 'pending'),
(10, 'Soil Conditioner', 2, 600, '12 Agri Street, Raipur, Chhattisgarh - 492001', 'delivered'),
(11, 'Drip Irrigation Kit', 1, 2500, '234 Valley Road, Kochi, Kerala - 682001', 'cancelled'),
(7, 'Compost Mix', 6, 720, '123 Green Farm Road, Mysore, Karnataka - 570001', 'pending'),
(8, 'Bio Pesticide', 4, 680, '45 Rural Lane, Coimbatore, Tamil Nadu - 641001', 'dispatched'),
(9, 'Tractor Oil', 2, 950, '78 Harvest Ave, Pune, Maharashtra - 411001', 'pending'),
(10, 'Mulch Film Roll', 3, 1500, '12 Agri Street, Raipur, Chhattisgarh - 492001', 'delivered'),
(12, 'Weed Remover Tool', 1, 350, '234 Valley Road, Kochi, Kerala - 682001', 'pending');

INSERT INTO product_details (product_id, product_name, unit_of_measure, cost_per_unit)
VALUES
(1000, 'Organic Fertilizer', 'kg', 20.00),
(1001, 'Neem Pesticide', 'litre', 35.50),
(1002, 'Bio-Compost', 'kg', 15.00),
(1003, 'Drip Irrigation Kit', 'unit', 950.00),
(1004, 'Greenhouse Film', 'roll', 450.00),
(1005, 'Cocopeat Block', 'block', 30.00),
(1006, 'Seedling Tray', 'tray', 25.00),
(1007, 'Vermicompost', 'kg', 18.00),
(1008, 'Liquid Seaweed Extract', 'litre', 40.00),
(1009, 'Tractor Engine Oil', 'litre', 55.00);

INSERT INTO employee_details (full_name, email, designation)
VALUES
('Aarav Mehta', 'aarav.mehta@satyukt.com', 'Accountant'),
('Kavya Reddy', 'kavya.reddy@satyukt.com', 'Sales Manager'),
('Rohan Singh', 'rohan.singh@satyukt.com', 'Warehouse Supervisor'),
('Sneha Iyer', 'sneha.iyer@satyukt.com', 'Customer Support Executive'),
('Vikram Das', 'vikram.das@satyukt.com', 'Logistics Manager');

INSERT INTO production_details (product_id, product_name, quantity, status)
VALUES
(1000, 'Organic Fertilizer', 100, 'ongoing'),
(1001, 'Neem Pesticide', 80, 'ongoing'),
(1002, 'Bio-Compost', 150, 'ongoing'),
(1003, 'Drip Irrigation Kit', 30, 'ongoing'),
(1004, 'Greenhouse Film', 50, 'ongoing'),
(1005, 'Cocopeat Block', 120, 'ongoing'),
(1006, 'Seedling Tray', 70, 'ongoing'),
(1007, 'Vermicompost', 200, 'ongoing'),
(1008, 'Liquid Seaweed Extract', 60, 'ongoing'),
(1009, 'Tractor Engine Oil', 40, 'ongoing');

