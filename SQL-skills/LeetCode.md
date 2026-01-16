## 1 (1757. Recyclable and Low Fat Products)
Write a solution to find the ids of products that are both low fat and recyclable.
Return the result table in any order.
```sql
SELECT
    product_id
FROM
    Products
WHERE low_fats = 'Y' AND recyclable = 'Y'
```
## 2 (584. Find Customer Referee)
Find the names of the customer that are either:
referred by any customer with id != 2.
not referred by any customer.
Return the result table in any order.
```sql
SELECT
    name
FROM
    Customer
WHERE referee_id != 2 OR referee_id IS NULL
```
## 3 (595. Big Countries)
A country is big if:
it has an area of at least three million (i.e., 3000000 km2), or
it has a population of at least twenty-five million (i.e., 25000000).
Write a solution to find the name, population, and area of the big countries.
Return the result table in any order.
```sql
SELECT
    name,
    population,
    `area`
FROM
    World
WHERE `area` >= 3000000 OR population >= 25000000
```
## 4 (1148. Article Views I)
Write a solution to find all the authors that viewed at least one of their own articles.
Return the result table sorted by id in ascending order.
```sql
SELECT DISTINCT
    author_id AS id
FROM
    Views
WHERE author_id = viewer_id
ORDER BY author_id
```
## 5 (1683. Invalid Tweets)
Write a solution to find the IDs of the invalid tweets. The tweet is invalid if the number of characters used in the content of the tweet is strictly greater than 15.
Return the result table in any order.
```sql
SELECT
    tweet_id
FROM
    Tweets
WHERE LENGTH(content) > 15
```
## 6 (1378. Replace Employee ID With The Unique Identifier)
Write a solution to show the unique ID of each user, If a user does not have a unique ID replace just show null.
Return the result table in any order.
```sql
SELECT
    unique_id,
    name
FROM Employees LEFT JOIN EmployeeUNI USING(id)
```
## 7 (1068. Product Sales Analysis I)
Write a solution to report the product_name, year, and price for each sale_id in the Sales table.
Return the resulting table in any order.
```sql
SELECT
    product_name,
    year,
    price
FROM Sales INNER JOIN Product USING(product_id)
```
## 8 (1581. Customer Who Visited but Did Not Make Any Transactions)
Write a solution to find the IDs of the users who visited without making any transactions and the number of times they made these types of visits.
Return the result table sorted in any order.
```sql
SELECT
    customer_id,
    COUNT(*) AS count_no_trans
FROM Visits LEFT JOIN Transactions USING (visit_id)
WHERE transaction_id IS NULL
GROUP BY customer_id
```
## 9 (197. Rising Temperature)
Write a solution to find all dates' id with higher temperatures compared to its previous dates (yesterday).
Return the result table in any order.
```sql
SELECT 
    w2.id
FROM 
    weather w1, weather w2
WHERE
    w1.temperature < w2.temperature
and ADDDATE(W1.RecordDate, INTERVAL 1 DAY) = W2.RecordDate
```
## 10 (1661. Average Time of Process per Machine)
There is a factory website that has several machines each running the same number of processes. Write a solution to find the average time each machine takes to complete a process.
The time to complete a process is the 'end' timestamp minus the 'start' timestamp. The average time is calculated by the total time to complete every process on the machine divided by the number of processes that were run.
The resulting table should have the machine_id along with the average time as processing_time, which should be rounded to 3 decimal places.
Return the result table in any order.
```sql
WITH CTE AS (SELECT
    machine_id,
    activity_type,
    ROUND(SUM(timestamp), 3) AS time_startend,
    COUNT(*) as counter
FROM
    Activity
GROUP BY machine_id, activity_type)

SELECT
    machine_id,
    ROUND((MAX(time_startend) - MIN(time_startend)) / counter, 3) AS processing_time
FROM CTE
GROUP BY machine_id
```
## 11 (577. Employee Bonus)
Write a solution to report the name and bonus amount of each employee who satisfies either of the following:
The employee has a bonus less than 1000.
The employee did not get any bonus.
Return the result table in any order.
```sql
SELECT
    name,
    bonus
FROM
    Employee LEFT JOIN Bonus USING (empId)
WHERE bonus < 1000 OR bonus IS NULL
```
## 12 (1280. Students and Examinations)
Write a solution to find the number of times each student attended each exam.
Return the result table ordered by student_id and subject_name.
```sql
WITH CTE_1 AS (SELECT
    student_id,
    student_name,
    subject_name,
    0 AS attended_exams
FROM Students 
    CROSS JOIN Subjects),

CTE_2 AS (SELECT
    Examinations.student_id,
    student_name,
    subject_name,
    COUNT(*) AS attended_exams
FROM
    Examinations 
    INNER JOIN Students USING (student_id)
GROUP BY student_id, subject_name),

CTE_3 AS (SELECT
    CTE_1.student_id,
    CTE_1.student_name,
    CTE_1.subject_name,
    CTE_1.attended_exams + CTE_2.attended_exams AS attended_exams
FROM
    CTE_1 LEFT JOIN CTE_2 ON
    CTE_1.student_id = CTE_2.student_id AND
    CTE_1.subject_name = CTE_2.subject_name)

SELECT
    student_id,
    student_name,
    subject_name,
    IFNULL(attended_exams, 0) AS attended_exams
FROM CTE_3
ORDER BY 1, 3
```
## 13 (570. Managers with at Least 5 Direct Reports)
Write a solution to find managers with at least five direct reports.
Return the result table in any order.
```sql
WITH CTE AS (SELECT
    managerId AS id
FROM
    Employee
GROUP BY managerID
HAVING COUNT(*) >= 5)

SELECT
    name
FROM
    CTE INNER JOIN Employee USING(id)
```
## 14 (1934. Confirmation Rate)
The confirmation rate of a user is the number of 'confirmed' messages divided by the total number of requested confirmation messages. The confirmation rate of a user that did not request any confirmation messages is 0. Round the confirmation rate to two decimal places.
Write a solution to find the confirmation rate of each user.
Return the result table in any order.
```sql
WITH CTE_confirmed AS (SELECT
    user_id,
    COUNT(*) AS confirmed
FROM
    Confirmations
WHERE action = 'confirmed'
GROUP BY user_id),

all_confirmed AS(
    SELECT
        Signups.user_id,
        IFNULL(confirmed, 0) as confirmed
    FROM
        Signups LEFT JOIN CTE_confirmed USING (user_id)),

CTE_actions AS (SELECT
    user_id,
    COUNT(*) AS actions
FROM
    Confirmations
GROUP BY user_id),

all_actions AS(
    SELECT
        Signups.user_id,
        IFNULL(actions, 0) as actions
    FROM
        Signups LEFT JOIN CTE_actions USING (user_id))



SELECT 
    all_actions.user_id,
    IFNULL(ROUND(confirmed/actions, 2), 0) AS confirmation_rate
FROM
    all_actions INNER JOIN all_confirmed USING (user_id)
```
## 15 (620. Not Boring Movies)
Write a solution to report the movies with an odd-numbered ID and a description that is not "boring".
Return the result table ordered by rating in descending order.
```sql
SELECT
    id,
    movie,
    description,
    rating
FROM Cinema
WHERE description != 'boring' AND id % 2 != 0
ORDER BY rating DESC
```
## 16 (1251. Average Selling Price)
Write a solution to find the average selling price for each product. average_price should be rounded to 2 decimal places. If a product does not have any sold units, its average selling price is assumed to be 0.
Return the result table in any order.
```sql
SELECT
    Prices.product_id,
    IFNULL(ROUND(SUM(units*price) / SUM(units), 2), 0) AS average_price
FROM
    Prices LEFT JOIN UnitsSold
    ON UnitsSold.purchase_date >= Prices.start_date
    AND UnitsSold.purchase_date <= Prices.end_date
    AND UnitsSold.product_id = Prices.product_id
GROUP BY product_id
ORDER BY Prices.product_id
```
## 17 (1075. Project Employees I)
Write an SQL query that reports the average experience years of all the employees for each project, rounded to 2 digits.
Return the result table in any order.
```sql
SELECT
    project_id,
    ROUND(SUM(experience_years) / COUNT(*), 2) AS average_years
FROM
    Project INNER JOIN Employee USING (employee_id)
GROUP BY project_id
```
## 18 (1633. Percentage of Users Attended a Contest)
Write a solution to find the percentage of the users registered in each contest rounded to two decimals.
Return the result table ordered by percentage in descending order. In case of a tie, order it by contest_id in ascending order.
```sql
SELECT
    contest_id,
    ROUND(100 * COUNT(*) / (SELECT COUNT(user_id) FROM Users), 2) AS percentage
FROM Register
GROUP BY contest_id
ORDER BY 2 DESC, contest_id
```
## 19 (1211. Queries Quality and Percentage)
We define query quality as:
The average of the ratio between query rating and its position.
We also define poor query percentage as:
The percentage of all queries with rating less than 3.
Write a solution to find each query_name, the quality and poor_query_percentage.
Both quality and poor_query_percentage should be rounded to 2 decimal places.
Return the result table in any order.
```sql
SELECT
    query_name,
    ROUND(AVG(rating/position), 2) AS quality,
    ROUND(100*(SUM(CASE WHEN rating < 3 THEN 1 ELSE 0 END) / COUNT(*)), 2) AS poor_query_percentage
FROM Queries
GROUP BY query_name
```
## 20 (1193. Monthly Transactions I)
Write an SQL query to find for each month and country, the number of transactions and their total amount, the number of approved transactions and their total amount.
Return the result table in any order.
```sql
SELECT
    DATE_FORMAT(trans_date, '%Y-%m') AS month,
    country,
    COUNT(*) AS trans_count,
    SUM(CASE WHEN state = 'approved' THEN 1 ELSE 0 END) AS approved_count,
    SUM(amount) AS trans_total_amount,
    SUM(CASE WHEN state = 'approved' THEN amount ELSE 0 END) AS approved_total_amount
FROM Transactions
GROUP BY DATE_FORMAT(trans_date, '%Y-%m'), country
```
## 21 (1174. Immediate Food Delivery II)
If the customer's preferred delivery date is the same as the order date, then the order is called immediate; otherwise, it is called scheduled.
The first order of a customer is the order with the earliest order date that the customer made. It is guaranteed that a customer has precisely one first order.
Write a solution to find the percentage of immediate orders in the first orders of all customers, rounded to 2 decimal places.
```sql
SELECT
    ROUND(AVG(100*(order_date = customer_pref_delivery_date)), 2) as immediate_percentage
FROM
    Delivery
WHERE
    (customer_id, order_date) in
    (
        SELECT
            customer_id,
            MIN(order_date)
        FROM Delivery
        GROUP BY customer_id
    )
```
## 22 (550. Game Play Analysis IV)
Write a solution to report the fraction of players that logged in again on the day after the day they first logged in, rounded to 2 decimal places. In other words, you need to determine the number of players who logged in on the day immediately following their initial login, and divide it by the number of total players.
```sql
WITH CTE AS (SELECT
    player_id
FROM
    Activity
WHERE   (player_id, event_date) IN 
    (SELECT
    player_id,
    DATE_ADD(MIN(event_date), INTERVAL 1 DAY) AS prop_date
FROM
    Activity
GROUP BY 
    player_id)),

CTE2 AS (SELECT DISTINCT
    Activity.player_id AS p_A,
    CASE WHEN CTE.player_id IS NULL THEN 0 ELSE 1 END AS p_cte
FROM
    CTE RIGHT JOIN Activity USING (player_id))


SELECT
    ROUND(SUM(p_cte) / COUNT(p_cte), 2) AS fraction
FROM CTE2
```
## 23 (2356. Number of Unique Subjects Taught by Each Teacher)
Write a solution to calculate the number of unique subjects each teacher teaches in the university.
Return the result table in any order.
```sql
SELECT
    teacher_id,
    COUNT(DISTINCT subject_id) AS cnt
FROM 
    Teacher
GROUP BY
    teacher_id
```
## 24 (1141. User Activity for the Past 30 Days I)
Write a solution to find the daily active user count for a period of 30 days ending 2019-07-27 inclusively. A user was active on someday if they made at least one activity on that day.
Return the result table in any order.
The result format is in the following example.
Note: Any activity from ('open_session', 'end_session', 'scroll_down', 'send_message') will be considered valid activity for a user to be considered active on a day.
```sql
SELECT
    activity_date AS day,
    COUNT(DISTINCT user_id) AS active_users
FROM 
    Activity
WHERE activity_date > DATE_SUB('2019-07-27', INTERVAL 30 DAY) AND activity_date <= DATE('2019-07-27')
GROUP BY
    activity_date
```
## 25 (1070. Product Sales Analysis III)
Write a solution to find all sales that occurred in the first year each product was sold.
For each product_id, identify the earliest year it appears in the Sales table.
Return all sales entries for that product in that year.
Return a table with the following columns: product_id, first_year, quantity, and price.
Return the result in any order.
```sql
SELECT
    product_id,
    year AS first_year,
    quantity,
    price
FROM
    Sales
WHERE (product_id, year) IN
    (SELECT
        product_id,
        MIN(year) AS first_year
    FROM
        Sales
    GROUP BY product_id)
```
## 26 (596. Classes With at Least 5 Students)
Write a solution to find all the classes that have at least five students.
Return the result table in any order.
```sql
SELECT
    DISTINCT class
FROM
    Courses
WHERE
    class IN 
    (SELECT
        class
    FROM
        Courses
    GROUP BY class
    HAVING COUNT(DISTINCT student) >= 5)
```
## 27 (1729. Find Followers Count)
Write a solution that will, for each user, return the number of followers.
Return the result table ordered by user_id in ascending order.
```sql
SELECT
    user_id,
    COUNT(*) AS followers_count
FROM
    Followers
GROUP BY
    user_id
ORDER BY user_id
```
## 28 (619. Biggest Single Number)
A single number is a number that appeared only once in the MyNumbers table.
Find the largest single number. If there is no single number, report null.
```sql
SELECT
    MAX(num) AS num
FROM
    MyNumbers
WHERE
    num IN
    (SELECT
        num
    FROM
        MyNumbers
    GROUP BY
        num
    HAVING
        COUNT(*) = 1)
```
## 29 (1045. Customers Who Bought All Products)
Write a solution to report the customer ids from the Customer table that bought all the products in the Product table.
Return the result table in any order.
```sql
SELECT
    customer_id
FROM
    Customer
GROUP BY customer_id
HAVING COUNT(DISTINCT product_key) = (SELECT COUNT(product_key) FROM Product)
```
## 30 (1731. The Number of Employees Which Report to Each Employee)
For this problem, we will consider a manager an employee who has at least 1 other employee reporting to them.
Write a solution to report the ids and the names of all managers, the number of employees who report directly to them, and the average age of the reports rounded to the nearest integer.
Return the result table ordered by employee_id.
```sql
WITH CTE AS (SELECT
    reports_to AS employee_id,
    COUNT(*) AS reports_count,
    ROUND(AVG(age)) AS average_age
FROM Employees 
GROUP BY reports_to
HAVING reports_to IS NOT NULL)

SELECT
    employee_id,
    name,
    reports_count,
    average_age
FROM CTE INNER JOIN Employees USING (employee_id)
ORDER BY employee_id
```
## 31 (1789. Primary Department for Each Employee)
Employees can belong to multiple departments. When the employee joins other departments, they need to decide which department is their primary department. Note that when an employee belongs to only one department, their primary column is 'N'.
Write a solution to report all the employees with their primary department. For employees who belong to one department, report their only department.
Return the result table in any order.
```sql
SELECT
    employee_id,
    department_id
FROM
    Employee
WHERE   
    primary_flag = 'Y'

UNION ALL

SELECT
    employee_id,
    department_id
FROM
    Employee
GROUP BY employee_id
HAVING COUNT(*) = 1
```
## 32 (610. Triangle Judgement)
Report for every three line segments whether they can form a triangle.
Return the result table in any order.
```sql
SELECT
    *,
    IF(x+y>z AND x+z>y AND y+z>x, 'Yes', 'No') AS triangle
FROM
    Triangle
```
## 33 (180. Consecutive Numbers)
Find all numbers that appear at least three times consecutively.
Return the result table in any order.
```sql
WITH CTE AS (SELECT
    id,
    num AS num_cte
FROM
    Logs),

CTE_CTE AS (SELECT
    id,
    num AS num_cte_cte
FROM
    Logs)

SELECT DISTINCT
    num AS ConsecutiveNums
FROM
    Logs 
    LEFT JOIN CTE ON Logs.id = CTE.id + 1
    LEFT JOIN CTE_CTE ON Logs.id = CTE_CTE.id + 2
WHERE num = num_cte AND num_cte = num_cte_cte
```
## 34 (1164. Product Price at a Given Date)
Initially, all products have price 10.
Write a solution to find the prices of all products on the date 2019-08-16.
Return the result table in any order.
```sql
WITH CTE AS (
    SELECT DISTINCT
        product_id
    FROM
        Products),

ANSWER AS (SELECT
    product_id,
    new_price
FROM
    Products
WHERE (product_id, change_date) IN 
    (SELECT
        product_id,
        MAX(change_date) AS last_change_date
    FROM
        Products
    WHERE change_date <= '2019-08-16'
    GROUP BY product_id))

SELECT
    product_id,
    IFNULL(new_price, 10) AS price
FROM 
    ANSWER RIGHT JOIN CTE USING (product_id)
```
## 35 (1204. Last Person to Fit in the Bus)
There is a queue of people waiting to board a bus. However, the bus has a weight limit of 1000 kilograms, so there may be some people who cannot board.
Write a solution to find the person_name of the last person that can fit on the bus without exceeding the weight limit. The test cases are generated such that the first person does not exceed the weight limit.
Note that only one person can board the bus at any given turn.
```sql
WITH CTE AS (SELECT
    turn,
    person_name,
    weight,
    SUM(weight) OVER (ORDER BY turn
                      ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS cum_weight
FROM
    Queue)

SELECT
    person_name
FROM
    CTE
WHERE cum_weight <= 1000
ORDER BY (cum_weight) DESC
LIMIT 1
```
## 36 (1907. Count Salary Categories)
Write a solution to calculate the number of bank accounts for each salary category. The salary categories are:
"Low Salary": All the salaries strictly less than $20000.
"Average Salary": All the salaries in the inclusive range [$20000, $50000].
"High Salary": All the salaries strictly greater than $50000.
The result table must contain all three categories. If there are no accounts in a category, return 0.
Return the result table in any order.
```sql
SELECT
    'Low Salary' AS category,
    COUNT(*) AS accounts_count
FROM
    Accounts
WHERE income < 20000

UNION ALL

SELECT
    'Average Salary' AS category,
    COUNT(*) AS accounts_count
FROM
    Accounts
WHERE income >= 20000 AND income <= 50000

UNION ALL

SELECT
    'High Salary' AS category,
    COUNT(*) AS accounts_count
FROM
    Accounts
WHERE income > 50000
```
## 37 (1978. Employees Whose Manager Left the Company)
Find the IDs of the employees whose salary is strictly less than $30000 and whose manager left the company. When a manager leaves the company, their information is deleted from the Employees table, but the reports still have their manager_id set to the manager that left.
Return the result table ordered by employee_id.
```sql
SELECT
    employee_id
FROM
    Employees
WHERE
    salary < 30000 AND manager_id IS NOT NULL AND manager_id NOT IN (SELECT DISTINCT employee_id FROM Employees)
ORDER BY
    employee_id
```
## 38 (626. Exchange Seats)
Write a solution to swap the seat id of every two consecutive students. If the number of students is odd, the id of the last student is not swapped.
Return the result table ordered by id in ascending order.
```sql
WITH CTE AS (SELECT
    id - 1 AS id,
    student
FROM
    Seat
WHERE id % 2 = 0

UNION ALL

SELECT
    CASE 
        WHEN id NOT IN (SELECT MAX(id) FROM Seat) THEN id + 1
        ELSE id
    END AS id,
        student
    FROM
        Seat
    WHERE id % 2 = 1)

SELECT
    *
FROM
    CTE
ORDER BY id
```
## 39 (1341. Movie Rating)
Write a solution to:
Find the name of the user who has rated the greatest number of movies. In case of a tie, return the lexicographically smaller user name.
Find the movie name with the highest average rating in February 2020. In case of a tie, return the lexicographically smaller movie name.
```sql
(SELECT
    name AS results
FROM
    MovieRating INNER JOIN Users USING (user_id)
GROUP BY MovieRating.user_id
ORDER BY COUNT(*) DESC, name
LIMIT 1)

UNION ALL

(SELECT
    title AS results
FROM
    MovieRating INNER JOIN Movies USING (movie_id)
WHERE MONTH(created_at) = 2 AND YEAR(created_at) = 2020
GROUP BY movie_id
ORDER BY AVG(rating) DESC, title
LIMIT 1)
```
## 40 (1321. Restaurant Growth)
You are the restaurant owner and you want to analyze a possible expansion (there will be at least one customer every day).
Compute the moving average of how much the customer paid in a seven days window (i.e., current day + 6 days before). average_amount should be rounded to two decimal places.
Return the result table ordered by visited_on in ascending order.
```sql
WITH CTE AS (SELECT
    visited_on,
    SUM(amount) AS amount
FROM
    Customer
GROUP BY visited_on)

SELECT
    visited_on,
    SUM(amount) OVER w AS amount,
    ROUND(AVG(amount) OVER w, 2) AS average_amount
FROM CTE
WINDOW w AS (ORDER BY visited_on
                      RANGE BETWEEN INTERVAL 6 DAY PRECEDING AND CURRENT ROW)
LIMIT 100 OFFSET 6
```
## 41 (602. Friend Requests II: Who Has the Most Friends)
Write a solution to find the people who have the most friends and the most friends number.
The test cases are generated so that only one person has the most friends.
```sql
WITH Clients AS (SELECT DISTINCT
    requester_id AS id,
    0 AS num
FROM
    RequestAccepted

UNION

SELECT DISTINCT
    accepter_id AS id,
    0 AS num
FROM
    RequestAccepted),

Req_Clients AS (SELECT
    requester_id AS id,
    COUNT(*) AS num
FROM
    RequestAccepted
GROUP BY requester_id),

Acc_Clients AS (SELECT
    accepter_id AS id,
    COUNT(*) AS num
FROM
    RequestAccepted
GROUP BY accepter_id)

SELECT 
    Clients.id,
    IFNULL(Req_Clients.num, 0) +  IFNULL(Acc_Clients.num, 0) + Clients.num AS num
FROM
    Clients 
    LEFT JOIN Req_CLients USING (id)
    LEFT JOIN Acc_Clients USING (id)
ORDER BY 2 DESC
LIMIT 1
```
## 42 (585. Investments in 2016)
Write a solution to report the sum of all total investment values in 2016 tiv_2016, for all policyholders who:
have the same tiv_2015 value as one or more other policyholders, and
are not located in the same city as any other policyholder (i.e., the (lat, lon) attribute pairs must be unique).
Round tiv_2016 to two decimal places.
```sql
SELECT
    ROUND(SUM(tiv_2016), 2) AS tiv_2016
FROM
    Insurance
WHERE tiv_2015 IN 
    (SELECT
        tiv_2015
    FROM
        Insurance
    GROUP BY tiv_2015
    HAVING COUNT(*) > 1
)
AND (lat, lon) IN
    (SELECT
        lat, lon
    FROM
        Insurance
    GROUP BY lat, lon
    HAVING COUNT(*) = 1)
```
## 43 (185. Department Top Three Salaries)
A company's executives are interested in seeing who earns the most money in each of the company's departments. A high earner in a department is an employee who has a salary in the top three unique salaries for that department.
Write a solution to find the employees who are high earners in each of the departments.
Return the result table in any order.
```sql
WITH CTE AS (SELECT
    Department.name AS Department,
    Employee.name AS Employee,
    salary AS Salary,
    DENSE_RANK() OVER w AS rating
FROM
    Employee INNER JOIN Department ON Employee.departmentId = Department.id
WINDOW w AS (PARTITION BY Department.id
             ORDER BY Salary DESC))

SELECT
    Department, 
    Employee,
    Salary
FROM
    CTE
WHERE rating <= 3
```
## 44 (1667. Fix Names in a Table)
Write a solution to fix the names so that only the first character is uppercase and the rest are lowercase.
Return the result table ordered by user_id.
```sql
SELECT
    user_id,
    CONCAT(LEFT(UPPER(name), 1), SUBSTRING(LOWER(name), 2)) AS name
FROM
    Users
ORDER BY user_id
```
## 45 (1527. Patients With a Condition)
Write a solution to find the patient_id, patient_name, and conditions of the patients who have Type I Diabetes. Type I Diabetes always starts with DIAB1 prefix.
Return the result table in any order.
```sql
SELECT
    patient_id,
    patient_name,
    conditions
FROM
    Patients
WHERE conditions LIKE 'DIAB1%' OR conditions LIKE '% DIAB1%'
```
## 46 (196. Delete Duplicate Emails)
Write a solution to delete all duplicate emails, keeping only one unique email with the smallest id.
For SQL users, please note that you are supposed to write a DELETE statement and not a SELECT one.
After running your script, the answer shown is the Person table. The driver will first compile and run your piece of code and then show the Person table. The final order of the Person table does not matter.
```sql
DELETE
FROM
    Person
WHERE id NOT IN 
    (SELECT
        min_id
    FROM
    (SELECT
        min(id) AS min_id
    FROM
        Person
    GROUP BY email) as a)
```
## 47 (176. Second Highest Salary)
Write a solution to find the second highest distinct salary from the Employee table. If there is no second highest salary, return null.
```sql
SELECT
    max(salary) AS SecondHighestSalary
FROM
    Employee
WHERE salary < (SELECT max(salary) FROM Employee)
```
## 48 (1484. Group Sold Products By The Date)
Write a solution to find for each date the number of different products sold and their names.
The sold products names for each date should be sorted lexicographically.
Return the result table ordered by sell_date.
```sql
WITH CTE AS (SELECT * FROM Activities ORDER BY sell_date, product)

SELECT 
    sell_date,
    COUNT(DISTINCT product) AS num_sold,
    GROUP_CONCAT(DISTINCT product) AS products
FROM
    CTE
GROUP BY sell_date
```
## 49 (1327. List the Products Ordered in a Period)
Write a solution to get the names of products that have at least 100 units ordered in February 2020 and their amount.
Return the result table in any order.
```sql
SELECT
    product_name,
    SUM(unit) AS unit
FROM
    Products INNER JOIN Orders USING (product_id)
WHERE MONTH(order_date) = 2 AND YEAR(order_date) = 2020
GROUP BY product_id
HAVING SUM(unit) >= 100
```
## 50 (1517. Find Users With Valid E-Mails)
Write a solution to find the users who have valid emails.
A valid e-mail has a prefix name and a domain where:
The prefix name is a string that may contain letters (upper or lower case), digits, underscore '_', period '.', and/or dash '-'. The prefix name must start with a letter.
The domain is '@leetcode.com'.
Return the result table in any order.
```sql
SELECT * fro Users
WHERE regexp_like(mail, '^[A-Za-z]+[A-Za-z0-9_.-]*@leetcode[.]com$','c')
```
