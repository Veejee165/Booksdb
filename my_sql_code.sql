DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS nocount;

CREATE TABLE IF NOT EXISTS books (
  bookid INTEGER PRIMARY KEY AUTOINCREMENT,
  year INTEGER,
  title VARCHAR(30),
  author VARCHAR(30),
  course VARCHAR(20),
  id CHAR(13),
  number INTEGER
);

CREATE TABLE IF NOT EXISTS nocount(
  cno INTEGER,
  number INTEGER,
  id CHAR(13),
  PRIMARY KEY(id)
);

CREATE TRIGGER IF NOT EXISTS check_number
BEFORE INSERT ON books
FOR EACH ROW
WHEN NEW.number <= 0
BEGIN
  SELECT RAISE(ABORT, 'Number must be greater than zero');
END;

CREATE TRIGGER IF NOT EXISTS check_count
BEFORE INSERT ON books
FOR EACH ROW
WHEN (SELECT COUNT(*) FROM nocount WHERE id = NEW.id) >= 6
BEGIN
  SELECT RAISE(ABORT, 'Maximum 6 books allowed per student');
END;

CREATE TRIGGER IF NOT EXISTS insert_nocount
AFTER INSERT ON books
WHEN (SELECT COUNT(*) FROM nocount WHERE id = NEW.id) = 0
BEGIN
  -- if the id is not present, insert a new row into nocount
  INSERT INTO nocount (id, number, cno) VALUES (NEW.id, 0, NEW.number);
END;

CREATE TRIGGER IF NOT EXISTS update_nocount
AFTER INSERT ON books
WHEN (SELECT COUNT(*) FROM nocount WHERE id = NEW.id) > 0
BEGIN
  -- if the id is present, update the count in nocount
  UPDATE nocount SET number = number + 1 WHERE id = NEW.id;
END;
