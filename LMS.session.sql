-- SQL Script for Library Management System 


CREATE TABLE Genres (
    Genre_ID SERIAL PRIMARY KEY,
    Genre VARCHAR(100) NOT NULL,
    Description TEXT
);


CREATE TABLE Authors (
    Author_ID SERIAL PRIMARY KEY,
    Author_Name VARCHAR(150) NOT NULL,
    BirthDate DATE NOT NULL,
    Email varchar(50) UNIQUE
);

CREATE TABLE Books (
    Book_ID SERIAL PRIMARY KEY,
    Book_Name VARCHAR(255) NOT NULL,
    Author_ID INT,
    Foreign key( Author_ID) REFERENCES Authors(Author_ID) ON DELETE CASCADE,
    Genre_ID INT,
    Foreign key (Genre_ID) REFERENCES Genres(Genre_ID) ON DELETE SET NULL,
    Pages INT,
    Publication_Year DATE,
    ISBN VARCHAR(13) UNIQUE
);




CREATE TABLE Books_Copies (
    Copy_ID SERIAL PRIMARY KEY,
    Book_ID INT,
    Foreign KEY (Book_ID) REFERENCES Books(Book_ID) ON DELETE CASCADE,
    Condition VARCHAR(50),
    Status VARCHAR(50) DEFAULT 'Available'
);

-- Table: Members
CREATE TABLE Members (-
    Member_ID SERIAL PRIMARY KEY,
    Member_Name VARCHAR(150) NOT NULL,
    Email VARCHAR(100) UNIQUE NOT NULL,
    Phone_Number VARCHAR(10),
    Address TEXT,
    Password VARCHAR(255) NOT NULL, -- Store hashed passwords
    Join_Date DATE DEFAULT CURRENT_DATE
);

-- Table: Staff
CREATE TABLE Staff (
    Staff_ID SERIAL PRIMARY KEY,
    Staff_Name VARCHAR(150) NOT NULL,
    Email VARCHAR(100) UNIQUE NOT NULL,
    Phone_Number VARCHAR(15),
    Address TEXT,
    Role VARCHAR(50) DEFAULT 'Staff', -- Can be 'Staff' or 'Admin'
    Join_Date DATE DEFAULT CURRENT_DATE,
    Password VARCHAR(255) NOT NULL -- Store hashed passwords
);

-- Table: Issued
CREATE TABLE Issued (
    Issued_ID SERIAL PRIMARY KEY,
    Copy_ID INT,
    Foreign KEY (Copy_ID) REFERENCES Books_Copies(Copy_ID) ON DELETE CASCADE,
    Member_ID INT,
    Foreign key (Member_ID) REFERENCES Members(Member_ID) ON DELETE CASCADE,
    Issued_Date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Due_Date TIMESTAMP NOT NULL,
    Status VARCHAR(50) DEFAULT 'Issued',
    Staff_ID INT,
    Foreign key (Staff_ID) REFERENCES Staff(Staff_ID) ON DELETE SET NULL
);

-- Table: Fines
CREATE TABLE Fines (
    Fine_ID SERIAL PRIMARY KEY,
    Issued_ID INT,
    Foreign key (Issued_ID) REFERENCES Issued(Issued_ID) ON DELETE CASCADE,
    Amount DECIMAL(10, 2) NOT NULL,
    Fine_Date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Paid_Status BOOLEAN DEFAULT FALSE,
    Payment_Date TIMESTAMP,
    Staff_ID INT,
    Foreign Key (Staff_ID) REFERENCES Staff(Staff_ID) ON DELETE SET NULL
);

-- Table: Reservations
CREATE TABLE Reservations (
    Reservation_ID SERIAL PRIMARY KEY,
    Copy_ID INT,
    Foreign Key (Copy_ID) References Books_Copies(Copy_ID) ON DELETE CASCADE,
    Member_ID INT,
    Foreign key (Member_ID) REFERENCES Members(Member_ID) ON DELETE CASCADE,
    Reservation_Date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Status VARCHAR(50) DEFAULT 'Pending'
);


