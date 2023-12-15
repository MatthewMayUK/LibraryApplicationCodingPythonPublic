#print("Hello World")

import os
import hashlib
import sys
import customtkinter as ctkinter #Using CustomTKInter
import datetime
from datetime import date
from typing import Optional, Tuple, Union
from pathlib import Path
from PIL import Image

libraryApplication = ctkinter.CTk()

#The below sets the Colour themes of the application
ctkinter.set_appearance_mode("dark") 
ctkinter.set_default_color_theme("dark-blue")

libraryApplication.geometry("770x500") #Sets the size of the page in pixels
libraryApplication.title("Library Application") #Sets the name in the Title Bar
libraryApplication.maxsize(770, 500) #Sets the maximum width and height of the program
libraryApplication.minsize(770, 500) #Sets the minimum width and height of the program

#This finds the location of this script file
ThisScriptLocation = Path(__file__).absolute().parent

#Text file for the username and password hashes after salting
UsernameAndPasswordFileLocation = ThisScriptLocation / 'UserNameAndPassword' / 'UsernameAndPassword.txt'

#----------------------------------------------------------------------------------------------

#This takes a number from a filename (eg: 1.png). Used to sort the order of os.listdir() output.
def TakeIntegerFromFileName(Filename): 
    return int(Filename.split('.')[0])

#----------------------------------------------------------------------------------------------

#login: This file is checked for a correct login.
#Registry: This checks the file for FinalOutputStringToFile lines that are the same as the one about to be written to it.
def CheckUserPassHashFile(FinalOutputStringToFile):
    with open(UsernameAndPasswordFileLocation) as UserPassSaltFile:
        UserPassSaltFileContents = UserPassSaltFile.readlines()
    for SaltAndHashLine in UserPassSaltFileContents:
        if FinalOutputStringToFile in SaltAndHashLine:
            return True #Login or Registry duplicate is present
    return False #Not present in file

#----------------------------------------------------------------------------------------------

#This writes the FinalOutputStringToFile to a new line in the file
def WriteUserPassFile(FinalOutputStringToFile):
    UserPassSaltFile = UsernameAndPasswordFileLocation.open("a") #Mode Append
    UserPassSaltFile.write(FinalOutputStringToFile)
    UserPassSaltFile.close()

#----------------------------------------------------------------------------------------------

#This takes in the username and password and creates the final output string for the UsernamePasswordHash file
def UsernamePasswordSaltAndHash(Username, Password):
    CombinedUserPassString = Username + Password #Concatenate the username and password so that it's ready to be hashed.
    Salt = Username + str(len(Password)) #Create a Salt string using the username and the length of the password
    CombinedUserPassSaltString = CombinedUserPassString + Salt #Combined Username, password and salt string ready to be hashed.
    CombinedUserPassSaltStringBytes = bytes(CombinedUserPassSaltString, "utf-8")

    HashedCombinedUserPassSalt = hashlib.sha512(CombinedUserPassSaltStringBytes).hexdigest() #Hash the CombinedUserPassSaltString with sha512 algorithm.

    FinalOutputStringToFile = Salt + "," + HashedCombinedUserPassSalt + "\n" #Write the Salt, then the Hash value, then a newline character to ensure subsequent writes are on a new line.

    return FinalOutputStringToFile

#----------------------------------------------------------------------------------------------    

def LoginLoadingPage(Username, Password): #This is the login function. It doubles as a loading page to prepare for the Book Display Page.

    #This is the background frame
    LoginLoadingFrame = ctkinter.CTkFrame(master = libraryApplication, width = 770, height = 500)
    LoginLoadingFrame.pack(padx = 0, pady = 0, fill = "both", expand = True)

    LoginLoadingHeader = ctkinter.CTkLabel(master = LoginLoadingFrame, text = "Loading...", font = ("Bahnschrift SemiBold", 20)) #Sets the header text, sets its font and size
    LoginLoadingHeader.pack(padx = 10, pady = 10, side = "top") #Places header text at top of frame

    #print("Login")
    #Performs checks here then...

    #Checks if the username or password is blank, if so, immediately fails and reloads the Login page
    if Username == "" or Password == "":
        LoginLoadingFrame.pack_forget()
        LibraryApplicationLoginPage()
        return
    else:
        pass

    FinalOutputStringToFile = UsernamePasswordSaltAndHash(Username, Password) #Use this function using the username and password to salt and hash and then output the result here.

    if CheckUserPassHashFile(FinalOutputStringToFile): #Checks the file for whether it already contains FinalOutputStringToFile
        #print("True") #It is in the file, Login has succeeded.
        LoginLoadingFrame.pack_forget() #Delete this page
        FilterButtonViewAllBooks() #Go to Library book display page via the All Books Filter.
        return
    else:
        #print("False") #It's not in the file, Login has failed
        LoginLoadingFrame.pack_forget() #Delete this Page
        LibraryApplicationLoginPage() #Return to login page
        return

