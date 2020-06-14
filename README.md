# inorbit


## Installation

1) clone this repository 
2) Install django if you don't have it
   
   conda install django
   OR
   pip install django


## Run the server

1) Get to the folder where you downloaded the repository
2) There should be a file: manage.py
3) execute : python manage.py runserver
4) You should see the following text

   Starting development server at http://127.0.0.1:8000/

5) Launch a web browser at http://127.0.0.1:8000/robotConfig/

If it all works you should see a dropdown menu to select the available robots (there are only three loaded)


## Use of the robotConfig app

- You can only select the available robots in the server
- Once you select it you should see the configuration in the text area
- The button 'Save' is disabled unless there is an edition in the text area
- Once the button 'Save' is clicked, the text is verified at the server to see if it is a valid configuration
- If it is valid the robot status text will displayed it was correctly saved
- If not, there is going to be an error message (either not a JSON or a Grammaer Error)
- Another way of accessing the data of the robot is directly going to http://127.0.0.1:8000/robotConfig/robotId/


## Configuration Grammar

- The configuration has to be a JSON
- There can be any number of Modules

      <moduleName1>: <conditions>,
      <moduleName2>: <conditions>,
      ...
          
- conditions can be:
   - Boolean (true or false)
   - A 'compare' expression
   - A 'logic' expression

- A 'compare' expression is formed by the comparison symbol and two elements to be compared
    - The comparison symbols are: 
    
         '$eq', '$gt', '$lt', '$gte', '$lte', '$ne'
    
    - Example: {'$eq': ['battery',50]}

- A 'logic' expression is formed by a logic symbol and one or two elements. The elements can be another 'compare' expression or another nested logic symbol.
     - The logic symbols are:
     
         '$and', '$or', '$not'
         
    - '$and' and '$or' expect two elements. '$not' expect one element
    - if one wants to do an AND or an OR with more than 2 elements, they have to be nested in pairs
    
    - Example:
    
    "$and": [
              { "$eq": ["privacy_mode", 0] },
              { "$ge": ["battery_level", 50] }
            ]
         

## Files to check

- Because Django creates a lot of files, here I provide the list of files where the code of the app is

- /robotConfig/views.py
- /robotConfig/templates/robotConfig/index.html
- /robotConfig/urls.py
- /inorbit/urls.py
- /robotConfig/tests.py (initial unittest; I did not create comprehensive unit or functional tests)

- The configuration JSON files are in /robotConfig/database


## Things to improve

- Unit and functional tests
- Validation on the client side. I started writing a validation javascript, but it required getting the logic written in python translated to javascript.
- It also required capturing the submit event to first validate and then POST the text if it is valid and modify the status results