-- Insert genres
INSERT INTO Genres (Genre, Description)
VALUES 
('Sci-Fi', 'Science fiction stories about futuristic concepts.'),
('Fantasy', 'Fantasy worlds with magic and mythical creatures.'),
('Action', 'Fast-paced, thrilling adventures.'),
('Isekai', 'Stories where characters are transported to another world.'),
('Adventure', 'Exciting journeys with challenges and discoveries.'),
('Magic', 'Stories featuring magical powers and worlds.'),
('Horror', 'Frightening tales designed to scare and thrill.'),
('Romance', 'Love stories and emotional connections.'),
('Mystery', 'Whodunits and thrilling enigmas to solve.'),
('Comedy', 'Lighthearted, humorous tales.'),
('Historical', 'Fiction based on historical events.'),
('Thriller', 'Suspenseful stories with exciting twists.'),
('Drama', 'Emotionally intense narratives.'),
('Cyberpunk', 'High-tech, low-life dystopian settings.'),
('Steampunk', 'Stories with retro-futuristic steam-powered technology.'),
('Epic Fantasy', 'Grand tales of heroism and magic.'),
('Urban Fantasy', 'Magical tales set in modern urban settings.'),
('Dark Fantasy', 'Fantasy with dark and eerie themes.'),
('Post-Apocalyptic', 'Stories about surviving after world-ending events.'),
('Supernatural', 'Tales of ghosts, spirits, and the paranormal.');

-- Insert authors
INSERT INTO Authors (Author_Name, BirthDate, Email)
VALUES 
('John Smith', '1975-02-15', 'johnsmith@example.com'),
('Jane Doe', '1980-06-30', 'janedoe@example.com'),
('Emily Carter', '1990-12-01', 'emilycarter@example.com'),
('Michael Johnson', '1988-09-20', 'michaeljohnson@example.com'),
('Sarah Connor', '1979-08-10', 'sarahconnor@example.com'),
('William Brown', '1975-03-15', 'williambrown@example.com'),
('Sophia Davis', '1991-05-25', 'sophiadavis@example.com'),
('Daniel Wilson', '1985-12-09', 'danielwilson@example.com'),
('Emma Thompson', '1983-11-01', 'emmathompson@example.com'),
('Oliver Martinez', '1987-06-20', 'olivermartinez@example.com'),
('Liam Anderson', '1978-04-19', 'liamanderson@example.com'),
('Charlotte White', '1993-08-30', 'charlottewhite@example.com'),
('James Lee', '1982-02-14', 'jameslee@example.com'),
('Isabella King', '1990-10-22', 'isabellaking@example.com'),
('Benjamin Harris', '1986-01-17', 'benjaminharris@example.com'),
('Mia Scott', '1995-09-11', 'miascott@example.com'),
('Elijah Young', '1976-07-07', 'elijahyoung@example.com'),
('Amelia Wright', '1992-03-05', 'ameliawright@example.com'),
('Noah Hall', '1984-12-13', 'noahhall@example.com'),
('Lucas Green', '1977-10-25', 'lucasgreen@example.com');

-- Insert books
INSERT INTO Books (Book_Name, Author_ID, Genre_ID, Pages, Publication_Year, ISBN)
VALUES 
('The Galactic Voyage', 1, 1, 300, '2015-08-20', '9781234567890'),
('Enchanted Kingdom', 2, 2, 250, '2018-05-10', '9781234567891'),
('Heroes of Valor', 3, 3, 320, '2020-12-01', '9781234567892'),
('Portal to Another World', 4, 4, 280, '2019-11-15', '9781234567893'),
('Adventurer’s Quest', 5, 5, 400, '2021-07-07', '9781234567894'),
('Magical Realms', 6, 6, 350, '2017-03-18', '9781234567895'),
('Haunted Shadows', 7, 7, 290, '2020-10-05', '9781234567896'),
('Love in the Stars', 8, 8, 240, '2016-04-22', '9781234567897'),
('Detective Chronicles', 9, 9, 310, '2019-09-14', '9781234567898'),
('Comedy Nights', 10, 10, 220, '2022-01-11', '9781234567899'),
('The War Saga', 11, 1, 330, '2014-05-07', '9781234567900'),
('Steampunk Adventures', 12, 15, 280, '2018-12-25', '9781234567901'),
('Cyberpunk Dreams', 13, 14, 370, '2019-06-30', '9781234567902'),
('Fantasy Legends', 14, 2, 420, '2021-02-18', '9781234567903'),
('Dark Realms', 15, 19, 290, '2020-08-03', '9781234567904');

