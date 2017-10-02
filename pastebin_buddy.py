import requests
from bs4 import BeautifulSoup

class PasteManager:
    
    dk = None   #developer key
    uk = None   #user key
    un = None   #user name
    pw = None   #user password
    PASTE_PATH = 'https://pastebin.com/api/api_post.php'
    LOGIN_PATH = 'https://pastebin.com/api/api_login.php'
    RAW_PATH = 'https://pastebin.com/api/api_raw.php'

    def __init__(self, dev_key, username=None, password=None):
        self.dk = dev_key
        self.un = username
        self.pw = password

    def paste_anon(self, content, syntax=None, title=None, privacy=0, expiry=None):
        params = {
                'api_dev_key':self.dk,
                'api_option':'paste',
                'api_paste_code':content,
                'api_paste_format':syntax,
                'api_paste_name':title,
                'api_paste_private':privacy,
                'api_paste_expire_date':expiry
                }

        r = requests.post(url = self.PASTE_PATH, data = params)
        print(f'Pasted {title} anonymously at {r.text}')

    def paste(self, content, syntax=None, title=None, privacy=0, expiry=None):
        if(self.uk==None):
            print('No user key defined! Please get_user_key(username, password) or set_user_key(user_key)')
        else:
            params = {
                    'api_user_key':self.uk,
                    'api_dev_key':self.dk,
                    'api_option':'paste',
                    'api_paste_code':content,
                    'api_paste_format':syntax,
                    'api_paste_name':title,
                    'api_paste_private':privacy,
                    'api_paste_expire_date':expiry
                    }

            r = requests.post(url = self.PASTE_PATH, data = params)
            print(f'Pasted {title} as {self.uk} at {r.text}')

    def get_user_key(self, write = True):
        if(self.un==None):
            self.un = input('Username: ')
        if(self.pw==None):
            self.pw = input('Password: ')
        params = {
                'api_dev_key':self.dk,
                'api_user_name':self.un,
                'api_user_password':self.pw
                }

        r = requests.post(url = self.LOGIN_PATH, data = params)
        print(f'Result: {r.text}. User keys can be reused next time with set_user_key(). Write to file is {write} (def. True).')
        self.uk = r.text

        if(write):
            output = open(f'User key for {self.un}.txt', 'w')
            output.write(self.uk)
            output.close()

    def set_user_key(self, user_key):
        self.uk = user_key
        print(f'User key set as {self.uk}')


    def parse_paste_list(self, listing):
        parent = listing[0]
        paste = listing[1]
        soup = BeautifulSoup(paste,'html.parser')
        paste_collection = soup.find_all('paste')
        content = [parent]

        for i, item in enumerate(paste_collection):
            paste_entity = {
                            'index':i+1,
                            'key':item.find('paste_key').get_text(),
                            'date':item.find('paste_date').get_text(),
                            'title':item.find('paste_title').get_text(),
                            'size':item.find('paste_size').get_text(),
                            'expiry':item.find('paste_expire_date').get_text(),
                            'format-long':item.find('paste_format_long').get_text(),
                            'format-short':item.find('paste_format_short').get_text(),
                            'url':item.find('paste_url').get_text(),
                            'hits':item.find('paste_hits').get_text()
                            }
            content.append(paste_entity)

        return tuple(content)

    def parse_user_info(self, listing):
        parent = listing[0]
        detail = listing[1]
        soup = BeautifulSoup(detail,'html.parser')
        content = [parent]

        for item in soup.find_all('user'):
            paste_entity = {
                            'id':parent,
                            'username':item.find('user_name').get_text(),
                            'user_format_short':item.find('user_format_short').get_text(),
                            'expiration':item.find('user_expiration').get_text(),
                            'avatar':item.find('user_avatar_url').get_text(),
                            'privacy':item.find('user_private').get_text(),
                            'website':item.find('user_website').get_text(),
                            'email':item.find('user_email').get_text(),
                            'location':item.find('user_location').get_text(),
                            'acc-type':item.find('user_account_type').get_text()
                            }
            content.append(paste_entity)

        return tuple(content)

    def list_pastes(self, target_user, results):
        params = {
                'api_dev_key':self.dk,
                'api_user_key':target_user,
                'api_results_limit':results,
                'api_option':'list'
                }

        r = requests.post(url = self.PASTE_PATH, data = params)
        result = (target_user, r.text)
        return self.parse_paste_list(result)

    def list_trending(self):
        params = {
                'api_dev_key':self.dk,
                'api_option':'trends'
                }

        r = requests.post(url = self.PASTE_PATH, data = params)
        result = ('pastebin', r.text)
        return self.parse_pastes(result)

    def delete_paste(self, target_user, paste_key):
        params = {
                'api_dev_key':self.dk,
                'api_user_key':target_user,
                'api_paste_key':paste_key,
                'api_option':'delete'
                }

        r = requests.post(url = self.PASTE_PATH, data = params)
        print(r.text)

    def user_info(self, target_user):
        params = {
                'api_dev_key': self.dk,
                'api_user_key': target_user,
                'api_option': 'userdetails'
                }

        r = requests.post(url = self.PASTE_PATH, data = params)
        result = (target_user, r.text)
        return self.parse_user_info(result) 

    def raw(self, target_user, paste_key):
        params = {
                'api_dev_key': self.dk,
                'api_user_key': target_user,
                'api_paste_key': paste_key,
                'api_option': 'show_paste'
                }

        r = requests.post(url = self.RAW_PATH, data = params)
        return (target_user, paste_key, r.text)

    def raw_key(self, paste_key):
        r = requests.get(f'https://pastebin.com/raw/{paste_key}')
        
        return (paste_key, r.text)
