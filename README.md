### Run the app

Everything is containerized. So all you need is Docker and Git installed, and then you can run :

```
git clone https://github.com/erayerturk/SwordSec-Challenge-Solution.git
cd SwordSec-Challenge-Solution
docker-compose up --build
```


### Notes

There are 10 consumers in seperated containers. You can change the number of consumers from docker-compose file. Do not forget to change depends-on fields.

When you run compose file in terminal it will print out this number at the end of the progress. If you see this number json file is succesfully created at './output/data.json'
