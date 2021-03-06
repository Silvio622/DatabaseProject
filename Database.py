# Project for Applied Databases
# Author: Silvio Dunst

import pymysql
import datetime
import pymongo
import keyboard


conn = None #create a variable for the connection to the MySQL database set to None for default


# Connection to the datbase
def connect():# makes a connection to a database
    global conn # make the variable "conn" global to see it in all functions
    conn = pymysql.connect(host="localhost", user="root", password="root", port=3306, db="moviesdb", cursorclass=pymysql.cursors.DictCursor)



# Menu 1 View Films
def view_films():
    global conn # make the variable "conn" global to see it in all functions
    conn = pymysql.connect(host="localhost", user="root", password="root", port=3306, db="moviesdb", cursorclass=pymysql.cursors.DictCursor)

    if not conn:
        connect() # call the connect function to connect to the database
    
    query = "SELECT film.FilmName, actor.ActorName FROM film INNER JOIN filmcast ON film.FilmID = filmcast.CastFilmID INNER JOIN actor ON filmcast.CastActorID = actor.ActorID ORDER BY film.FilmName ASC, actor.ActorName ASC "
    
    with conn:
        cursor = conn.cursor() # this returns a cursor object
        cursor.execute(query) # execute the query variable and pass in "number" in the placeholder %s. number comes from the parameter what is passed in in the function
        films = cursor.fetchall() # create a variable with returns all rows from the database into it
        return films
    

# Menu 2 View Actors by Year of Birth & Gender
def view_actors():    
    birthyear = int(input("Year of Birth :"))
    
    if birthyear >= 1913 and birthyear <= 1994:
        strbirthyear = str(birthyear)
    else:
        view_actors() 

    global conn # make the variable "conn" global to see it in all functions
    conn = pymysql.connect(host="localhost", user="root", password="root", port=3306, db="moviesdb", cursorclass=pymysql.cursors.DictCursor)

    while True:
        gender = input("Gender (Male/Female) :")

        if gender == "Male" or gender == "Female":
            
            if not conn:
                connect() # call the connect function to connect to the database     
        
            query = "SELECT * FROM actor WHERE year(ActorDOB) = %s AND ActorGender LIKE %s"         
        
            with conn: # close the connection
                cursor = conn.cursor() # this returns a cursor object
                cursor.execute(query,(strbirthyear,gender)) # ,birthyear,gender # execute the query variable and pass in "strbirthyear" and "gender"in the placeholders %s. number comes from the parameter what is passed in in the function
                actors = cursor.fetchall() # create a variable with returns all rows from the database into it
                return actors
                break

        elif gender == "":
            
            if not conn:
                connect() # call the connect function to connect to the database     
        
            query = "SELECT * FROM actor WHERE year(ActorDOB) = %s"         
        
            with conn: # close the connection
                cursor = conn.cursor() # this returns a cursor object
                cursor.execute(query,(strbirthyear))  # execute the query variable and pass in "number" in the placeholder %s. number comes from the parameter what is passed in in the function
                actors = cursor.fetchall() # create a variable with returns all rows from the database into it
                return actors 
                break     
      

# Menu 3 View Studios
def view_studios():
    global conn # make the variable "conn" global to see it in all functions
    conn = pymysql.connect(host="localhost", user="root", password="root", port=3306, db="moviesdb", cursorclass=pymysql.cursors.DictCursor)

    if not conn:
        connect() # call the connect function to connect to the database 
    
    query = "SELECT * FROM studio ORDER BY StudioID " # database query Select all rows from table teacher where the column experience < %s is the placeholder              

    with conn: # close the connection
        cursor = conn.cursor() # this returns a cursor object
        cursor.execute(query) # execute the query variable and pass in "number" in the placeholder %s. number comes from the parameter what is passed in in the function
        studios = cursor.fetchall() # create a variable with returns all rows from the database into it
        
        return studios
  
