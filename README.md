# Getting started
To setup the necessary environments run "yarn install" and then " yarn create-env " 

# Start the app locally 
 ## Frontend 
 yarn start-client

 ## Backend
 yarn start-api

# Start the app locally using Docker
docker-compose up

 # Test the app
 ## Client
 yarn test-client
 ## API 
 yarn test-api

 # Check lint
 yarn lint

 # Lint everything
 yarn lint:fix

 ## To save something in the db
 export the database you have in the volume and put the content of the sql file into data/init/setup.sql 
 
 Remark: this solution is used because mounting the db ( with .data/db_data:var/lib/mysql in docker-compose.yml in the volume of db) to a local folder data/db_data is an issue because we get too many unuseful files (A DISCUTER SI ON GARDE CA OU ON CHANGE EN ACCEPTANT DAVOIR TOUT EN LOCAL)

 ## enable auto lint file on save 
 File -> preferences -> parameter -> action on save, and add:
```
{
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  },
  "eslint.validate": ["typescript","typescriptreact"]
 }
```
 ### Inspiration and help 
 https://blog.miguelgrinberg.com/post/how-to-dockerize-a-react-flask-project