create table customer(
     customer_id int primary key generated always as identity,
     customer_name varchar(50)
     );
create table bank_account(
     account_id int primary key generated always as identity,
     account_type varchar(50),
     balance float,
     customer_id int,
     constraint fk_customer_bank foreign key (customer_id) references customer(customer_id)
     );   
     
insert into customer  (customer_name) values ('ali');    

select * from bank_account where customer_id =11 and balance between 3000 and 700000;
select * from bank_account where customer_id =11 and account_id =10 ;
select * from bank_account 
update bank_account set balance = 999 where account_id =13 and customer_id =6 returning account_id,customer_id ;
delete from bank_account where customer_id =6 and account_id =13 returning account_id ;
delete from customer where customer_id = 6;

