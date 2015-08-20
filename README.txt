Simple app that authenticates user and password against sqlite3 db.

If no matching username and password found, option to create a new login
 is provided.
The New User window will save all the users information to a sqlite3 db
 to be authenticated at next login time.

The app creates a database from two ranks, Scout and Tenderfoot, in regards to boy
 scouts ranks and populates those ranks with tasks that are required to complete
 the rank, acquired from rankData.json located in the ../biglarpourTC/assets folder

As the user finishes each task they can check off the task and save in
 their user status page.

Once all the tasks are complete the app will move on to the next rank,
 may require to use the reload button to move on to the next rank
 if the user finishes all the ranks in one session.

From the user status page you can show all the assets that are pertaining
 to the app by clicking on the show assets button.

Requires python 2.7+

To run the app run the main.py from this folder against python,

ie.
python ../biglarpourTC/main.py
