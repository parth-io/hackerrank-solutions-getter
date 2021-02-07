from pathlib import Path
import getpass
import sys
import json
import requests

class Get:
    base_url = 'https://www.hackerrank.com/'
    login_url = base_url + 'auth/login'
    submissions_url = base_url + 'rest/contests/master/submissions/?offset={}&limit={}'
    challenge_url = base_url + 'rest/contests/master/challenges/{}/submissions/{}'

    def __init__(self):
        self.session = requests.Session()
        self.total_submissions = 0
        self.limit = 500
        self.offset = 0
        self.username = ''
        self.password = ''
        self.headers = {}

    #Get login values
    def get_values(self):
        self.username = input('What is your HackerRank username? ')
        self.password = getpass.getpass('What is your HackerRank password? ')
    
    #Send login values to HackerRank and store session cookiess
    def login(self):
        try:
            resp = self.session.post(self.login_url, auth=(self.username, self.password)#, headers={'user-agent': self.user_agent}) It's conventional to send a User Agent header, but you could just use the default one in requests user-agent = 'requestsx.x.x.'
            data = resp.json()
            if data['status']:
                self.cookies = self.session.cookies.get_dict()
                self.headers = resp.request.headers
            return data['status']
        except Exception as error:
            print(type(error))
            print(error.args)
            print("Error in execution", error)            
    
    #Get the total number of submissions
    def get_number_of_submissions(self):
        if not self.total_submissions:
            total_submissions_url = self.submissions_url.format(0, 500)
            resp = self.session.get(total_submissions_url, headers=self.headers)
            self.total_submissions = resp.json()['total']

    #Get user-defined values for limit and offset, or else use default
    def get_values_limit_offset(self):
        user_limit_and_offset = input('Do you want to start from a specific solution number and/or need a specific number of solutions? Yes/No ' )
        if user_limit_and_offset in ('Y', 'y', 'yes', 'Yes'):
            self.offset = input('Which solution number do you want to start from? ')
            self.limit = input('How many solutions do you need? ')
        else:
            self.limit = self.total_submissions

    # Download a JSON file from HackerRank's API that contains a summary of all your submissions.
    def get_list(self):
        get_list_url = self.submissions_url.format(self.offset, self.limit)
        resp = self.session.get(get_list_url, headers=self.headers)
        data = resp.json()
        models = data['models']
        return models
    
    # Would it better to save the file first, then create an empty file with open()? For example, make the ~/HackerRank/ directory first, then use with open(~/HackerRank/code.java, 'w') to create the file if it does not exist.
    # Save the code to the file
    def save_code_to_path(self, path_to_file, code):
        if not path_to_file.exists():
            path_to_file.mkdir()
        # 'with' statement in Python does not need a try-except block???
        try:
            with open(path_to_file, 'w') as file_to_write_to:
                file_to_write_to.write(code)
        except IOError as error:
            print("I/O Error with \n", path_to_file)
            print(error)            
            
    # Rewrite this whole method, it's way toooo long
    def get_submissions(self, models):
        base_path_to_file = Path.home() / 'Hackerrank' / 'Solutions'
        if not base_path_to_file.exists():
            base_path_to_file.mkdir()
        
        for model in models:
            model_id = model['id']
            challenge_id = model['challenge_id']
            status = model['status']
            language = model['language']
            challenge_name = model['challenge']['name']
            challenge_slug = model['challenge']['slug']
            
            if (status == 'Accepted'):
                challenge_url = self.challenge_url.format(challenge_slug, challenge_id)
                resp = self.session.get(challenge_url, headers=self.headers)
                data = resp.json()['model']
                code = data['code']
                track = data['track']
                
                # Boilerplate code much? Refactor lol
                if language == 'java' or language = 'java8':
                    challenge_file = challenge_name + '.java'
                else if language = 'python':
                    challenge_file = challenge_name + '.py'
                else if language = 'javascript'
                    challenge_file = challenge_name + '.js'
                else:
                    challenge_file = challenge_name + '.txt'
                
                path_to_file = base_path_to_file / challenge_file
                self.save_code_to_path(path_to_file, code)

def main():
    # Instantiation
    getter = Get()
    
    getter.get_values()
    
    if getter.login() is False:
        print('Error in authenticating login')
        sys.exit(1)
        
    getter.get_number_of_submissions()
    
    getter.get_values_limit_offset()
    
    models = getter.get_list()
    
    getter.get_submissions(models)
    
    print('Done with everything')
    sys.exit(0)
    
if __name__ == "__main__":
    main()
