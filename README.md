# Python-Twitter-Bot
A twitter bot written in python and using sqlite3 to store needed information
##How to use:
Main.py is used as an example of tweepy and DataManager. Using DataManager for any twitter bots is simple.
When you first initate a database class you can use the default name or enter your own
Example:
```python
dataSample = BotSql("myDatabaseName")
```
If a .db file exists in the directory it will be used as the database without removing any records. Or one will be created. The database used by DataManager has 4 diffrent tables in the database. Below are the tables and their usages
###Using DataManager to store in tables
* Tweets:   Consests of all the tweets the bot has proccessed stored using (Tweet id, id of the person who tweeted it)
  Usage: 
  ```
  add_Tweet(tweetid,userid) #Add a tweet to the Tweets table 
  ```  
  ```
  remove_Tweet(tweetid)     #Remove a tweet from the Tweets table  
  ```  
  ```
  check_Tweet(tweetid)      #Check for a tweet in the Tweets table  
  ```  
  
* Admins:   Consests of all the admins and their information (Twitter user id, admin name, email)
  Usage:
  ```
  add_Admin(userid, name, email) Add an admin by adding them to the Admins table  
  ```  
  ```
  remove_Admin(userid)           Revoke admin privliages from a current admin by removing them from Admins table  
  ```  
  ```
  check_Admin(userid)            Check if a user is an admin by checking the bans table  
  ```  

* Bans:     Consests of a database of all the banned users (Twitter user id, reason for ban)
  Usage:  
  ```
  ban_User(userid, reason = "NONE PROVIDED") Ban a user by adding them to the Bans table (default reason can be changed by replacing NONE PROVIDED)  
  ```  
  ```
  unban_User(userid)                         Unban a user by removing them from the Bans table  
  ```  
  ```
  check_Ban(userid)                          Check if a user is banned by checking the Bans table  
  ```  

* Mentions: Consests of all the processed tweets in the mention timeline. Can be used as a command input for users stores (tweet id,id of the person who tweeted it, command)
  Usage:  
  ```
  add_Mention(tweetid,userid, command = "NONE") Add a tweet to the Mentions table (default command can be changed by replaced NONE)  
  ```  
  ```
  remove_Mention(tweetid)                       Remove a tweet from the Mentions table  
  ```  
  ```
  check_Mention(self,tweetid)                   Check for a tweet in the Mentions table  
  ```  
NOTE that both reason for banning and the command in the Mentions table have default values meaning if you don't want to use them ignore them  
Finally you can get current stats from the database by using get_stats() which returns a string with all the information
