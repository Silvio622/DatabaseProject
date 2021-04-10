show databases;
use bus2;
show tables;
select * FROM bus;
select * FROM driver;

DROP database moviesdb;
use moviesdb;
show tables;
show databases;


SELECT * FROM film ORDER BY filmname;

SELECT * FROM actor LIMIT 1;

SELECT * FROM country LIMIT 1;

SELECT ac.ActorID, ac.ActorName, ac.ActorDOB, ac.ActorGender,
ac.ActorCountryID
FROM actor ac
WHERE year(ActorDOB)>= "1950" AND year(ActorDOB)<= "1959"
ORDER BY ActorName;





SELECT di.DirectorName ,lan.language 
FROM film fm
INNER JOIN language lan
ON fm.FilmLanguageID = lan.LanguageID
INNER JOIN director di
ON fm.FilmDirectorID = di.DirectorID
WHERE fm.FilmLanguageID != 1
ORDER BY DirectorName;


SELECT ge.GenreName, COUNT(*)
FROM genre ge
LEFT JOIN film fm
ON ge.GenreID = fm.FilmgenreID
GROUP BY ge.GenreName;










