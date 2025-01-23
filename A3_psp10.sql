
-- Had to add these checks becuase i was getting errors
IF OBJECT_ID('checkin', 'U') IS NOT NULL
    DROP TABLE checkin;

IF OBJECT_ID('tip', 'U') IS NOT NULL
    DROP TABLE tip;

IF OBJECT_ID('review', 'U') IS NOT NULL
    DROP TABLE review;

IF OBJECT_ID('friendship', 'U') IS NOT NULL
    DROP TABLE friendship;

IF OBJECT_ID('user_yelp', 'U') IS NOT NULL
    DROP TABLE user_yelp;

IF OBJECT_ID('business', 'U') IS NOT NULL
    DROP TABLE business;

	-- make the tables
CREATE TABLE business (
    business_id VARCHAR(22) PRIMARY KEY,
    name VARCHAR(60) NOT NULL,
    address VARCHAR(75),
    city VARCHAR(30) NOT NULL,
    postal_code VARCHAR(7),
    stars DECIMAL(2, 1) CHECK (stars >= 1 AND stars <= 5),
    review_count INT DEFAULT 0 CHECK (review_count >= 0)
);

CREATE TABLE user_yelp (
    user_id VARCHAR(22) PRIMARY KEY,
    name VARCHAR(35) NOT NULL,
    review_count INT DEFAULT 0 CHECK (review_count >= 0),
    yelping_since DATETIME NOT NULL DEFAULT GETDATE(),
    useful INT DEFAULT 0 CHECK (useful >= 0),
    funny INT DEFAULT 0 CHECK (funny >= 0),
    cool INT DEFAULT 0 CHECK (cool >= 0),
    fans INT DEFAULT 0 CHECK (fans >= 0),
    average_stars DECIMAL(3, 2) CHECK (average_stars >= 1 AND average_stars <= 5)
);


CREATE TABLE checkin (
    checkin_id INT PRIMARY KEY,
    business_id VARCHAR(22) NOT NULL,
    date DATETIME NOT NULL DEFAULT GETDATE(),
    FOREIGN KEY (business_id) REFERENCES business(business_id)
);


CREATE TABLE tip (
    tip_id INT PRIMARY KEY,
    user_id VARCHAR(22) NOT NULL,
    business_id VARCHAR(22) NOT NULL,
    date DATETIME NOT NULL DEFAULT GETDATE(),
    compliment_count INT DEFAULT 0 CHECK (compliment_count >= 0),
    FOREIGN KEY (business_id) REFERENCES business(business_id),
    FOREIGN KEY (user_id) REFERENCES user_yelp(user_id)
);


CREATE TABLE review (
    review_id VARCHAR(22) PRIMARY KEY,
    user_id VARCHAR(22) NOT NULL,
    business_id VARCHAR(22) NOT NULL,
    stars INT NOT NULL CHECK (stars >= 1 AND stars <= 5),
    useful INT DEFAULT 0 CHECK (useful >= 0),
    funny INT DEFAULT 0 CHECK (funny >= 0),
    cool INT DEFAULT 0 CHECK (cool >= 0),
    date DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (business_id) REFERENCES business(business_id),
    FOREIGN KEY (user_id) REFERENCES user_yelp(user_id)
);




CREATE TABLE friendship (
    user_id VARCHAR(22),
    friend VARCHAR(22),
    PRIMARY KEY (user_id, friend),
    FOREIGN KEY (user_id) REFERENCES user_yelp(user_id),
    FOREIGN KEY (friend) REFERENCES user_yelp(user_id)
);

BULK INSERT dbo.business 
FROM 'd:\userdata\business.csv' 
WITH (fieldterminator=',',rowterminator='\n', firstrow=2);


BULK INSERT dbo.user_yelp
FROM 'd:\userdata\user_yelp.csv'
WITH (FIELDTERMINATOR = ',', ROWTERMINATOR = '\n', FIRSTROW = 2);

BULK INSERT dbo.checkin
FROM 'd:\userdata\checkin.csv'
WITH (FIELDTERMINATOR = ',', ROWTERMINATOR = '\n', FIRSTROW = 2);

BULK INSERT dbo.tip
FROM 'd:\userdata\tip.csv'
WITH (FIELDTERMINATOR = ',', ROWTERMINATOR = '\n', FIRSTROW = 2);

BULK INSERT dbo.review
FROM 'd:\userdata\review.csv'
WITH (FIELDTERMINATOR = ',', ROWTERMINATOR = '\n', FIRSTROW = 2);

BULK INSERT dbo.friendship
FROM 'd:\userdata\friendship.csv'
WITH (FIELDTERMINATOR = ',', ROWTERMINATOR = '\n', FIRSTROW = 2);


/* result
(5573 rows affected)

(23863 rows affected)

(208923 rows affected)

(15513 rows affected)

(109435 rows affected)

(2473 rows affected)

Completion time: 2024-10-11T16:08:59.4170377-07:00
*/
