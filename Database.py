

import pymysql
import datetime


conn = None #create a variable for the connection to the MySQL database set to None for default


# Connection to the datbase
def connect():# makes a connection to a database
    global conn # make the variable "conn" global to see it in all functions
    conn = pymysql.connect(host="localhost", user="root", password="root", port=3306, db="moviesdb", cursorclass=pymysql.cursors.DictCursor)

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
    #print("choice 3")
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
    '''
    for studio in studios:# loop trough the studios varaible and seperate the dictionaries with column header StudioID and StudioName
        print(studio["StudioID"], "|",studio["StudioName"])
        studio["StudioID"], "|",studio["StudioName"]
    '''   


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
        print("choice 1")

    elif choice == "2":
        print("Actors")
        print("------")
        actors = view_actors()
               
        for actor in actors:
            month = datetime.datetime.strftime(actor["ActorDOB"],"%B")# convert datetime object to month's full name(%B)
            print(actor["ActorName"],"¦",month,"¦",actor["ActorGender"])
        
        print("")
        display_Menu()

    elif choice == "3":
        print("Studios")
        print("-------")
        studios = view_studios()
                
        for studio in studios:# loop trough the studios varaible and seperate the dictionaries with column header StudioID and StudioName
            print(studio["StudioID"], "¦",studio["StudioName"]) 
        
    elif choice == "4":
        print("choice 4")
    elif choice == "5":
        print("choice 5")
    elif choice == "6":
        print("choice 6")
    elif choice == "x":
        print("choice x")
        exit()


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
