# CTFDmanage
The provided script is a Python program that interacts with an CTFD. It allows you to perform various operations users such as get, add, modify, and delete.

## General Help
![alt text](https://raw.githubusercontent.com/GuyGuy-59/CTFDmanage/main/pictures/CTFDmanage.png)

## Modules Help
#### GetUsers
Searches for and returns all users.
```sh
CTFD_manage.py -t ctf.local --token YOUR_TOKEN -M GetUsers
```
#### CreateUsers
Adds users with a csv file.
```sh
CTFD_manage.py -t ctf.local --token YOUR_TOKEN -M CreateUsers --path users.csv
```
#### DeleteUsers
Deletes users with a csv file.
```sh
CTFD_manage.py  -t ctf.local --token YOUR_TOKEN -M DeleteUsers --path users.csv
```