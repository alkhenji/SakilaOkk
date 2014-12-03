use sakila;

# 1.b 119 is the 20% of the total number of disctinct customerID in the payment table (599).
# this view showes the table of the preferred customers.
-- create view PreferredStatus  as
-- select sum(amount) as Revenue, customer_id
-- from payment
-- group by customer_id
-- order by sum(amount) desc
-- limit 119;

create view allCustomers as
select sum(amount) as Revenue, customer_id
from payment
group by customer_id
order by sum(amount) desc;


#this view showes the table of the casual customers.
-- create view CasualStatus  as
-- select sum(amount) as Revenue, customer_id
-- from payment
-- group by customer_id
-- order by sum(amount) asc
-- limit 119;

# this procedure takes in the CustomerID and returns the status of the customer based on the Revenue.
delimiter //
create procedure CustomerStatus (in ID int)

begin
declare status varchar(45);
set status = ' ';
case

when ID in (select customer_id from PreferredStatus) then
set status = 'Preferred';

when ID in (select customer_id from CasualStatus) then
set status = 'Casual';

else
set status = 'Regular';

end case;
select status;
end//
Delimiter ;

#1.c
/*
in this procedure u just pass a Customer ID and it prints the lasr 5 movies that he has rented
*/
delimiter //
create procedure last5(in ID int)
begin
select film.title
from customer, rental, inventory, film
where rental.customer_id = customer.customer_id
and rental.inventory_id = inventory.inventory_id
and inventory.film_id = film.film_id
and customer.customer_id = ID
order by rental.rental_date desc
limit 5;
end //
delimiter ;

#balancePerMovie Function
delimiter //
create function balanceDuePerMovie ( ID int, invID int) returns decimal(5,2)
begin
declare x int;
declare y decimal (5,2);
declare z int;
declare due decimal (5,2);
select datediff(now(), rental_date) into x
from rental, film, inventory
where rental.inventory_id = inventory.inventory_id
and inventory.film_id = film.film_id
and rental.customer_id = ID
and rental.inventory_id = invID;

select rental_duration into z
from rental, film, inventory
where rental.inventory_id = inventory.inventory_id
and inventory.film_id = film.film_id
and rental.customer_id = ID
and inventory.inventory_id = invID;

select replacement_cost into y
from film, inventory
where inventory.film_id = film.film_id
and inventory.inventory_id = invID;

if y> z and x >= y then return y;
elseif y>z and y<=x then return x;
else return 0;
end if ;

end //

delimiter ;

drop function balanceDuePerMovie;
# total balance due function
delimiter //
CREATE function totalBalanceDue( ID INT) returns decimal (5,2)
BEGIN
declare result decimal (5,2);

declare counter int;
declare i int;
declare z int;
set i = 1;
set result = 0.0;
select balanceDue into result from customer where customer_id = ID;

CREATE TEMPORARY TABLE UnreturnedItems(n int auto_increment primary key, inventory_id int not null);

INSERT INTO UnreturnedItems(inventory_id)
select inventory.inventory_id
from rental, film, inventory
where rental.inventory_id = inventory.inventory_id
and inventory.film_id = film.film_id
and return_date is null
and rental.customer_id = ID;
select max(n) into counter from UnreturnedItems;


while i < counter+1 do
select inventory_id into z
from UnreturnedItems
where  n = i;
set result = result + (select balanceDuePerMovie(ID, z));

set i= i+1;
end while;
#select balanceDuePerMovie(ID, 3715);
drop temporary table if exists UnreturnedItems;
return result;
end//
delimiter ;

drop function totalBalanceDue;

#1.d
Alter table customer
add balanceDue decimal (5,2);
alter table customer
modify balanceDue decimal(5,2);

SET SQL_SAFE_UPDATES=0;

update customer
set balanceDue = 0 where store_id = 1 or store_id = 2;

