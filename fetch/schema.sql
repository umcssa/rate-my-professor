CREATE TABLE departments (
  departmentid INTEGER PRIMARY KEY AUTOINCREMENT,
  name         VARCHAR(15) NOT NULL
);

CREATE TABLE courses (
  courseid     INTEGER PRIMARY KEY AUTOINCREMENT,
  departmentid INTEGER      NOT NULL,
  number       INTEGER      NOT NULL,
  title        VARCHAR(150) NOT NULL,
  FOREIGN KEY (departmentid) REFERENCES departments (departmentid)
);

CREATE TABLE professors (
  professorid  INTEGER PRIMARY KEY AUTOINCREMENT,
  departmentid INTEGER     NOT NULL,
  name         VARCHAR(50) NOT NULL,
  FOREIGN KEY (departmentid) REFERENCES departments (departmentid)
);