#----------------------------------------------------------------------------------------------

def RegisterLoadingPage(Username, Password): #This is the register function

    #This is the background frame
    RegistryFrame = ctkinter.CTkFrame(master = libraryApplication, width = 770, height = 500)
    RegistryFrame.pack(padx = 0, pady = 0, fill = "both", expand = True)

    RegistryHeader = ctkinter.CTkLabel(master = RegistryFrame, text = "Registering Details", font = ("Bahnschrift SemiBold", 20)) #Sets the header text, sets its font and size
    RegistryHeader.pack(padx = 10, pady = 10, side = "top") #Places header text at top of frame

    #print("Register")
    #Registers new user here...

    #Checks if the username or password is blank, if so, immediately fails and loads the Registry failure page
    if Username == "" or Password == "":
        RegistryFrame.pack_forget()
        RegistryFailurePage()
        return
    else:
        pass

    FinalOutputStringToFile = UsernamePasswordSaltAndHash(Username, Password) #Use this function using the username and password to salt and hash and then output the result here.

    if CheckUserPassHashFile(FinalOutputStringToFile): #Checks the file for whether it already contains FinalOutputStringToFile
        #print("True") #It is in the file, Registration has failed.
        RegistryFrame.pack_forget() #Delete this page
        #As it doesn't work, call ...
        RegistryFailurePage()
        return
    else:
        #print("False") #It's not in the file, Registration can proceed
        WriteUserPassFile(FinalOutputStringToFile)
        RegistryFrame.pack_forget() #Delete this Page
        LibraryApplicationLoginPage()
        return

#----------------------------------------------------------------------------------------------

def RegistryFailurePage():

    #This is the background frame
    RegistryFailureFrame = ctkinter.CTkFrame(master = libraryApplication, width = 770, height = 500)
    RegistryFailureFrame.pack(padx = 0, pady = 0, fill = "both", expand = True)

    RegistryFailureHeader = ctkinter.CTkLabel(master = RegistryFailureFrame, text = "Registry Failed", font = ("Bahnschrift SemiBold", 20)) #Sets the header text, sets its font and size
    RegistryFailureHeader.pack(padx = 10, pady = 10, side = "top") #Places header text at top of frame

    #print("Registry Failed")

    #Button to go back to login page
    LoginButton = ctkinter.CTkButton(master = RegistryFailureFrame, text = "Click to go back to Login Page", command = lambda: (RegistryFailureFrame.pack_forget(), LibraryApplicationLoginPage()))
    LoginButton.pack(padx = 100, pady = 10, fill = "x")

#----------------------------------------------------------------------------------------------

def LogOut(): #This is the Log out function
    #print("Log out")
    
    LibraryApplicationLoginPage()
    return

#----------------------------------------------------------------------------------------------

def ProgramExit(): #This is the Log out function
    #print("Program Exit")
    sys.exit()

#----------------------------------------------------------------------------------------------

#This creates the LibraryApplication Login Page
def LibraryApplicationLoginPage():

    #This is the background frame
    LibraryApplicationLoginFrame = ctkinter.CTkFrame(master = libraryApplication, width = 770, height = 500)
    LibraryApplicationLoginFrame.pack(padx = 0, pady = 0, fill = "both", expand = True)

    LibraryPageHeader = ctkinter.CTkLabel(master = LibraryApplicationLoginFrame, text = "Library Application", font = ("Bahnschrift SemiBold", 40)) #Sets the header text, sets its font and size
    LibraryPageHeader.pack(padx = 10, pady = 10, side = "top") #Places header text at top of frame

    #----------------------------------------------------------------------------------------------
    #These create the login frame and title.
    LoginPageFrame = ctkinter.CTkFrame(master = LibraryApplicationLoginFrame, width = 770, height = 500)
    LoginPageFrame.pack(padx = 10, pady = 10, fill = "both", expand = True)

    LoginPageHeader = ctkinter.CTkLabel(master = LoginPageFrame, text = "Login Page", font = ("Bahnschrift SemiBold", 30)) #Sets the header text, sets its font and size
    LoginPageHeader.pack(padx = 10, pady = 10, side = "top") #Places header text at top of frame

    #Creates the Username entry box
    UserNameEntry = ctkinter.CTkEntry(master = LoginPageFrame, placeholder_text = "Enter Username here")
    UserNameEntry.pack(padx = 100, pady = 10, fill = "x")

    #Creates the Password entry box
    PasswordEntry = ctkinter.CTkEntry(master = LoginPageFrame, placeholder_text = "Enter Password here", show = "*") #shows "*" character instead of user input.
    PasswordEntry.pack(padx = 100, pady = 10, fill = "x")

    #Creates the login button
    LoginButton = ctkinter.CTkButton(master = LoginPageFrame, text = "Click to Login using these details", command = lambda: (LibraryApplicationLoginFrame.pack_forget(), LoginLoadingPage(UserNameEntry.get(), PasswordEntry.get())))
    LoginButton.pack(padx = 100, pady = 10, fill = "x")

    #Creates the Register button
    RegisterButton = ctkinter.CTkButton(master = LoginPageFrame, text = "Click to Register using these details", command = lambda: (LibraryApplicationLoginFrame.pack_forget(), RegisterLoadingPage(UserNameEntry.get(), PasswordEntry.get())))
    RegisterButton.pack(padx = 100, pady = 10, fill = "x")

    #Creates the Exit button
    ExitButton = ctkinter.CTkButton(master = LoginPageFrame, text = "Click to Exit Program", command = ProgramExit)
    ExitButton.pack(padx = 100, pady = 10, fill = "x")

