
from .template_messages import Template_Messages
from .tokens import Tokens
from .db import DB
from .formats import Format

class Settings():    

    @property
    def tokens(self): return Tokens()
    
    @property
    def admins(self): return [1020541698, 479347949]
    
    @property
    def template_messages(self): return Template_Messages()
    
    @property
    def DB(self): return DB()    

    @property
    def format(self): return Format()

    