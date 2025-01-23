
-- assignment 4



SELECT u.name
FROM user_yelp u
JOIN tip t ON u.user_id = t.user_id
GROUP BY u.name
HAVING SUM(t.compliment_count) = (
    SELECT MAX(total_compliments)
    FROM (

        SELECT SUM(compliment_count) AS total_compliments
        FROM tip
        GROUP BY  user_id
    ) AS compliment_totals
);

SELECT b.name
FROM business b  JOIN review r ON b.business_id = r.business_id
WHERE b.city = 'Edmonton' AND   b.review_count >5
GROUP BY b.business_id,  b.name
HAVING AVG(r.stars) >= 4;


SELECT AVG(b.stars)  AS average_stars
FROM business b
JOIN review r  ON b.business_id = r.business_id
JOIN user_yelp u ON r.user_id = u.user_id
WHERE b.name  LIKE '%Best Buy%'
  AND u.name = 'John'
  AND EXISTS (
      SELECT 1
      FROM review sub_r
      WHERE sub_r.business_id = b.business_id  AND sub_r.useful <= 3
  );


SELECT COUNT(DISTINCT r1.business_id) AS business_count
FROM review r1
JOIN review r2 ON r1.business_id  = r2.business_id 
              AND r1.user_id <> r2.user_id
JOIN friendship f ON (f.user_id = r1.user_id AND f.friend = r2.user_id)
WHERE (r1.useful > 0 AND r2.funny > 0)
   OR (r1.funny > 0 AND r2.useful > 0);



DROP TRIGGER IF EXISTS Updatecount;
GO

CREATE TRIGGER UpdateCount
ON review
AFTER INSERT
AS
BEGIN
    UPDATE b
    SET b.review_count = (
        SELECT COUNT(DISTINCT r.user_id)
        FROM review r
        WHERE r.business_id = b.business_id
    )
    FROM business b
    WHERE b.business_id IN (SELECT DISTINCT business_id FROM inserted);
END;
GO

DROP TRIGGER IF EXISTS check_friend;
GO

CREATE TRIGGER check_friend
ON review
INSTEAD OF INSERT
AS
BEGIN
   
    INSERT INTO review (review_id, user_id, business_id, stars, useful, funny, cool, date)
    SELECT i.review_id, i.user_id, i.business_id, i.stars, i.useful, i.funny, i.cool, i.date
    FROM inserted i
    WHERE EXISTS (
        SELECT 1
        FROM friendship f
        JOIN review r ON f.friend = r.user_id
        WHERE f.user_id = i.user_id AND r.business_id = i.business_id
    );

END;
GO