-- Insert members
INSERT INTO Members (Member_Name, Email, Phone_Number, Address, Password, Join_Date)
VALUES 
('Alice Johnson', 'alice@example.com', '9876543210', '123 Main St', 'hashedpassword1', '2020-05-15'),
('Bob Smith', 'bob@example.com', '9876543211', '456 Oak Ave', 'hashedpassword2', '2019-08-20'),
('Catherine Brown', 'catherine@example.com', '9876543212', '789 Pine Rd', 'hashedpassword3', '2021-01-10'),
('David Wilson', 'david@example.com', '9876543213', '321 Maple Dr', 'hashedpassword4', '2018-12-25'),
('Emma Davis', 'emma@example.com', '9876543214', '654 Birch Ln', 'hashedpassword5', '2022-07-01');

-- Insert staff
INSERT INTO Staff (Staff_Name, Email, Phone_Number, Address, Role, Password, Join_Date)
VALUES 
('Admin User', 'admin@example.com', '9876543200', 'Library HQ', 'Admin', 'adminhashedpass', '2017-09-12'),
('Staff One', 'staff1@example.com', '9876543201', 'Library Branch 1', 'Staff', 'staff1hashedpass', '2019-11-05'),
('Staff Two', 'staff2@example.com', '9876543202', 'Library Branch 2', 'Staff', 'staff2hashedpass', '2020-03-18');
-- Insert book copies
INSERT INTO Books_Copies (Book_ID, Condition, Status)
VALUES
(1, 'New', 'Available'),
(1, 'Good', 'Issued'),
(1, 'Fair', 'Available'),
(2, 'New', 'Available'),
(2, 'Good', 'Available'),
(3, 'New', 'Issued'),
(3, 'Good', 'Available'),
(4, 'Fair', 'Available'),
(4, 'Poor', 'Damaged'),
(5, 'New', 'Available'),
(5, 'Good', 'Issued'),
(6, 'Fair', 'Available'),
(6, 'Good', 'Available'),
(7, 'New', 'Available'),
(7, 'Good', 'Issued'),
(8, 'Fair', 'Available'),
(8, 'New', 'Available'),
(9, 'Good', 'Available'),
(9, 'New', 'Available'),
(10, 'Good', 'Issued'),
(10, 'Fair', 'Available'),
(11, 'New', 'Available'),
(11, 'Fair', 'Issued'),
(12, 'Good', 'Available'),
(12, 'New', 'Available'),
(13, 'Fair', 'Available'),
(13, 'New', 'Available'),
(14, 'Good', 'Available'),
(14, 'New', 'Available'),
(15, 'Fair', 'Available'),
(15, 'Good', 'Available'),
(15, 'New', 'Issued');

-- Insert issued books
INSERT INTO Issued (Copy_ID, Member_ID, Issued_Date, Due_Date, Status, Staff_ID)
VALUES 
(1, 1, '2023-01-10', '2023-01-20', 'Returned', 1),
(2, 2, '2023-02-15', '2023-02-25', 'Issued', 2),
(3, 3, '2023-03-01', '2023-03-11', 'Issued', 1);

-- Insert fines
INSERT INTO Fines (Issued_ID, Amount, Fine_Date, Paid_Status, Payment_Date, Staff_ID)
VALUES 
(4, 10.00, '2023-01-22', TRUE, '2023-01-25', 1),
(5, 5.00, '2023-02-28', FALSE, NULL, 2);

-- Insert reservations
INSERT INTO Reservations (Copy_ID, Member_ID, Reservation_Date, Status)
VALUES 
(4, 4, '2023-03-15', 'Pending'),
(5, 5, '2023-03-18', 'Completed');

INSERT INTO Books (Book_Name, Author_ID, Genre_ID, Pages, Publication_Year, ISBN)
VALUES 
('Beyond the Horizon', 16, 5, 280, '2017-11-23', '9781234567905'),
('Mystery of the Lost Artifact', 17, 9, 320, '2015-06-14', '9781234567906'),
('The AI Paradox', 18, 12, 350, '2023-09-30', '9781234567907'),
('Parallel Universes', 19, 1, 400, '2020-07-19', '9781234567908'),
('Echoes of the Past', 20, 3, 270, '2018-02-08', '9781234567909'),
('Dystopian Future', 21, 14, 380, '2021-04-12', '9781234567910'),
('The Last Sorcerer', 22, 2, 290, '2019-08-25', '9781234567911'),
('Gothic Tales', 23, 19, 260, '2016-12-07', '9781234567912'),
('The Secret of Moonlight Manor', 24, 7, 310, '2017-09-15', '9781234567913'),
('The Lost Civilization', 25, 8, 360, '2022-03-29', '9781234567914'),
('Alien Encounters', 26, 1, 390, '2018-11-04', '9781234567915'),
('The Hacker Chronicles', 27, 12, 340, '2021-05-17', '9781234567916'),
('The Timeless Traveler', 28, 4, 410, '2020-10-20', '9781234567917'),
('Medieval Legends', 29, 5, 280, '2015-01-09', '9781234567918'),
('Tales of the Unknown', 30, 6, 230, '2019-07-23', '9781234567919');


