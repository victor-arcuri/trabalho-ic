import os

class AsciiArtLoader:
    def __init__(self, arts_dir='media/ascii', use_cache=True):
        self.arts_dir = os.path.join(os.path.dirname(__file__), arts_dir)
        self.use_cache = use_cache
        self.cache = {}

    def _load_file(self, file_name):
        path = os.path.join(self.arts_dir, file_name)
        with open(path, 'r', encoding='utf-8') as f:
            return f.readlines()

    def load_art(self, file_name):
        if self.use_cache and file_name in self.cache:
            return self.cache[file_name]
        
        art = self._load_file(file_name)
        
        if self.use_cache:
            self.cache[file_name] = art
        
        return art

    def load_all_arts(self):
        arts = {}
        for file in os.listdir(self.arts_dir):
            if file.endswith('.txt'):
                arts[file] = self.load_art(file)
        return arts

    def list_arts(self):
        return [f for f in os.listdir(self.arts_dir) if f.endswith('.txt')]