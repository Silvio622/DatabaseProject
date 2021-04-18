

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
    #print(films)


# Menu 2 View Actors by Year of Birth & Gender
def view_actors():
    
    birthyear = int(input("Year of Birth :"))
    
    if birthyear >= 1913 and birthyear <= 1994:
        strbirthyear = str(birthyear)
    else:
        view_actors() 
      
    while True:
        gender = input("Gender (Male/Female) :")

        if gender == "Male" or gender == "Female":
            global conn # make the variable "conn" global to see it in all functions
            conn = pymysql.connect(host="localhost", user="root", password="root", port=3306, db="moviesdb", cursorclass=pymysql.cursors.DictCursor)

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
        #print("No Connection")
        connect() # call the connect function to connect to the database 
    #else:
        #print("Already Connected") 

    query = "SELECT * FROM studio ORDER BY StudioID " # database query Select all rows from table teacher where the column experience < %s is the placeholder              

    with conn: # close the connection
        cursor = conn.cursor() # this returns a cursor object
        cursor.execute(query) # execute the query variable and pass in "number" in the placeholder %s. number comes from the parameter what is passed in in the function
        studios = cursor.fetchall() # create a variable with returns all rows from the database into it
        #print(studios)# to show all the rows
        return studios
        #conn.close() # close connection
    '''
    for studio in studios:# loop trough the studios varaible and seperate the dictionaries with column header StudioID and StudioName
        print(studio["StudioID"], "|",studio["StudioName"])
        studio["StudioID"], "|",studio["StudioName"]
    '''  


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
    #display_Menu()

myclient = None

def mongo_connect():
    global myclient
    print("In mongo_connect()")
    print("1",myclient)
    myclient = pymongo.MongoClient(host="localhost",port=27017) # connect to the Mongo deamon
    print("2",myclient)
    myclient.admin.command("ismaster")
    
    


def mongo_find():
    #filmlist = []
    
    db = myclient["movieScriptsDB"]# call the database
    docs = db["movieScripts"]# call the collection/table
    
    querymongo = {"subtitles": subtitle}# read out the attribute "subtitle" in the Mongo database collection
    dbsubtitles = docs.find(querymongo)
    
    print(dbsubtitles)

    for sub in dbsubtitles:
        #print(s["keywords[]"],"|",s["subtitles[]"])
        print(sub["_id"])
        moviesid = []
        moviesid = sub["_id"]
        print (moviesid)
        
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
            #filmlist = filmlist.append(film["FilmName"],"¦",film["FilmSynopsis"])
            #filmlist = filmlist.append(film)
            #print(filmlist)
            print(film["FilmName"],"¦",film["FilmSynopsis"][0:30])# print only a length of 30 string characters

    '''
    for ids in moviesid:                       
        if not conn:
            connect() # call the connect function to connect to the SQL database 
        
        querysql = "SELECT FilmName, FilmSynopsis FROM film WHERE FilmId = %s "

        with conn: # close the connection
                    cursor = conn.cursor() # this returns a cursor object
                    cursor.execute(querysql,(ids))  # execute the query variable and pass in "number" in the placeholder %s. number comes from the parameter what is passed in in the function
                    #cursor.execute(querysql,(moviesid))  # execute the query variable and pass in "number" in the placeholder %s. number comes from the parameter what is passed in in the function
                    films = cursor.fetchall() # create a variable with returns all rows from the database into it

        for film in films:
            print(film["FilmName"],"¦",film["FilmSynopsis"])
    '''

    '''
    mydb = myclient["w10"]# create a variable "mydb" connecto the the database "w10"
    docs = mydb["docs"]# create a variable docs and put in the collection/table docs from w10 database
    query = {"address":"Dublin"} # importent to put the column "address" in quotation marks otherwise we get an error
    poeple = docs.find(query)# cretae a variable poeple and put in the docs.find method and put in the query variable
    print (poeple)
    for p in poeple: # loops through the variable poeple and print out every element(database intry) 
        print(p["name"],"|",p["age"])# type in the column name and age only 
       # print(p["name"],"|",int(p["age"]))# type in the column name and age only but convert the age to an integer 5
    '''

# Menu 5 View Movies with Subtitles
def view_movies():
    global subtitle
    subtitle = input("Enter subtitle language: ")
    if subtitle == "":
        view_movies()
        print(subtitle)
         
    else:
        if not myclient:# if no connections are made
            try:
                mongo_connect()# connect to the database
                mongo_find()
            except Exception as e:
                print("Error", e)

        #print("choice 5")

# Menu 6 Add New Movie Script
def new_movie():
    #try:
        #newmovieid = int(input("ID : "))
    #except ValueError:
        #new_movie()
    newmovieid = input("ID : ")
    if newmovieid == str:
        new_movie()
    else:
        newmovieid = int(newmovieid)
    
    print("choice 6")
    print("moviesid")


        


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
        #display_Choice()
        main()
        #display_Menu()

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
            print(film["FilmName"],"¦",film["ActorName"])
            count = count + 1
            if count == 5:
                break
        '''

        for index,film in enumerate(iterable=films,start=10):
            print(film["FilmName"],"¦",film["ActorName"])
            count = count + 1
            if count == 5:
                break
        
        '''
        for index,(film) in enumerate(iterable=films,start=0):
            print(film["FilmName"],"¦",film["ActorName"])
            count = count + 1
            if count == 5:
                break
        '''      
        '''
        for index,(key,value) in enumerate(iterable=films,start=10):
            #print(key,"¦", fil
            # 1ms[index])
            print(films[index])
            
            count = count + 1
            if count == 5:
                break
        '''
        '''
        for index,key in enumerate(iterable=films,start=10):
            #print(key,"¦", fil
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
            print(actor["ActorName"],"¦",month,"¦",actor["ActorGender"])
        
        print("")
        #display_Menu()
        main() # Return to main() menu 

    
    elif choice == "3":
        print("Studios")
        print("-------")
        global studiocount
        global studios
        if studiocount == 0: # runs after the first call
            studios = view_studios() # information are stored in the program variable studios
                
            for studio in studios:# loop trough the studios variable and seperate the dictionaries with column header StudioID and StudioName
                print(studio["StudioID"], "¦",studio["StudioName"]) 

            studiocount = studiocount + 1
        else: # runs from the second call onwards
            for studio in studios:# loop trough the studios variable and seperate the dictionaries with column header StudioID and StudioName
                print(studio["StudioID"], "¦",studio["StudioName"])
            
        main() # Return to main() menu 

    elif choice == "4":
        print("Add New Country")
        print("---------------")
        add_country()
        main() # Return to main() menu 
        
    elif choice == "5":
        print("Movies with Subtitles")
        print("---------------------")
        view_movies()
        #display_Menu()
        main() # Return to main() menu 
        
    elif choice == "6":
        print("Add New Movie Script")
        print("--------------------")
        new_movie()
        

    elif choice == "x":
        print("choice x")
        exit()
    else:
        display_Menu()
        #main() # Return to main() menu 

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
