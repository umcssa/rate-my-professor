CREATE TABLE department (
  department_id INTEGER PRIMARY KEY AUTOINCREMENT,
  name          VARCHAR(15) NOT NULL
);

CREATE TABLE course (
  course_id     INTEGER PRIMARY KEY AUTOINCREMENT,
  department_id INTEGER      NOT NULL,
  number        INTEGER      NOT NULL,
  title         VARCHAR(150) NOT NULL,
  credits       VARCHAR(15)  NOT NULL,
  FOREIGN KEY (department_id) REFERENCES department (department_id)
);

CREATE TABLE professor (
  professor_id  INTEGER PRIMARY KEY AUTOINCREMENT,
  department_id INTEGER     NOT NULL,
  name          VARCHAR(50) NOT NULL,
  FOREIGN KEY (department_id) REFERENCES department (department_id)
);

CREATE TABLE semester (
  semester_id INTEGER PRIMARY KEY AUTOINCREMENT,
  year        INTEGER    NOT NULL,
  season      VARCHAR(6) NOT NULL,
  CHECK (season = 'spring' OR
         season = 'summer' OR
         season = 'fall' OR
         season = 'winter')
);

CREATE TABLE rate (
  rate_id        INTEGER PRIMARY KEY AUTOINCREMENT,
  timestamp      TIMESTAMP           DEFAULT CURRENT_TIMESTAMP NOT NULL,
  course_id      INTEGER,
  course_title   VARCHAR(150),
  professor_id   INTEGER,
  professor_name VARCHAR(50),
  semester_id    INTEGER     NOT NULL,
  credits        INTEGER,
  isHU           INTEGER     NOT NULL,
  isSS           INTEGER     NOT NULL,
  isNS           INTEGER     NOT NULL,
  isID           INTEGER     NOT NULL,
  isRE           INTEGER     NOT NULL,
  isOther        INTEGER     NOT NULL,
  grade          VARCHAR(10) NOT NULL,
  difficulty     DOUBLE      NOT NULL,
  quality        DOUBLE      NOT NULL,
  workload       DOUBLE      NOT NULL,
  recommend      INTEGER     NOT NULL,
  suggestion     VARCHAR(2000),
  viewable       INTEGER             DEFAULT 0 NOT NULL,
  CHECK (grade = 'A Range' OR
         grade = 'B Range' OR
         grade = 'C Range' OR
         grade = 'P/F' OR
         grade = 'Others'),
  CHECK (difficulty >= 0 AND difficulty <= 1),
  CHECK (quality >= 0 AND quality <= 1),
  CHECK (workload >= 0 AND workload <= 1),
  CHECK (recommend >= 0 AND recommend <= 1),
  FOREIGN KEY (course_id) REFERENCES course (course_id),
  FOREIGN KEY (professor_id) REFERENCES professor (professor_id),
  FOREIGN KEY (semester_id) REFERENCES semester (semester_id)
);
