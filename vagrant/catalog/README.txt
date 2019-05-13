This is an application to store items from different categories into a database. The categories are all sports and their respective equipment.
A user may log into the website, using Google oauth2, to add new categories or items. If the user created the item, they may also edit or delete it.

Steps to run the catalog app:
1) Run "vagrant up". Once the virtual machine is running, use "vagrant ssh" to begin using the virtual machine
2) Once in the machine, change directories to /vagrant/catalog and ensure the correct shebang on all python files
3) Run "python databaseSetupCatalog.py" to create the database
4) Run "python lotsofcategories.py" to fill the database with items
5) Run "python catalogApp.py" to start the application
6) Go to "localhost:8000/catalog" to visit the home page of the catalog
7) Hit "Ctrl+C" in the terminal to disconnect
