CREATE TABLE libraryspn (
    title TEXT,
    author TEXT,
    quantity INT,
    genre TEXT
);

COPY libraryspn (title, author, quantity, genre)
FROM '/Users/finnodonnell/LibrarySPN/SPN library - SPN_library_strict_genres.csv'
DELIMITER ','
CSV HEADER;

SELECT * FROM libraryspn
WHERE genre ILIKE '%general %'
ORDER BY quantity DESC;

SELECT current_database()