INSERT INTO Authors (Author_Name, BirthDate, Email)  
VALUES  
('John Carter', '1975-06-12', 'john.carter@example.com'),  
('Emma Williams', '1982-09-25', 'emma.williams@example.com'),  
('Robert Johnson', '1968-04-18', 'robert.johnson@example.com'),  
('Sophia Martinez', '1990-07-10', 'sophia.martinez@example.com'),  
('Michael Anderson', '1979-02-28', 'michael.anderson@example.com'),  
('Olivia Brown', '1985-11-05', 'olivia.brown@example.com'),  
('David Thompson', '1993-03-14', 'david.thompson@example.com'),  
('Emily Clark', '1987-08-22', 'emily.clark@example.com'),  
('James Wilson', '1970-01-30', 'james.wilson@example.com'),  
('Charlotte White', '1995-05-17', 'charlotte.white@example.com'),  
('Benjamin Hall', '1980-12-11', 'benjamin.hall@example.com'),  
('Amelia Scott', '1992-06-09', 'amelia.scott@example.com'),  
('Daniel Harris', '1976-10-20', 'daniel.harris@example.com'),  
('Victoria Lee', '1984-04-02', 'victoria.lee@example.com'),  
('Alexander Lewis', '1991-09-08', 'alexander.lewis@example.com'),  
('Natalie King', '1989-07-27', 'natalie.king@example.com'),  
('William Adams', '1974-03-12', 'william.adams@example.com'),  
('Samantha Baker', '1996-11-23', 'samantha.baker@example.com'),  
('Ethan Roberts', '1981-02-14', 'ethan.roberts@example.com'),  
('Grace Collins', '1994-12-31', 'grace.collins@example.com'),  
('Henry Mitchell', '1983-05-29', 'henry.mitchell@example.com'),  
('Madison Perez', '1997-08-15', 'madison.perez@example.com'),  
('Liam Campbell', '1977-09-06', 'liam.campbell@example.com'),  
('Isabella Evans', '1986-07-01', 'isabella.evans@example.com'),  
('Noah Rogers', '1998-04-30', 'noah.rogers@example.com'),  
('Harper Stewart', '1973-06-22', 'harper.stewart@example.com'),  
('Lucas Turner', '1988-01-05', 'lucas.turner@example.com'),  
('Mia Parker', '1990-10-09', 'mia.parker@example.com'),  
('Elijah Morris', '1982-03-18', 'elijah.morris@example.com'),  
('Abigail Reed', '1999-07-20', 'abigail.reed@example.com');  










        Select members.member_name,books.book_name,reservations.reservation_date,reservations.status 
        from reservations
        inner join members On reservations.member_id=members.member_id
        inner join books_copies On reservations.copy_id=books_copies.copy_id
        inner join books on books.book_id=books_copies.book_id;


        SELECT *from issued;



Select members.member_name,books.book_name,issued.issued_date FROM issued
inner join members ON members.member_id=issued.member_id
inner join books_copies On books_copies.copy_id=issued.copy_id
inner join books ON books.book_id=books_copies.book_id


SELECT B.Book_Name,A.author_name,G.genre,B.Publication_Year,B.Pages FROM books as B inner join authors as A On B.Author_ID=A.Author_ID inner join Genres as G On G.Genre_ID=B.Genre_ID where B.book_id=2

select *from books_copies;
select Book_id,Count(book_id) from books_copies
Where book_id = 2

Group by book_id



select *from books;

ALTER TABLE books 
    ADD COLUMN IF NOT EXISTS Synopsis VARCHAR(200);

select *from books_copies;


INSERT INTO Books_Copies (Book_ID, Condition, Status)
VALUES
(32, 'New', 'Available')

select *from books;

select *from books_copies;
                select Count(book_id) from books_copies
                Where book_id = 32
                Group by book_id

                INSERT INTO Books_Copies (Book_ID, Condition, Status)
                    VALUES
                    (39, 'New', 'Available')