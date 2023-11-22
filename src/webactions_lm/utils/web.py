import requests
import sys, os, pickle

def read_webpage_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None
    
def cache (_f):
    def wrapper (*args, **kwargs):
        if False == os.path.exists ('.cache'):
            os.makedirs ('.cache')

        filename = f'.cache/{_f.__qualname__}.pkl'
        try:
            with open (filename, 'rb') as file:
                c = pickle.load (file)
                return c [str((args, kwargs))]
        except:
            print ('--- CACHE MISS ---')
            ret = _f (*args, **kwargs)
            c = {}
            if os.path.isfile (filename):
                with open (filename, 'rb') as file:
                    c = pickle.load (file)
            c [str((args, kwargs))] = ret
            with open (filename, 'wb') as file:
                pickle.dump (c, file)
            return ret
    return wrapper