delimiter //
create procedure RentDVDWithPayment(in invID int, in staffID int, ID int)
begin
declare res varchar(100);
declare paymentID int;
declare rentID int;
declare balance int;
declare pay decimal (10,2);

select max(payment_id) into paymentID from payment;
select MAx(rental_id) into rentID from payment;
set paymentID = PaymentID + 1;
select totalBalanceDue(ID) into balance;
select max(amount)into pay

from payment, inventory, rental
where inventory.inventory_id = rental.inventory_id
and rental.rental_id = payment.rental_id
and inventory.inventory_id =invID;

case

when balance >= 10 then
set res = 'Rent rejected, you have to pay your Balance Due first' ;
else
insert into rental (rental_date, inventory_id, customer_id, return_date, staff_id, last_update)
values ( now(), invID, ID, null, staffID, now());
select rental_id into rentID
from rental
where inventory_id = invID
and customer_id = ID
and staff_id = staffID;

insert into payment (payment_id, customer_id, staff_id, rental_id, amount)
values (paymentID, ID, staffID, rentID, pay);

set res = 'Rent Accepted';

end case;
select res;

end //
delimiter ;
drop procedure RentDVDWithPayment;
call RentDVDWithPayment( 18, 1, 15);
#1.e
delimiter //
create procedure RentDVDWithoutPayment(in invID int, in staffID int, ID int)
begin
declare res varchar(100);
declare paymentID int;
declare rentID int;
declare balance int;
declare pay decimal (10,2);

select max(payment_id) into paymentID from payment;
select max(rental_id) into rentID from payment;
set paymentID = PaymentID + 1;
set rentID = rentId +1;
select totalBalanceDue(ID) into balance;

select max(amount)into pay
from payment, inventory, rental
where inventory.inventory_id = rental.inventory_id
and rental.rental_id = payment.rental_id
and inventory.inventory_id =invID;

case

when balance >= 10 then
set res = 'Rent rejected, you have to pay your Balance Due first' ;
else
update customer
set balanceDue = balanceDue + pay where customer_id = ID;
set res = 'Rent Accepted';

insert into rental (rental_date, inventory_id, customer_id, return_date, staff_id, last_update)
values ( now(), invID, ID, null, staffID, now());


end case;
select res;

end //
delimiter ;
drop procedure if exists RentDVDWithoutPayment;
call RentDVDWithoutPayment( 18, 1, 1);

#1.f
/*
in this procedure u pass the id of the customer, and it showes the list of movies that has not
not been returned yet and it passed the returning date.

*/
delimiter //
create procedure OverDueMovies (in ID int)

begin

select film.title, inventory.inventory_id, inventory.store_id from rental, film, inventory
where rental.inventory_id = inventory.inventory_id
and inventory.film_id = film.film_id
and return_date is null
and datediff(now(), rental_date) > film.rental_duration
and rental.customer_id =ID;

end //
delimiter ;

delimiter //
create procedure NotOverDueMovies (in ID int)

begin

select film.title, inventory.inventory_id, inventory.store_id from rental, film, inventory
where rental.inventory_id = inventory.inventory_id
and inventory.film_id = film.film_id
and return_date is null
and datediff(now(), rental_date) < film.rental_duration
and rental.customer_id =ID;

end //
delimiter ;



#1.g
delimiter //
create procedure returnDVD(in ID int , in filmID int)
begin
declare invID int;
declare balance decimal (5,2);
declare amount decimal (5,2);
select inventory.inventory_id into invID
from rental, film, inventory
where rental.inventory_id = inventory.inventory_id
and inventory.film_id = film.film_id
and return_date is null
and datediff(now(), rental_date) > film.rental_duration
and rental.customer_id =ID
and inventory.film_id = filmID;

set amount = balanceDuePerMovie (ID, invID);
select balanceDue into balance from customer where customer_id = ID;

update rental
set return_date = now() where customer_id = ID and inventory_id = invID;

