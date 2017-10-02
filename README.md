# pastebin_buddy
## Pastebin API control via python3
### DISCLAIMER: This is a beginner project. This module is to be used at your own risk: there is no guarantee that the code is perfect or well optimized.

Here is my take on accessing the Pastebin API using Python 3. This implementation was created with free accounts in mind, and does not support the IP whitelisting features for high-frequency scraping.

It has two dependancies:
  * requests
  * bs4 (BeautifulSoup)

Due to the nature of the API, some functions require additional login information, whilst others can be called with only the unique [developer key](https://pastebin.com/api#1). In this readme I'll label the headers for the functions that do not require additional info with **(BASIC)**.

The PasteManager class has a variable uk (user key) that can be passed to certain functions to make them self-directing. You will see examples of this later.

### Importing and initializing pastebin_buddy (BASIC)
~~~ python
from pastebin_buddy import PasteManager
p = PasteManager(developer_key, username=None, password=None)
~~~

In order for the Pastebin API to be accessed, a PasteManager object must be created and the user must provide their unique [developer key](https://pastebin.com/api#1). **The username and password need not be provided yet, but will be necessary to generate a user key for full functionality if you do not already have one. If you have a user key already, go to "Applying an existing user key".**

### Obtaining a new user key for full functionality 
~~~ python
p.get_user_key(write=True)
~~~

If you didn't provide a username and password earlier, you will be prompted to provide it now. It is required for creating a user key. **You do not have to keep regenerating user keys, they do not expire!** By default, your key is written to a text file (this can be turned off by passing False when calling the function.

### Applying an existing user key (BASIC)
~~~ python
p.set_user_key('user_key')
~~~

If you have a user key, or have generated one before, you do not need to request another one. Call the above function with your user key as an argument and you'll be good to go.

### Creating a new paste anonymously (BASIC)
~~~ python
p.paste_anon(content, syntax=None, title=None, privacy=0, expiry=None)
~~~

This function creates a paste anonymously and so does not need any username or password to do (but you still have to registered!). The arguments are as follows:
  * content: What you want to paste to Pastebin
  * syntax: Pastebin supports format highlighting, you can see what to pass for each text format [here](https://pastebin.com/api#5)
  * title: The title of your paste. Defaults to "Untitled"
  * privacy: 0 = public, 1 = unlisted, 2 = private. If you don't have a paid account, the private setting may not work.
  * expiry: When the paste will expire and disappear. [There are set values for this.](https://pastebin.com/api#6)
 
### Creating a new paste from your account
~~~ python
p.paste(content, syntax=None, title=None, privacy=0, expiry=None)
~~~

This function works the same as paste_anon, however will tie the paste to your account. If you do not have a user key, now is the time to get/set one.

### List the pastes of a user/yourself (Still being tested)
~~~ python
p.list_pastes(target_user_key, results=10)
~~~

This function will return the pastes from a specified Pastebin account. In order for this to work, you'll need *their* user key. The results argument specifies the maximumum number of their pastes to fetch. If you want to fetch your own pastes, simply pass the following (you will need to get/set your user key so the script recognizes it first):

~~~ python
p.list_pastes(p.uk, results=10)
~~~

The return value is in the following format:

~~~ python
>> pastes = p.list_pastes(target_user_key, results=10)
>> pastes
(target_user_key, {'key':'value'}, ...)
~~~

The list_pastes function returns a tuple. The first element contains the key of the target, whether it is you (thus it contains your user key) or someone else (where it will contain their user key). The following elements in the tuple will be dictionaries with the following keys:
  * index: The entry number of the paste. The first paste will be a dictionary of ['index'] = 1, the second will be ['index'] = 2 etc. This is so that referencing a specific paste from the tuple can be done easily by looking at the index and using that number directly.
  * key: The paste key. This will be used in later functions to get the data of the paste.
  * date: Date the paste was posted.
  * title: Title of the paste.
  * size: Size (in characters) of the paste.
  * expiry: Date the paste expires.
  * format-long and format-short: long and short formats (i.e. the format highlighting mentioned earlier).
  * url: The URL of the paste. Usually just the paste key appended onto a pastebin URL.
  * hits: The hits (views) the paste has to date.
  
### List the top 18 trending pastes (BASIC)
~~~ python
p.list_trending()
~~~

This will list the top 18 most trending pastes on Pastebin. The return format of this function is identical to list_pastes above. The first element of the tuple will be 'pastebin'.

### Delete a paste (Still being tested)
~~~ python
p.delete_paste(target_user_key, paste_key)
~~~

Working similar to the list_pastes function, this will allow you to delete a paste using the user key of the author and the paste key of the paste. If you want to delete your own paste, you can do:

~~~ python
p.delete_paste(p.uk, paste_key)
~~~

### Get user info
~~~ python
p.user_info(target_user_key)
~~~

Gets info about the user with the user key target_user_key. If you want to get info about yourself, this can be done once the script recognizes your user key:

~~~ python
p.user_info(p.uk)
~~~

This returns a tuple with two elements. The first element being the user key of whoever was targeted, and the second containing a dictonary of the following:
  * id: Same as the first element- gives the user key.
  * username: Username of the account.
  * user_format_short: Account format.
  * expiration: When the account expires.
  * avatar: URL to the avatar image.
  * privacy: Privacy setting of the account.
  * website: URL to the user website.
  * email: User email address.
  * location: User location.
  * acc-type: Account type.
  
### Getting raw data from a paste (whether public, unlisted or your own private)
~~~ python
p.raw(target_user_key, paste_key)
~~~

The arguments are similar to the delete_paste function, but the function returns a tuple of 3 elements:
  * [0]: target_user_key
  * [1]: paste_key
  * [2]: Raw data from the paste
  
As usual, passing p.uk as target_user_key (and a valid paste_key) will show the raw data from your own pastes.

### Getting raw data from a NON-PRIVATE paste (BASIC)
~~~ python
p.raw_key(paste_key)
~~~

This function returns a two-element tuple.
  * [0]: paste_key
  * [1]: Raw data from the paste.
