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