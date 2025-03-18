from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")  # Bot toek
ADMINS = env.list("ADMINS")  # adminlar ro'yxati
IP = env.str("ip")  