update customer
set balanceDue = (amount+ balance)  where customer_id = ID;






end //
delimiter ;
drop procedure returnDVD;
call returnDVD(15, 526);
#1.h
select inventory.film_id
from rental, film, inventory
where rental.inventory_id = inventory.inventory_id
and inventory.film_id = film.film_id
and return_date is null
and datediff(now(), rental_date) > film.rental_duration
and rental.customer_id = 9;

call returnDVD(9, 219);
select totalBalanceDue (9);

#1.i

delimiter //
create procedure payBalanceDue (in ID int)
begin
declare x int;
declare res varchar(100);
declare staffID int;
declare rentalID int;
declare pay decimal (5,2);
declare paymentID int ;
select balanceDue into pay from customer where customer_id =ID;


select  count(film.title) into x
from rental, film, inventory
where rental.inventory_id = inventory.inventory_id
and inventory.film_id = film.film_id
and return_date is null
and rental.customer_id =ID;

select  payment.staff_id into staffID
from rental, film, inventory, payment
where rental.inventory_id = inventory.inventory_id
and rental.rental_id = payment.rental_id
and inventory.film_id = film.film_id
and rental.customer_id =ID
order by rental_date desc
limit 1;

select max(payment_id)into paymentID from payment;
set paymentID = paymentID + 1;

select rental_id into rentalID  from rental
where customer_id =ID
order by rental_date desc
limit 1 ;

case
when x > 0 then
set res = 'Please return the Movies that you have rented first';
else
insert into payment (payment_id, customer_id, staff_id, rental_id, amount)
values (paymentID, ID, staffID, rentalID, pay);

update customer
set balanceDue = 0 where customer_id = ID;
set res = 'You have successfully paid your balance';
end case;
select res;
end //
delimiter ;


d
create function balanceDueFinally(id int) returns decimal (5,2)
begin
declare x decimal (5,2);
declare y decimal (5,2);
declare res decimal(5,2);

select sum(rental_rate +payDiff(customer.customer_id, inventory.inventory_id)) into x
from film, rental, inventory, customer
where customer.customer_id = rental.customer_id
and rental.inventory_id = inventory.inventory_id
and inventory.film_id = film.film_id
and customer.customer_id =id;
select sum(amount)into y from payment where customer_id = id;

set res = x-y;
return res;
end //
delimiter ;

select balanceDueFinally(1);


call RentDVDWithoutPayment( 18, 1, 1);



delimiter //
create function payDiff( id int, invID int) returns decimal (5,2)
begin
declare x int ;
declare y int;
declare z decimal(5,2);
declare res decimal(5,2);

select datediff(return_date, rental_date) into x from rental, inventory, film, customer
where customer.customer_id = rental.customer_id
and rental.inventory_id = inventory.inventory_id
and inventory.film_id = film.film_id
and inventory.inventory_id= invID
and customer.customer_id = id;

select replacement_cost into z
from inventory, film
where inventory.film_id = film.film_id
and inventory_id = invID;

select rental_duration into y from inventory, film
where inventory.film_id = film.film_id
and inventory. inventory_id = invID;

case
when x>y and x > z then
set res =z;
when x>y and X<z then set res = x-y;
else  
set res = 0.00;
end case;
return res;
end //
delimiter ;




/*Movies*/

/*a
Enter a movie ID and it will give you the Movie information(title, description, language, actors, length, replacement cost, rating, special features) */
DELIMITER //
CREATE PROCEDURE Movieinfo(IN ID INT)
BEGIN
SELECT film.title, film.description, language.name, actor.first_name, actor.last_name, film.length, film.replacement_cost, film.rating, film.special_features
FROM film, language, film_actor, actor
WHERE film.language_id=language.language_id
AND film.film_id=film_actor.film_id
AND film_actor.actor_id=actor.actor_id
AND film.film_id=ID;
END //
DELIMITER ;

