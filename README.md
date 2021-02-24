### Run the app

Everything is containerized. So all you need is Docker installed, and then you can run :

```
docker-compose up --build
```


### Notes

There are 10 consumers in seperated containers. You can change the number of consumers from docker-compose file. Do not forget to change depends-on fields.

6.json file is broken. There are missing data. I made it valid with 977 users' data. So total number of users 9977. When you run compose file in terminal it will print out this number at the end of the progress. If you see this number json file is succesfully created at './output/data.json'