# Menu 4 Add New Country
def add_country():
    global countryid
    global countryname
    try:
        countryid = int(input("ID : "))
    except ValueError:
        add_country()
    
    while True:
        countryname = input("Name : ")
        if countryname != "":
            break
    
    global conn # make the variable "conn" global to see it in all functions
    conn = pymysql.connect(host="localhost", user="root", password="root", port=3306, db="moviesdb", cursorclass=pymysql.cursors.DictCursor)
    

    if not conn:
        connect() # call the connect function to connect to the database 
    
    query = "INSERT INTO country (CountryID, CountryName) VALUES (%s,%s)"

    with conn: # close the connection
        try:
            cursor = conn.cursor() # this returns a cursor object
            cursor.execute(query,(countryid,countryname))
            conn.commit()
            print("")
            print("Country: {} , {} added to database".format(countryid,countryname))

        except pymysql.err.IntegrityError:
            print("")
            print("*** ERROR ***: ID and/or Name ({} , {}) already exist".format(countryid,countryname))

    
myclient = None

def mongo_connect():
    global myclient
    myclient = pymongo.MongoClient(host="localhost",port=27017) # connect to the Mongo deamon
    myclient.admin.command("ismaster")


def mongo_find():
    db = myclient["movieScriptsDB"]# call the database
    docs = db["movieScripts"]# call the collection/table
    
    querymongo = {"subtitles": subtitle}# read out the attribute "subtitle" in the Mongo database collection
    dbsubtitles = docs.find(querymongo)
        
    
    for sub in dbsubtitles:
        moviesid = []
        moviesid = sub["_id"]
                
        global conn # make the variable "conn" global to see it in all functions
        conn = pymysql.connect(host="localhost", user="root", password="root", port=3306, db="moviesdb", cursorclass=pymysql.cursors.DictCursor)
        
        if not conn:
            connect() # call the connect function to connect to the SQL database 
            
        querysql = "SELECT FilmName, FilmSynopsis FROM film WHERE FilmId = %s "

        with conn: # close the connection
            cursor = conn.cursor() # this returns a cursor object
            cursor.execute(querysql,(moviesid))  # execute the query variable and pass in "number" in the placeholder %s. number comes from the parameter what is passed in in the function
            films = cursor.fetchall() # create a variable with returns all rows from the database into it

        for film in films:
            print(film["FilmName"],"??",film["FilmSynopsis"][0:30])# print only a length of 30 string characters

    

# Menu 5 View Movies with Subtitles
def view_movies():
    global subtitle 
    subtitle = ""
    subtitle = input("Enter subtitle language: ")
    if subtitle == "":
        view_movies()
        subtitle = ""
        
    else:
        if not myclient:# if no connections are made
            try:
                mongo_connect()# connect to the database
                mongo_find()
                
            except Exception as e:
                print("Error", e)
                    

def mongo_insert():
    db = myclient["movieScriptsDB"]# call the database
    docs = db["movieScripts"]# call the collection/table
    
    try:
        docs.insert_one(newmoviedic)# insert one document the dictionary newmoviedic into the mongo database
    except pymongo.errors.DuplicateKeyError as e:
        print("")
        print("*** ERROR ***: Movie Script with id: {} already exist".format(newmovieid))

    except Exception as e:
        print("Error",e)
            

# Menu 6 Add New Movie Script
def new_movie():
    global keywordslist
    global subtitleslist
    global newmovieid
    global newmoviedic
    keywordslist = []
    subtitleslist = []  
    
    
    while True: # Insert a valid Movie ID
        try:
            newmovieid = int(input("ID : "))
        except ValueError:
            new_movie()

        if newmovieid >= 0:
            break
    

    keyword = ""
    
    while True: # Insert keywords
        keyword = input("Keyword<-1 to end>: ")
        if keyword == "-1":
            break
        else:
            keywordslist.append(keyword)        

    subtitlelanguage = ""
    
    while True: # Insert Subtitles Languages
        subtitlelanguage = input("Subtitles Languages <-1 to end>: ")
        if subtitlelanguage == "-1":
            break
        else:
            subtitleslist.append(subtitlelanguage)

    newmoviedic = {"_id":newmovieid ,"keywords":keywordslist,"subtitles":subtitleslist}


    # Connect to moviesDB SQL Database and check if the movie id exist in the Database
    global conn # make the variable "conn" global to see it in all functions
    conn = pymysql.connect(host="localhost", user="root", password="root", port=3306, db="moviesdb", cursorclass=pymysql.cursors.DictCursor)
    

    if not conn:
        connect() # call the connect function to connect to the database 
    
    queryfm = "SELECT filmID FROM film WHERE filmID LIKE %s"

    with conn: # close the connection
        try:
            cursor = conn.cursor() # this returns a cursor object
            cursor.execute(queryfm,(newmovieid))
            conn.commit()
            checkfilmid = cursor.fetchone() # returns the filmid if it exist if it not exists it returns None
                        
        except pymysql.err.IntegrityError as e:
            print("*** Error ***:",e)
                        

    if checkfilmid == None:# the filmid does not exist in the movieDB SQL Database
        print("")
        print("*** ERROR ***: Film with id: {} does not exist in moviesDB".format(newmovieid))
        return checkfilmid

    elif checkfilmid != None:
        checkfilmid = checkfilmid
                   

    # Connect to Mongo Database 
    if not myclient:# if no connections are made
        try:
            mongo_connect()# connect to the database
            mongo_insert()
        except Exception as e:
            print("Error", e)
     
   

