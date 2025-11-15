-- ==========================
-- CampusFind Database Schema
-- ==========================

-- Students Table
CREATE TABLE IF NOT EXISTS student (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    student_id TEXT UNIQUE NOT NULL,
    phone TEXT,
    profile_picture TEXT,
    is_active BOOLEAN DEFAULT 1,
    is_verified BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Admins Table
CREATE TABLE IF NOT EXISTS admin (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    is_active BOOLEAN DEFAULT 1,
    is_staff BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Categories Table
CREATE TABLE IF NOT EXISTS category (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Locations/Buildings Table
CREATE TABLE IF NOT EXISTS location (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    building_name TEXT UNIQUE NOT NULL,
    building_code TEXT UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Items Table (found/lost items)
CREATE TABLE IF NOT EXISTS item (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    category_id INTEGER NOT NULL,
    location_id INTEGER NOT NULL,
    status TEXT CHECK (status IN ('Lost', 'Found', 'Returned', 'Unclaimed')) DEFAULT 'Found',
    item_type TEXT CHECK (item_type IN ('Found', 'Lost')) NOT NULL,
    evidence_file TEXT,
    reported_by_id INTEGER NOT NULL,
    reported_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES category (id),
    FOREIGN KEY (location_id) REFERENCES location (id),
    FOREIGN KEY (reported_by_id) REFERENCES student (id)
);

-- Reports Table
CREATE TABLE IF NOT EXISTS report (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id INTEGER NOT NULL,
    report_type TEXT CHECK (report_type IN ('Found', 'Lost')) NOT NULL,
    description TEXT NOT NULL,
    created_by_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (item_id) REFERENCES item (id),
    FOREIGN KEY (created_by_id) REFERENCES student (id)
);

-- Claims Table
CREATE TABLE IF NOT EXISTS claim (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id INTEGER NOT NULL,
    claimed_by_id INTEGER NOT NULL,
    status TEXT CHECK (status IN ('Pending', 'Approved', 'Rejected')) DEFAULT 'Pending',
    evidence_file TEXT,
    claim_description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (item_id) REFERENCES item (id),
    FOREIGN KEY (claimed_by_id) REFERENCES student (id),
    UNIQUE(item_id, claimed_by_id)
);

-- Audit Log Table
CREATE TABLE IF NOT EXISTS audit (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    action TEXT NOT NULL,
    affected_table TEXT NOT NULL,
    affected_id INTEGER NOT NULL,
    changed_by_id INTEGER,
    claim_id INTEGER,
    item_id INTEGER,
    old_value TEXT,
    new_value TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (changed_by_id) REFERENCES admin (id),
    FOREIGN KEY (claim_id) REFERENCES claim (id),
    FOREIGN KEY (item_id) REFERENCES item (id)
);

-- ==========================
-- Views
-- ==========================

-- Lost Items View
CREATE VIEW IF NOT EXISTS lost_items_view AS
SELECT 
    i.id,
    i.name,
    i.description,
    i.category_id,
    c.name as category_name,
    i.location_id,
    l.building_name,
    i.status,
    i.reported_date,
    s.first_name,
    s.last_name,
    s.email
FROM item i
JOIN category c ON i.category_id = c.id
JOIN location l ON i.location_id = l.id
JOIN student s ON i.reported_by_id = s.id
WHERE i.item_type = 'Lost' AND i.status IN ('Lost', 'Unclaimed');

-- Student History View
CREATE VIEW IF NOT EXISTS student_history_view AS
SELECT 
    i.id,
    i.name,
    i.description,
    i.category_id,
    c.name as category_name,
    i.location_id,
    l.building_name,
    i.status,
    i.reported_date,
    i.reported_by_id,
    s.first_name,
    s.last_name
FROM item i
JOIN category c ON i.category_id = c.id
JOIN location l ON i.location_id = l.id
JOIN student s ON i.reported_by_id = s.id;

-- Unclaimed Found Items View
CREATE VIEW IF NOT EXISTS unclaimed_found_items_view AS
SELECT 
    i.id,
    i.name,
    i.description,
    i.category_id,
    c.name as category_name,
    i.location_id,
    l.building_name,
    i.status,
    i.reported_date,
    COUNT(cl.id) as claim_count
FROM item i
JOIN category c ON i.category_id = c.id
JOIN location l ON i.location_id = l.id
LEFT JOIN claim cl ON i.id = cl.item_id AND cl.status = 'Pending'
WHERE i.item_type = 'Found' AND i.status = 'Found'
GROUP BY i.id;

-- ==========================
-- Sample Data
-- ==========================

-- Categories
INSERT OR IGNORE INTO category (id, name, description) VALUES
(1, 'Electronics', 'Phones, laptops, headphones, etc.'),
(2, 'Books', 'Textbooks and notebooks'),
(3, 'Clothing', 'Jackets, bags, shoes, etc.'),
(4, 'Documents', 'IDs, certificates, documents'),
(5, 'Other', 'Miscellaneous items');

-- Locations
INSERT OR IGNORE INTO location (id, building_name, building_code, description) VALUES
(1, 'Science Building', 'SCI', 'Main science building'),
(2, 'Library', 'LIB', 'Central library'),
(3, 'Engineering Building', 'ENG', 'Engineering department'),
(4, 'Student Center', 'SC', 'Student center and cafeteria'),
(5, 'Arts Building', 'ART', 'Arts and humanities');

-- Students
INSERT OR IGNORE INTO student (id, email, password_hash, first_name, last_name, student_id, phone, is_active, is_verified) VALUES
(1, 'alice@university.edu', 'pbkdf2_sha256$260000$1234567890abcdef$hash1', 'Alice', 'Johnson', 'STU001', '555-0001', 1, 1),
(2, 'bob@university.edu', 'pbkdf2_sha256$260000$1234567890abcdef$hash2', 'Bob', 'Smith', 'STU002', '555-0002', 1, 1),
(3, 'charlie@university.edu', 'pbkdf2_sha256$260000$1234567890abcdef$hash3', 'Charlie', 'Brown', 'STU003', '555-0003', 1, 1),
(4, 'diana@university.edu', 'pbkdf2_sha256$260000$1234567890abcdef$hash4', 'Diana', 'Prince', 'STU004', '555-0004', 1, 0);

-- Admins
INSERT OR IGNORE INTO admin (id, email, password_hash, first_name, last_name, is_active, is_staff) VALUES
(1, 'admin@university.edu', 'pbkdf2_sha256$260000$1234567890abcdef$hash_admin1', 'John', 'Admin', 1, 1),
(2, 'manager@university.edu', 'pbkdf2_sha256$260000$1234567890abcdef$hash_admin2', 'Jane', 'Manager', 1, 1);

-- Items (Mixed found and lost)
INSERT OR IGNORE INTO item (id, name, description, category_id, location_id, status, item_type, reported_by_id, reported_date) VALUES
(1, 'iPhone 13', 'Black iPhone 13 with cracked screen, in otter box', 1, 2, 'Found', 'Found', 1, '2025-11-10 10:00:00'),
(2, 'Advanced Calculus Textbook', 'Blue cover, 5th edition', 2, 1, 'Unclaimed', 'Found', 2, '2025-11-11 09:30:00'),
(3, 'Student ID Badge', 'Lost near student center, name: Charlie Brown', 4, 4, 'Lost', 'Lost', 3, '2025-11-12 14:15:00'),
(4, 'Navy Blue Backpack', 'Missing from engineering building', 3, 3, 'Lost', 'Lost', 1, '2025-11-12 16:45:00'),
(5, 'Laptop (Dell XPS)', 'Silver Dell XPS 15, left in library', 1, 2, 'Found', 'Found', 2, '2025-11-13 08:00:00');

-- Reports
INSERT OR IGNORE INTO report (id, item_id, report_type, description, created_by_id) VALUES
(1, 1, 'Found', 'Found in library, black iPhone 13 with otter box, no owner info', 1),
(2, 2, 'Found', 'Found on third floor of science building, advanced calculus textbook', 2),
(3, 3, 'Lost', 'Lost my student ID near student center, need replacement', 3),
(4, 4, 'Lost', 'Navy blue backpack with electronics inside, lost in engineering building', 1),
(5, 5, 'Found', 'Found laptop in library study area, appears to be Dell XPS', 2);

-- Claims
INSERT OR IGNORE INTO claim (id, item_id, claimed_by_id, status, claim_description) VALUES
(1, 1, 1, 'Pending', 'This is my iPhone, has my contacts inside'),
(2, 2, 3, 'Pending', 'I need this textbook for my calculus class'),
(3, 5, 1, 'Approved', 'This is definitely my laptop, I left it in the library yesterday');

-- Audit Logs
INSERT OR IGNORE INTO audit (id, action, affected_table, affected_id, changed_by_id, item_id, new_value) VALUES
(1, 'CLAIM_APPROVED', 'claim', 3, 1, 5, 'Approved'),
(2, 'ITEM_STATUS_UPDATED', 'item', 5, 1, 5, 'Returned');
