# PyHappn

Project is based in https://github.com/rickhousley/happn

## Authentication
### Facebook authentication
Using your favorite web browser, get an access token from Facebook for the registered Happn application:

```
https://www.facebook.com/dialog/oauth?client_id=247294518656661&redirect_uri=https://www.happn.fr&scope=basic_info&response_type=token
```

After the authentication dialog, your browser is redirected by Facebook to the Happn website, and the token is part of the URL displayed in the address bar:

```
https://www.happn.com/en/#access_token=XXXXX&expires_in=5183805
```

You need to create a file named settings.ini inside of pyhappn. Use settings_example.ini as base. Change FB_TOKEN by access_token value.

## Client

### Examples

Like all crossings
```
python cli.py like_all
```

Hidden all crossings
```
python cli.py hidden_all
```

## Updates
### Features not working because of last updates in Happn's API:
- get instagram and facebook of persons
- get credits
