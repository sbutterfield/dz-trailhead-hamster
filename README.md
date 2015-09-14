# App to exercise Heroku Connect
![Image of Hammy and GP](media/Tales_of_the_Riverbank.png)

### Local Development

    - cp env.example .env
    - ./hammy


## Deployment
  1. [![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy?template=https://github.com/heroku/hc-hamster)
  2. Provision Connect

    heroku addons:create [herokuconnect|connectqa]:test -a new-app-name
    heroku addons:open [herokuconnect|connectqa] -a new-app-name

  3. Authenticate with Salesforce
  4. Import configuration from config.json
  5. Visit https://dashboard.heroku.com/apps/new-app-name and change to hobby dynos and enable pywriter


### Salesforce

  - Setup new SFDC Org for test harness using connect-team+new-app-name@heroku.com as the email address.
  - Setup network whitelist for 54.0.0.0-55.255.255.255 and others discovered with the following command.
  - curl http://app.herokuapp.com/api/ip
