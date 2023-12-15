# LibraryApplication
My submission of a Library Application.

To use:
1) Edit the "LibraryApplicationBookList.txt" file in the "BookListFile" folder.
	The categories within are separated by commas, and the categories are as follows:
	Book Image Number,
	Book Name,
	Book Description,
	Due Date,
	Has Book Been Borrowed,
	Borrowee First Name,
	Borrowee Last Name,
	Borrowee Email

 	If the value has no data, say the book has not been taken out and so there is no due date,
	then place "N/A" as the value. As you can see there are no spaces between the commas and the
	text around them. Maintain this.

2) Edit the Images within the "BookListAndImages" folder.
	Make sure there are as many images as there are books in the "LibraryApplicationBookList.txt" file.
	If there are 15 books in the "LibraryApplicationBookList.txt" file, then make sure there are 15 images
	named for their respective images rows.
	Make sure they are named accordingly, eg. "1" is the image for book 1.
	If no image is available for a book, copy the "NoBookImageAvailable" image in the
	"NoBookAvailableImage" folder to the "BookListAndImages" folder and rename it to the
	book that has no image, eg. "NoBookImageAvailable" -> "16" (if a 16th book is added)

For the steps above, the program contains pre-done/testing data already implemented so the user can 
run the program immediately to get started.

3) Install Libraries to make sure program works:
   	Libraries installed using Pip were:
   	CustomTKInter: For the GUI
   	Packaging: Dependency for CustomTKInter
   	Pillow: For image manipulation in CustomTKInter

4) Start the Application.
	When starting the application, enter your username and password in their respective boxes, then click
	register. This Registers your username and password within the program, and you will use this again to
	log in. The Login page will have reloaded. Enter the username and password you have just created into
	the relevent boxes and hit the login button.

	The rest of the application is quite simple, to borrow a book, make sure you have clicked on the
	"Available" filter button, then click borrow. Enter the exact name of the book you want to borrow
	and your details (Firstname, Surname, Email). If the details are not correct, or the book is spelled
	wrong, then the book will not be borrowed and you will have to try again.

	Once you are done in the application, click log out to go back to the login page, then exit the program
	using the exit button.
