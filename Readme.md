# Copy pasted from my other repo. 
## Things are yet to be changed

# What the package contains

## The tree goes like










+ **Run.py** file only works to run the app and nothing much
+ **__init__**.py is our main file that handles all creation and import and stuff
+ **froms.py** has our forms as before
+ **models.py** has our database info
+ **routes.py** has our routes

- **Static** folder has

    - **anch.jpg, bg.jpg, logo.png** { our static image files used in html pages}

        - **Quick tip** = in flask images only load in if they are kept in the static folder with the css file

    - **main.css** {out stylesheet}

- **Templates** folder has

    - **_formhelpers.html**--> is a macro that loads in the form fields as well as the erros, also the styles and classes are mentioned here if you want to edit them in css

    - **layout.html** --> is a macro basically the block and extend thing and this controls the overall layout and things that are common to every other page

    - **home.html, abouthtml** --> Basic nothing much

    - **signin.html, signup.html** --> our form pages where using the macros in _formhelpers.html we render the form fiels 



- **databse.db** is our databse file from SQLAlchemy