#----------------------------------------------------------------------------------------------

def FilterButtonViewAllBooks(): #Function to see all books in the library

    FilterMode = "All" #Sets the initial filter mode.

    LibraryApplicationBookDisplayPage(FilterMode) #Sends filtermode to the main Book Display page
    return

#----------------------------------------------------------------------------------------------

def FilterButtonAvailableToBorrowBooks(): #Function to see all books available to borrow

    FilterMode = "Available"

    LibraryApplicationBookDisplayPage(FilterMode)
    return

#----------------------------------------------------------------------------------------------

def FilterButtonDueTodayBooks(): #Function to see all books due today

    FilterMode = "DueToday"

    LibraryApplicationBookDisplayPage(FilterMode)
    return

#----------------------------------------------------------------------------------------------

def FilterButtonCurrentlyOnLoanBooks(): #Function to see all books currently on loan

    FilterMode = "OnLoan"

    LibraryApplicationBookDisplayPage(FilterMode)
    return

#----------------------------------------------------------------------------------------------

def BorrowBookFindEditBookDetails(BookName, FirstName, LastName, Email, BookNameList):

    #This is the background frame
    BorrowBookFindEditBookDetailsFrame = ctkinter.CTkFrame(master = libraryApplication, width = 770, height = 500)
    BorrowBookFindEditBookDetailsFrame.pack(padx = 0, pady = 0, fill = "both", expand = True)

    BorrowBookFindEditBookDetailsHeader = ctkinter.CTkLabel(master = BorrowBookFindEditBookDetailsFrame, text = "Borrowing Book....", font = ("Bahnschrift SemiBold", 20)) #Sets the header text, sets its font and size
    BorrowBookFindEditBookDetailsHeader.pack(padx = 10, pady = 10, side = "top") #Places header text at top of frame

    #Checks if the FirstName, LastName or Email is blank, if so, immediately fails and loads the BorrowingBookFailure page
    if FirstName == "" or LastName == "" or Email == "":
        BorrowBookFindEditBookDetailsFrame.pack_forget()
        BorrowingBookFailure(BookNameList)
        return
    else:
        pass

    if "@" in Email:
        if BookName in BookNameList: #If the Book Title is valid, then we can look for it in the Book information file and add our details
        
            LinesInFile = [] #A list to store all lines from the file

            #This finds the location of the file that contains all books
            BookFileLocation = ThisScriptLocation / 'BookListFile' / 'LibraryApplicationBookList.txt'
            BookFile = BookFileLocation.open("r+")
            for line in BookFile: #Reads all lines in the book file
                LinesInFile.append(line) #Add current line to List
                line = line.strip("\n")
                Categories = line.split(",")
                TextFileBookName = Categories[1]

                if BookName == TextFileBookName:
                    TwoWeeks = datetime.timedelta(days = 14)
                    Today = datetime.datetime.today()
                    TwoWeeksFromToday = Today + TwoWeeks
                    NewBookDueDate = str(TwoWeeksFromToday)
                    #Create variables with new borrowee details
                    NewBookBorrowed = "True"
                    NewBookBorroweeFirstName = FirstName
                    NewBookBorroweeLastName = LastName
                    NewBookBorroweeEmail = Email
                    #Assemble final string to be placed in file.
                    FinalLineOutput = Categories[0] + "," + TextFileBookName + "," + Categories[2] + "," + NewBookDueDate[:10] + "," + NewBookBorrowed + "," + NewBookBorroweeFirstName + "," + NewBookBorroweeLastName + "," + NewBookBorroweeEmail + "\n"

                else: #Book not valid. Tell user and return to Book Borrow page.
                    pass
            
            BookFile.close() #Close file.

            BookFile = BookFileLocation.open("w") #Reopen the file with mode "w".This mode deletes the entire file. We'll be rewriting it.
        
            #For each line in the list, if our Book name appears, we replace that line with our FinalLineOutput. If not, then we write the original line back.
            for Line in LinesInFile:
                if BookName in Line:
                    BookFile.write(FinalLineOutput)

                else:
                    BookFile.write(Line)

            BookFile.close() #Close file.
            BorrowBookFindEditBookDetailsFrame.pack_forget()
            LibraryApplicationBookDisplayPage("All")
            return
            
    
        else: #Our Book is not valid. Tell user and return to Book Borrow page.
            BorrowBookFindEditBookDetailsFrame.pack_forget()
            BorrowingBookFailure(BookNameList)
            return
        
    else: #Our Book is not valid. Tell user and return to Book Borrow page.
        BorrowBookFindEditBookDetailsFrame.pack_forget()
        BorrowingBookFailure(BookNameList)
        return

