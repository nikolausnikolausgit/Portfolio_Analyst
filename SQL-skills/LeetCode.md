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
```sql
SELECT DISTINCT
    author_id AS id
FROM
    Views
WHERE author_id = viewer_id
ORDER BY author_id
```
## 5 (1683. Invalid Tweets)
```sql
SELECT
    tweet_id
FROM
    Tweets
WHERE LENGTH(content) > 15
```
## 6 (1378. Replace Employee ID With The Unique Identifier)
```sql
SELECT
    unique_id,
    name
FROM Employees LEFT JOIN EmployeeUNI USING(id)
```
## 7 (1068. Product Sales Analysis I)
```sql
SELECT
    product_name,
    year,
    price
FROM Sales INNER JOIN Product USING(product_id)
```
## 8 (1581. Customer Who Visited but Did Not Make Any Transactions)
```sql
SELECT
    customer_id,
    COUNT(*) AS count_no_trans
FROM Visits LEFT JOIN Transactions USING (visit_id)
WHERE transaction_id IS NULL
GROUP BY customer_id
```
## 9 (197. Rising Temperature)
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
```sql
SELECT
    name,
    bonus
FROM
    Employee LEFT JOIN Bonus USING (empId)
WHERE bonus < 1000 OR bonus IS NULL
```
## 12 (1280. Students and Examinations)
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
```sql
SELECT
    project_id,
    ROUND(SUM(experience_years) / COUNT(*), 2) AS average_years
FROM
    Project INNER JOIN Employee USING (employee_id)
GROUP BY project_id
```
## 18 (1633. Percentage of Users Attended a Contest)
```sql
SELECT
    contest_id,
    ROUND(100 * COUNT(*) / (SELECT COUNT(user_id) FROM Users), 2) AS percentage
FROM Register
GROUP BY contest_id
ORDER BY 2 DESC, contest_id
```
## 19 (1211. Queries Quality and Percentage)
```sql
SELECT
    query_name,
    ROUND(AVG(rating/position), 2) AS quality,
    ROUND(100*(SUM(CASE WHEN rating < 3 THEN 1 ELSE 0 END) / COUNT(*)), 2) AS poor_query_percentage
FROM Queries
GROUP BY query_name
```
## 20 (1193. Monthly Transactions I)
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
```sql
SELECT
    customer_id
FROM
    Customer
GROUP BY customer_id
HAVING COUNT(DISTINCT product_key) = (SELECT COUNT(product_key) FROM Product)
```
## 30 (1731. The Number of Employees Which Report to Each Employee)
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
```sql
SELECT
    *,
    IF(x+y>z AND x+z>y AND y+z>x, 'Yes', 'No') AS triangle
FROM
    Triangle
```
## 33 (180. Consecutive Numbers)
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
```sql
SELECT
    user_id,
    CONCAT(LEFT(UPPER(name), 1), SUBSTRING(LOWER(name), 2)) AS name
FROM
    Users
ORDER BY user_id
```
## 45 (1527. Patients With a Condition)
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
```sql
SELECT
    max(salary) AS SecondHighestSalary
FROM
    Employee
WHERE salary < (SELECT max(salary) FROM Employee)
```
## 48 (1484. Group Sold Products By The Date)
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
```sql
SELECT * fro Users
WHERE regexp_like(mail, '^[A-Za-z]+[A-Za-z0-9_.-]*@leetcode[.]com$','c')
```
