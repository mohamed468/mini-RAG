from helpers.config import get_settings, Settings
import os
import random, string

class BaseController:
    def __init__(self):
        self.app_settings= get_settings()
        self.base_dir = os.path.dirname(os.path.dirname(__file__)) # هات المسار الخاص بالملف الأساسي ال أنا موجود فيه
        # self.files_dir = self.base_dir + "/" + "assets/files"  دي طريقة, وفي طريقة تانية أحسن
        self.files_dir = os.path.join(
            self.base_dir,
            "assets/files"
        )
    def generate_random_string(self, length : int=12):
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k= length))
    