#----------------------------------------------------------------------------------------------
    
def BorrowingBookFailure(BookNameList):

    #This is the background frame
    BorrowBookFailureFrame = ctkinter.CTkFrame(master = libraryApplication, width = 770, height = 500)
    BorrowBookFailureFrame.pack(padx = 0, pady = 0, fill = "both", expand = True)

    BorrowBookFailureHeader = ctkinter.CTkLabel(master = BorrowBookFailureFrame, text = "Borrowing Failed. Please Try Again.", font = ("Bahnschrift SemiBold", 20)) #Sets the header text, sets its font and size
    BorrowBookFailureHeader.pack(padx = 10, pady = 10, side = "top") #Places header text at top of frame

    #Button to go back to the borrow a book page so the user can try again.
    BorrowABookButton = ctkinter.CTkButton(master = BorrowBookFailureFrame, text = "Click to go back to the Book Borrow Page", command = lambda: (BorrowBookFailureFrame.pack_forget(), BorrowABook(BookNameList)))
    BorrowABookButton.pack(padx = 100, pady = 10, fill = "x")

#----------------------------------------------------------------------------------------------

def BorrowABook(BookNameList): #Function called when you click on the borrow a book button next to a book
    
    LibraryApplicationBorrowBookFrame = ctkinter.CTkFrame(master = libraryApplication, width = 770, height = 500)
    LibraryApplicationBorrowBookFrame.pack(padx = 0, pady = 0, fill = "both", expand = True)

    BorrowBookHeader = ctkinter.CTkLabel(master = LibraryApplicationBorrowBookFrame, text = "Library Application", font = ("Bahnschrift SemiBold", 40)) #Sets the header text, sets its font and size
    BorrowBookHeader.pack(padx = 10, pady = 10, side = "top") #Places header text at top of frame

    #Button to go back to the Book Display page
    BookDisplayButton = ctkinter.CTkButton(master = LibraryApplicationBorrowBookFrame, text = "Click to go back to the Book Display Page", command = lambda: (LibraryApplicationBorrowBookFrame.pack_forget(), LibraryApplicationBookDisplayPage("All")))
    BookDisplayButton.pack(padx = 100, pady = 10, fill = "x")

    #A frame to hold the Borrowee Information Entry boxes
    BookBorroweeDetailsFrame = ctkinter.CTkFrame(master = LibraryApplicationBorrowBookFrame, width = 770, height = 500)
    BookBorroweeDetailsFrame.pack(padx = 10, pady = 10, fill = "both", expand = True)
    
    BorrowBookDetailsHeader = ctkinter.CTkLabel(master = BookBorroweeDetailsFrame, text = "Enter your details and the book you wish to borrow:", font = ("Bahnschrift SemiBold", 20)) #Sets the header text, sets its font and size
    BorrowBookDetailsHeader.pack(padx = 10, pady = 10, side = "top") 

    #Entry Boxes for borrowee details 
    BookNameEntry = ctkinter.CTkEntry(master = BookBorroweeDetailsFrame, placeholder_text = "Enter Book Title Here")
    BookNameEntry.pack(padx = 100, pady = 10, fill = "x")

    FirstNameEntry = ctkinter.CTkEntry(master = BookBorroweeDetailsFrame, placeholder_text = "Enter First Name Here")
    FirstNameEntry.pack(padx = 100, pady = 10, fill = "x")

    LastNameEntry = ctkinter.CTkEntry(master = BookBorroweeDetailsFrame, placeholder_text = "Enter Last Name Here")
    LastNameEntry.pack(padx = 100, pady = 10, fill = "x")

    EmailEntry = ctkinter.CTkEntry(master = BookBorroweeDetailsFrame, placeholder_text = "Enter Email Here")
    EmailEntry.pack(padx = 100, pady = 10, fill = "x")

    #Button to save those details to the book they borrowed.
    BorrowButton = ctkinter.CTkButton(master = BookBorroweeDetailsFrame, text = "Click to Borrow Book", command = lambda: (LibraryApplicationBorrowBookFrame.pack_forget(), BorrowBookFindEditBookDetails(BookNameEntry.get(), FirstNameEntry.get(), LastNameEntry.get(), EmailEntry.get(), BookNameList)))
    BorrowButton.pack(padx = 100, pady = 10, fill = "x")

