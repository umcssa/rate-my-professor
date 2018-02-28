CREATE TABLE department (
  department_id INTEGER PRIMARY KEY AUTOINCREMENT,
  name         VARCHAR(15) NOT NULL
);

CREATE TABLE course (
  course_id     INTEGER PRIMARY KEY AUTOINCREMENT,
  department_id INTEGER      NOT NULL,
  number       INTEGER      NOT NULL,
  title        VARCHAR(150) NOT NULL,
  credits      VARCHAR(15)  NOT NULL,
  FOREIGN KEY (department_id) REFERENCES department (department_id)
);

CREATE TABLE professor (
  professor_id  INTEGER PRIMARY KEY AUTOINCREMENT,
  department_id INTEGER     NOT NULL,
  name         VARCHAR(50) NOT NULL,
  FOREIGN KEY (department_id) REFERENCES department (department_id)
);