/*b
Enter a movie ID and it will give you how many each store has from this movie*/
DELIMITER //
CREATE PROCEDURE Instore(IN ID INT)
BEGIN
SELECT film.title, COUNT(film.film_id) AS 'How_many_the_store_has', store.store_id
FROM film, store, inventory
WHERE film.film_id=inventory.film_id
AND inventory.store_id=store.store_id
GROUP BY film.title, store.store_id;
END //
DELIMITER ;

/*Enter a movie ID and it will give you how many each store has from this movie*/
DELIMITER $$
CREATE FUNCTION Instore(ID SMALLINT) RETURNS INT
BEGIN
    DECLARE Amountavailable INT;
    SELECT COUNT(film.film_id) INTO Amountavailable
    FROM film, store, inventory
    WHERE film.film_id=inventory.film_id
    AND inventory.store_id=store.store_id
    AND film.film_id=ID
    GROUP BY film.title;
    RETURN Amountavailable;
END $$
Delimiter;

/*Enter a movie ID and it will give you how many of this movie are currently rented out or not in store*/
DELIMITER //
CREATE PROCEDURE Rentedout(IN ID INT)
BEGIN
SELECT film.title, COUNT(rental.rental_id) AS 'Amount rented out currently', film.film_id
FROM customer, film, payment, rental, inventory
WHERE return_date IS null
AND customer.customer_id=rental.customer_id
AND film.film_id=inventory.film_id
AND payment.rental_id=rental.rental_id
AND inventory.inventory_id=rental.inventory_id
GROUP BY film.film_id;
END //
DELIMITER ;

/*Enter a movie ID and it will give you how many of this movie are currently rented out or not in store*/
DELIMITER $$
CREATE FUNCTION Rentedout(ID SMALLINT) RETURNS INT
BEGIN
    DECLARE Amountavailable INT;
    SELECT COUNT(rental.rental_id) INTO Amountavailable
    FROM customer, film, payment, rental, inventory
    WHERE return_date IS null
    AND customer.customer_id=rental.customer_id
    AND film.film_id=inventory.film_id
    AND payment.rental_id=rental.rental_id
    AND inventory.inventory_id=rental.inventory_id
    and film.film_id = ID
    GROUP BY film.film_id;
    RETURN Amountavailable;
END $$
Delimiter;

/*Enter a movie ID and it will give you how many of this movie are currently available or in store*/
DELIMITER //
CREATE PROCEDURE Currentlyavailable(IN ID INT)
BEGIN
DECLARE res INT;
SET res = (SELECT Instore(ID)) - (SELECT Rentedout(ID));
SELECT res;
END //
DELIMITER ;

/*It will take a movie id and it will find how many are in store, 
how many are rented out, and subtract them from each other 
which will be the amount currently available*/
DELIMITER //
CREATE PROCEDURE Alltogether(IN ID INT)
BEGIN
DECLARE x INT;
DECLARE y INT;
DECLARE res INT;
SET x = (SELECT Instore(ID));
SET y = (SELECT Rentedout(ID));
SET res = (SELECT Instore(ID)) - (SELECT Rentedout(ID));
SELECT x,y,res;
END //
DELIMITER ;

/*c
This view will give you all movies ordered by rental income*/
create view allMovies as
select sum(amount) as sum, film.film_id, film.title from rental, film, inventory, payment
where film.film_id = inventory.film_id
and inventory.inventory_id = rental.inventory_id
and rental.rental_id = payment.rental_id
group by film.film_id
order by sum desc;

/*this view will give us the top ten movies based on rental income*/
-- create view topTen as
-- select sum(amount) as sum, film.film_id, film.title from rental, film, inventory, payment
-- where film.film_id = inventory.film_id
-- and inventory.inventory_id = rental.inventory_id
-- and rental.rental_id = payment.rental_id
-- group by film.film_id
-- order by sum desc
-- limit 10 ;