studiocount = 0

def main(): 
    display_Menu()
    display_Choice()

def display_Choice():
    
    choice = input("Choice:")

    if choice == "1" or choice == "2" or choice == "3" or choice == "4" or choice == "5" or choice == "6" or choice == "x": 
        print("")
    else:
        print("Invalid Input Please try again!")
        
        main() # Return to main() menu
        

    if choice == "1":
        print("Films")
        print("-----")
        
        films = view_films()
        count = 0
        while True:
            try:
                if not keyboard.is_pressed('q'):
                    print("pressed")
                    break
            except:
                break
        #keyboard.wait()
        '''
        for film in films:            
            print(film["FilmName"],"??",film["ActorName"])
            count = count + 1
            if count == 5:
                break
        '''

        for index,film in enumerate(iterable=films,start=10):
            print(film["FilmName"],"??",film["ActorName"])
            count = count + 1
            if count == 5:
                break
        
        '''
        for index,(film) in enumerate(iterable=films,start=0):
            print(film["FilmName"],"??",film["ActorName"])
            count = count + 1
            if count == 5:
                break
        '''      
        '''
        for index,(key,value) in enumerate(iterable=films,start=10):
            #print(key,"??", fil
            # 1ms[index])
            print(films[index])
            
            count = count + 1
            if count == 5:
                break
        '''
        '''
        for index,key in enumerate(iterable=films,start=10):
            #print(key,"??", fil
            # 1ms[index])
            #print(films[index])
            print(key[index])
            
            count = count + 1
            if count == 5:
                break


        print("index",index)

        '''
        print(count)    
                #if count == 5:
                    #break
                #count = count + 1 

        main() # Return to main() menu                 
       

    elif choice == "2":
        print("Actors")
        print("------")
        actors = view_actors()
               
        for actor in actors:
            month = datetime.datetime.strftime(actor["ActorDOB"],"%B")# convert datetime object to month's full name(%B)
            print(actor["ActorName"],"??",month,"??",actor["ActorGender"])
        
        print("")
        main() # Return to main() menu 

    
    elif choice == "3":
        print("Studios")
        print("-------")
        global studiocount
        global studios
        if studiocount == 0: # runs after the first call
            studios = view_studios() # information are stored in the program variable studios
                
            for studio in studios:# loop trough the studios variable and seperate the dictionaries with column header StudioID and StudioName
                print(studio["StudioID"], "??",studio["StudioName"]) 

            studiocount = studiocount + 1
        else: # runs from the second call onwards
            for studio in studios:# loop trough the studios variable and seperate the dictionaries with column header StudioID and StudioName
                print(studio["StudioID"], "??",studio["StudioName"])

        print("")    
        main() # Return to main() menu 


    elif choice == "4":
        print("Add New Country")
        print("---------------")
        add_country()

        print("") 
        main() # Return to main() menu 

        
    elif choice == "5":
        print("Movies with Subtitles")
        print("---------------------")
        view_movies()
        
        print("")
        main() # Return to main() menu 
        
        
    elif choice == "6":
        print("Add New Movie Script")
        print("--------------------")
        new_movie()
                
        print("")
        main() # Return to main() menu 
        

    elif choice == "x":
        print("choice x")
        exit()
    else:
        display_Menu()
        

def display_Menu():
    print("Movies DB")
    print("---------")
    print("")
    print("MENU")
    print("====")
    print("1 - View Films")
    print("2 - View Actors by Year of Birth & Gender")
    print("3 - View Studios")
    print("4 - Add New Country")
    print("5 - View Movie with Subtitles")
    print("6 - Add New MovieScript")
    print("x - Exit application")





if __name__ == "__main__": # execute only if run from a script
    main() # calls the main program at the start when python start to run