#----------------------------------------------------------------------------------------------

def BookInformationLoading(FilterMode):

    #All lists used throughout this function
    BookImageNumberList = []
    BookNameList = []
    BookDescriptionList = []
    BookDueDateList = []
    BookBorrowedList = []
    BookBorroweeFirstNameList = []
    BookBorroweeLastNameList = []
    BookBorroweeEmailList = []

    BookImagePILList = []

    #----------------------------------------------------------------------------------------------

    #This finds the location of the file that contains all books and finds the location of the book images
    BookFileLocation = ThisScriptLocation / 'BookListFile' / 'LibraryApplicationBookList.txt'
    BookFile = BookFileLocation.open()
    for line in BookFile: #Reads all lines in the book file
        line = line.strip("\n") #Strip the new character line
        Categories = line.split(",") #Split by the exclamation mark
        BookImageNumber = Categories[0] #Grabs the book image number of each respective book from the file

        #Finds and Appends the respective items from the BookList file to their respective category.
        BookName = Categories[1] #Names
        BookDescription = Categories[2] #Description
        BookDueDate = Categories[3] #Due Date
        BookBorrowed = Categories[4] #If the book has been borrowed

        #Details of the borrowee
        BookBorroweeFirstName = Categories[5] 
        BookBorroweeLastName = Categories[6]
        BookBorroweeEmail = Categories[7]

        #----------------------------------------------------------------------------------------------

        #FilterMode is available and book has not been borrowed, so you can borrow it.
        if FilterMode == "Available" and BookBorrowed == "False": #Only in these circumstances do we append the lists with the data.
            BookImageNumberList.append(BookImageNumber)
            BookNameList.append(BookName)
            BookDescriptionList.append(BookDescription)
            BookDueDateList.append(BookDueDate)
            BookBorrowedList.append(BookBorrowed)
            BookBorroweeFirstNameList.append(BookBorroweeFirstName)
            BookBorroweeLastNameList.append(BookBorroweeLastName)
            BookBorroweeEmailList.append(BookBorroweeEmail)

        #FilterMode is DueToday and the book due date is today.
        elif FilterMode == "DueToday" and BookDueDate == str(date.today()): #Only in these circumstances do we append the lists with the data.
            BookImageNumberList.append(BookImageNumber)
            BookNameList.append(BookName)
            BookDescriptionList.append(BookDescription)
            BookDueDateList.append(BookDueDate)
            BookBorrowedList.append(BookBorrowed)
            BookBorroweeFirstNameList.append(BookBorroweeFirstName)
            BookBorroweeLastNameList.append(BookBorroweeLastName)
            BookBorroweeEmailList.append(BookBorroweeEmail)

        #FilterMode is OnLoan and book has been borrowed.
        elif FilterMode == "OnLoan" and BookBorrowed == "True": #Only in these circumstances do we append the lists with the data.
            BookImageNumberList.append(BookImageNumber)
            BookNameList.append(BookName)
            BookDescriptionList.append(BookDescription)
            BookDueDateList.append(BookDueDate)
            BookBorrowedList.append(BookBorrowed)
            BookBorroweeFirstNameList.append(BookBorroweeFirstName)
            BookBorroweeLastNameList.append(BookBorroweeLastName)
            BookBorroweeEmailList.append(BookBorroweeEmail)

        #FilterMode is all. Show all books.
        elif FilterMode == "All": #Only in these circumstances do we append the lists with the data.
            BookImageNumberList.append(BookImageNumber)
            BookNameList.append(BookName)
            BookDescriptionList.append(BookDescription)
            BookDueDateList.append(BookDueDate)
            BookBorrowedList.append(BookBorrowed)
            BookBorroweeFirstNameList.append(BookBorroweeFirstName)
            BookBorroweeLastNameList.append(BookBorroweeLastName)
            BookBorroweeEmailList.append(BookBorroweeEmail)

        else: #Skip book if it doesn't fit in any of the FilterModes. eg. Mode is Available and BookBorrowed is True.
            pass

    #----------------------------------------------------------------------------------------------        

    BookImagesLocation = ThisScriptLocation / 'BookListAndImages' #The folder containing the book images
    BookImagesList = os.listdir(BookImagesLocation) #List all files in the folder
    BookImagesListSorted = sorted(BookImagesList, key = TakeIntegerFromFileName) #Sort the book image names so that they line up to the order in the BookImageNumber list
    BookImageNameNoExtensionIntsList = [] #A list to hold the image png numbers

    #For Numbers of image files in the folder
    for BookImageName in BookImagesListSorted: #For each image name in the sorted list
        BookImageNameNoExtension = BookImageName.strip(".png") #Get rid of the file extension
        BookImageNameNoExtensionInt = int(BookImageNameNoExtension) #Convert the number (a string) to a Int
        BookImageNameNoExtensionIntsList.append(BookImageNameNoExtensionInt) #Append to the list of Image Number Ints.

    #For Numbers in the File. Category[0]
    BookImageNumberIntList = [] #Create a list to hold the Ints of the book image numbers from the file.
    for BookImageNumber in BookImageNumberList: #Loop through the list
        BookImageNumberInt = int(BookImageNumber) #Convert to int
        BookImageNumberIntList.append(BookImageNumberInt) #Append to new list

    BookImageNameIntersectedList = set(BookImageNameNoExtensionIntsList) & set(BookImageNumberIntList) #Intersect the 2 lists and output only the matching values from both lists.

    BookImageStringExtensionList = [] #Create a list to hold the intersected book images with file extensions
    for BookImage in BookImageNameIntersectedList: #For each book image number in the intersected list
        BookImageString = str(BookImage) #Transform the int back to a string
        BookImageStringExtension = BookImageString + ".png" #Re-append the file extension to the number (string).
        BookImageStringExtensionList.append(BookImageStringExtension) #Append the final string to the list

    if FilterMode == "Available":
        BookImagesListLength = len(BookImageNameIntersectedList) #Return value BookImagesListLength is the length of the intersected list

        for BookImageFileName in BookImageStringExtensionList: #For each book image file name in the intersected book images with file extension list
            BookImageFullPath = os.path.join(BookImagesLocation, BookImageFileName) #Get the full path of each file based on its name
            BookImagePIL = Image.open(BookImageFullPath) #Opens the images from their locations as PIL images.
            BookImagePILList.append(BookImagePIL) #Appends these PIL images to the list
    
    elif FilterMode == "DueToday":
        BookImagesListLength = len(BookImageNameIntersectedList) #Return value BookImagesListLength is the length of the intersected list

        for BookImageFileName in BookImageStringExtensionList: #For each book image file name in the intersected book images with file extension list
            BookImageFullPath = os.path.join(BookImagesLocation, BookImageFileName) #Get the full path of each file based on its name
            BookImagePIL = Image.open(BookImageFullPath) #Opens the images from their locations as PIL images.
            BookImagePILList.append(BookImagePIL) #Appends these PIL images to the list

    elif FilterMode == "OnLoan":
        BookImagesListLength = len(BookImageNameIntersectedList) #Return value BookImagesListLength is the length of the intersected list

        for BookImageFileName in BookImageStringExtensionList: #For each book image file name in the intersected book images with file extension list
            BookImageFullPath = os.path.join(BookImagesLocation, BookImageFileName) #Get the full path of each file based on its name
            BookImagePIL = Image.open(BookImageFullPath) #Opens the images from their locations as PIL images.
            BookImagePILList.append(BookImagePIL) #Appends these PIL images to the list

    else:
        BookImagesListSortedFullPathList = [] #Create list of full paths for all the images
        BookImagesListLength = len(BookImagesListSorted) #Get the array length of the entire book images list

        for i in range(BookImagesListLength):
            BookImageFullPath = os.path.join(BookImagesLocation, BookImagesListSorted[i]) #Joins the Images location with the respective Images filename themselves to get a full specific image location
            BookImagesListSortedFullPathList.append(BookImageFullPath) #Appends these full locations to the list

        for i in range(BookImagesListLength):
            BookImagePIL = Image.open(BookImagesListSortedFullPathList[i]) #Opens the images from their locations as PIL images.
            BookImagePILList.append(BookImagePIL) #Appends these PIL images to the list
    
    #Return all these lists as a combined tuple for splitting and usage later.
    return BookImagesListLength, BookImagePILList, BookNameList, BookDescriptionList, BookDueDateList, BookBorrowedList, BookBorroweeFirstNameList, BookBorroweeLastNameList, BookBorroweeEmailList