/*This view will give you the hot movies */
-- create view hotMovies as
-- select sum(amount) as sum, film.film_id, film.title from rental, film, inventory, payment
-- where film.film_id = inventory.film_id
-- and inventory.inventory_id = rental.inventory_id
-- and rental.rental_id = payment.rental_id
-- group by film.film_id
-- order by sum desc
-- limit 200 ;

/*This view will give you the Dud movies*/
-- create view dudMovies as
-- select sum(amount) as sum, film.film_id, film.title from rental, film, inventory, payment
-- where film.film_id = inventory.film_id
-- and inventory.inventory_id = rental.inventory_id
-- and rental.rental_id = payment.rental_id
-- group by film.film_id
-- order by sum asc
-- limit 200;

Delimiter //
create procedure MovieStatus2 (in ID int)
begin
declare res varchar(45);
 case
when ID in (select film_id from topTen)
then set res = 'Top ten';
when ID in (select film_id from hotMovies)
then set res = 'Hot';
when ID in (select film_id from dudMovies)
then set res = 'Dud';
else
set res = 'regular';
end case;
select res;
end//
delimiter ;

/*This will give you the list of all the movie ID’s and the rental income of each one*/
DELIMITER //
CREATE PROCEDURE Allmovies()
BEGIN
    SELECT (payment.amount * count(payment.customer_id)) AS Rentalincome, film.film_id AS id
    FROM customer, film, payment, rental, inventory
    WHERE customer.customer_id=rental.customer_id
    AND film.film_id=inventory.film_id
    AND payment.rental_id=rental.rental_id
    AND inventory.inventory_id=rental.inventory_id
    GROUP BY film.film_id
    ORDER BY Rentalincome DESC;
END //
DELIMITER ;

/*Enter a movie ID and it will tell you the status of the movie: top ten or hot or dud or regular which is anything else*/
DELIMITER //
CREATE PROCEDURE Moviestatus(IN ID SMALLINT, OUT status VARCHAR(20))
BEGIN
    IF ID IN (SELECT id FROM Toptenmovies) THEN SET status = 'Top Ten';
    ELSEIF ID IN (SELECT id FROM Hotmovies) THEN SET status = 'Hot';
    ELSEIF ID IN (SELECT id FROM Dud) THEN SET status = 'Dud';
    ELSEIF ID IN (SELECT id FROM Regular) THEN SET status = 'Regular';
    ELSE SET status= 'Wrong';
    END IF;
END //
DELIMITER ;

/*Enter a movie ID and it will tell you the status of the movie: top ten or hot or dud or regular which is anything else*/
DELIMITER $$
CREATE FUNCTION Moviestatus(ID SMALLINT) RETURNS VARCHAR(20)
BEGIN
    DECLARE statuss varchar(20);
    IF ID IN (SELECT id FROM Toptenmovies) THEN
        SET statuss = 'Top Ten';
    ELSEIF ID IN (SELECT id FROM Hotmovies) THEN
        SET statuss = 'Hot';
    ELSEIF ID IN (SELECT id FROM Dud) THEN
        SET statuss = 'Dud';
    Else 
        SET statuss = 'Regular';
    END IF;
RETURN (statuss);
END $$
Delimiter;

/*d
Enter a movie ID and it will tell you last 5 “rentals” of the movie,
including the name of the customer who rented it out, the rental date,
the return date (if any), and the store from which it was rented out.*/
DELIMITER //
CREATE PROCEDURE last5rentals(IN ID INT)
BEGIN
SELECT rental.rental_id, film.title, customer.first_name, customer.last_name, rental.rental_date,
rental.return_date, store.store_id
FROM customer, rental, inventory, film, store
WHERE rental.customer_id = customer.customer_id
AND rental.inventory_id = inventory.inventory_id
AND inventory.film_id = film.film_id
AND inventory.store_id = store.store_id
AND film.film_id=ID
ORDER BY rental.rental_date DESC
LIMIT 5;
END //
DELIMITER ;


