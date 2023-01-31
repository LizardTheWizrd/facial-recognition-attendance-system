# Facial Recognition Attendance System

 ## Changelog
 
* [31/01/2023]
  * Added program attribute e.g. BCs, BBIS, etc. in 'student' table
  * Added route to return live attendance list
  * Updated database schema and insertions:
    * Added 'program' attribute to 'student' table
    * Added 'clock_in' attribute to 'attedance' table
 
* [29/01/2023]
  * Added API route to get attendance list for a specific class
  * Updated database schema and insertions:
    * Added 'session_number' attribute to 'session' table
    * Added 'week' attribute added to 'attendance' table for api simplicity
  
* [28/01/2023]
  * Added API route to get class(session) list for a specific teacher

* [08/01/2023]
  * Integrated JWT Authenticaion in flask app
  * Made login route using JWT
  
## Backlog

* Backend/API
  * Attendance list for specific session
    * Calculate and add attendance percentage for a student
    * Count and add number of unexcused absensces for a student
  
  * Starting attendance
    * ~~Add route to return live attendance list~~
    * ~~Add option to pick the week for attendance~~
    * Calculate and add attendance percentage for a student
    
  * Student table
    * ~~Add program attribute e.g. BCs, BBIS, etc.~~
  
  * JWT Authentication
    * Fix issues with token expiration and token refreshes
    * Find where to stash access tokens in frontend\
    
  * Notifications Feature
    * Decide if notifications needs a table 
    * Figure out how to have timed notifications system (do we need request to an API?)
  
  * Admin Portal
    * Add sessions to the database
    * Edit classes information
    * Modify student attendance 
  
* Backend/Facial-Recognition
  * Find reasonable size for dataset or decide who's system to running the tranining file in