#----------------------------------------------------------------------------------------------

def LibraryApplicationBookDisplayPage(FilterMode):

    BookInformationLoadingTuple = BookInformationLoading(FilterMode)

    #This is the background frame
    LibraryApplicationBookDisplayFrame = ctkinter.CTkFrame(master = libraryApplication, width = 770, height = 500)
    LibraryApplicationBookDisplayFrame.pack(padx = 0, pady = 0, fill = "both", expand = True)

    LibraryPageHeader = ctkinter.CTkLabel(master = LibraryApplicationBookDisplayFrame, text = "Library Application", font = ("Bahnschrift SemiBold", 40)) #Sets the header text, sets its font and size
    LibraryPageHeader.pack(padx = 10, pady = 10, side = "top") #Places header text at top of frame

    #Creates the Logout button
    LogOutButton = ctkinter.CTkButton(master = LibraryApplicationBookDisplayFrame, text = "Click to Log Out", command = lambda: (LibraryApplicationBookDisplayFrame.pack_forget(), LogOut()))
    LogOutButton.pack(padx = 100, pady = 10, fill = "x")

    #----------------------------------------------------------------------------------------------

    #These create the Book Display frame and title.
    BookDisplayFrame = ctkinter.CTkScrollableFrame(master = LibraryApplicationBookDisplayFrame, width = 770, height = 500) #A scrollable frame
    BookDisplayFrame.pack(padx = 10, pady = 10, fill = "both", expand = True)

    BookDisplayHeader = ctkinter.CTkLabel(master = BookDisplayFrame, text = "Book Display Page", font = ("Bahnschrift SemiBold", 30)) #Sets the header text, sets its font and size
    BookDisplayHeader.pack(padx = 10, pady = 10, side = "top") #Places header text at top of frame

    #----------------------------------------------------------------------------------------------

    BookListDisplayHeader = ctkinter.CTkLabel(master = BookDisplayFrame, text = "List of Books", font = ("Bahnschrift SemiBold", 20)) #Sets the header text, sets its font and size
    BookListDisplayHeader.pack(padx = 10, pady = 10, side = "top") #Places header text at top of frame

    if FilterMode == "Available": #Borrow button should only appear when in the "Available" filter.
        #When clicked, button passes list of Book Names to Borrow a Book Function to use.
        BookBorrowButton = ctkinter.CTkButton(master = BookDisplayFrame, width = 50, text = "Borrow a Book", command = lambda: (LibraryApplicationBookDisplayFrame.pack_forget(), BorrowABook(BookInformationLoadingTuple[2])))
        BookBorrowButton.pack(padx = 10, pady = 10, side = "top")

    #----------------------------------------------------------------------------------------------

    BookListFilterHeader = ctkinter.CTkLabel(master = BookDisplayFrame, text = "Book Filters: (Note: Book Borrow button only available on 'Available to borrow' Filter)", font = ("Bahnschrift SemiBold", 15)) #Sets the header text, sets its font and size
    BookListFilterHeader.pack(padx = 10, pady = 10, side = "top") #Places header text at top of frame
    
    #Creates a frame to hold the filter buttons.
    BookListFilterFrame = ctkinter.CTkFrame(master = BookDisplayFrame, width = 770, height = 50)
    BookListFilterFrame.pack(padx = 10, pady = 10, fill = "both", expand = True)

    #The Filter buttons
    FilterButtonViewAll = ctkinter.CTkButton(master = BookListFilterFrame, text = "All Books", command = lambda: (LibraryApplicationBookDisplayFrame.pack_forget(), FilterButtonViewAllBooks()))
    FilterButtonViewAll.pack(padx = 10, pady = 10, side = "left")

    FilterButtonAvailableToBorrow = ctkinter.CTkButton(master = BookListFilterFrame, text = "Available to Borrow", command = lambda: (LibraryApplicationBookDisplayFrame.pack_forget(), FilterButtonAvailableToBorrowBooks()))
    FilterButtonAvailableToBorrow.pack(padx = 10, pady = 10, side = "left")

    FilterButtonDueToday = ctkinter.CTkButton(master = BookListFilterFrame, text = "Due in Today", command = lambda: (LibraryApplicationBookDisplayFrame.pack_forget(), FilterButtonDueTodayBooks()))
    FilterButtonDueToday.pack(padx = 10, pady = 10, side = "left")

    FilterButtonCurrentlyOnLoan = ctkinter.CTkButton(master = BookListFilterFrame, text = "Currently on Loan", command = lambda: (LibraryApplicationBookDisplayFrame.pack_forget(), FilterButtonCurrentlyOnLoanBooks()))
    FilterButtonCurrentlyOnLoan.pack(padx = 10, pady = 10, side = "left")

    #----------------------------------------------------------------------------------------------

    BookCategoryHolderFrame = ctkinter.CTkFrame(master = BookDisplayFrame, width = 770, height = 50)
    BookCategoryHolderFrame.pack(padx = 10, pady = 10, fill = "x", expand = True)

    BookCategoriesImage = ctkinter.CTkLabel(master = BookCategoryHolderFrame, text = "Image:", font = ("Bahnschrift SemiBold", 10))
    BookCategoriesImage.pack(padx = 10, pady = 10, side = "left")

    BookCategoriesName = ctkinter.CTkLabel(master = BookCategoryHolderFrame, text = "Name of Book:", font = ("Bahnschrift SemiBold", 10))
    BookCategoriesName.pack(padx = 10, pady = 10, side = "left")

    BookCategoriesDescription = ctkinter.CTkLabel(master = BookCategoryHolderFrame, text = "Description:", font = ("Bahnschrift SemiBold", 10))
    BookCategoriesDescription.pack(padx = 10, pady = 10, side = "left")

    BookCategoriesDueDate = ctkinter.CTkLabel(master = BookCategoryHolderFrame, text = "Due Date:", font = ("Bahnschrift SemiBold", 10))
    BookCategoriesDueDate.pack(padx = 10, pady = 10, side = "left")

    BookCategoriesBorrowed = ctkinter.CTkLabel(master = BookCategoryHolderFrame, text = "Borrowed:", font = ("Bahnschrift SemiBold", 10))
    BookCategoriesBorrowed.pack(padx = 10, pady = 10, side = "left")

    BookCategoriesBorroweeFirstNameDetails = ctkinter.CTkLabel(master = BookCategoryHolderFrame, text = "First Name:", font = ("Bahnschrift SemiBold", 10))
    BookCategoriesBorroweeFirstNameDetails.pack(padx = 10, pady = 10, side = "left")

    BookCategoriesBorroweeLastNameDetails = ctkinter.CTkLabel(master = BookCategoryHolderFrame, text = "Last Name:", font = ("Bahnschrift SemiBold", 10))
    BookCategoriesBorroweeLastNameDetails.pack(padx = 10, pady = 10, side = "left")

    BookCategoriesBorroweeEmailDetails = ctkinter.CTkLabel(master = BookCategoryHolderFrame, text = "Email Name:", font = ("Bahnschrift SemiBold", 10))
    BookCategoriesBorroweeEmailDetails.pack(padx = 10, pady = 10, side = "left")

    #----------------------------------------------------------------------------------------------

    #BookInformationLoadingTuple[1][i] accesses the 2nd item in the tuple, a list here, and the i-th item in the list
    for i in range(BookInformationLoadingTuple[0]):

        BookHolderFrame = ctkinter.CTkFrame(master = BookDisplayFrame, width = 770, height = 50)
        BookHolderFrame.pack(padx = 10, pady = 10, fill = "x", expand = True)

        BookImage = ctkinter.CTkImage(BookInformationLoadingTuple[1][i], size = (21, 30))
        BookImageContainer = ctkinter.CTkLabel(master = BookHolderFrame, text = " ", image = BookImage)
        BookImageContainer.pack(padx = 10, pady = 10, side = "left")

        BookName = ctkinter.CTkLabel(master = BookHolderFrame, text = BookInformationLoadingTuple[2][i], font = ("Bahnschrift SemiBold", 10))
        BookName.pack(padx = 10, pady = 10, side = "left")

        BookDescription = ctkinter.CTkLabel(master = BookHolderFrame, text = BookInformationLoadingTuple[3][i], font = ("Bahnschrift SemiBold", 10))
        BookDescription.pack(padx = 10, pady = 10, side = "left")

        BookDueDate = ctkinter.CTkLabel(master = BookHolderFrame, text = BookInformationLoadingTuple[4][i], font = ("Bahnschrift SemiBold", 10))
        BookDueDate.pack(padx = 10, pady = 10, side = "left")

        BookBorrowed = ctkinter.CTkLabel(master = BookHolderFrame, text = BookInformationLoadingTuple[5][i], font = ("Bahnschrift SemiBold", 10))
        BookBorrowed.pack(padx = 10, pady = 10, side = "left")

        BookBorroweeFirstNameDetails = ctkinter.CTkLabel(master = BookHolderFrame, text = BookInformationLoadingTuple[6][i], font = ("Bahnschrift SemiBold", 10))
        BookBorroweeFirstNameDetails.pack(padx = 10, pady = 10, side = "left")

        BookBorroweeLastNameDetails = ctkinter.CTkLabel(master = BookHolderFrame, text = BookInformationLoadingTuple[7][i], font = ("Bahnschrift SemiBold", 10))
        BookBorroweeLastNameDetails.pack(padx = 10, pady = 10, side = "left")

        BookBorroweeEmailDetails = ctkinter.CTkLabel(master = BookHolderFrame, text = BookInformationLoadingTuple[8][i], font = ("Bahnschrift SemiBold", 10))
        BookBorroweeEmailDetails.pack(padx = 10, pady = 10, side = "left")

        #----------------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------------

LibraryApplicationLoginPage() #Starts the program on the Login Page
libraryApplication.mainloop()