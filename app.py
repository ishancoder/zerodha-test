import cherrypy
import os
import redis
from jinja2 import Environment, FileSystemLoader, select_autoescape
from downloader import download

env = Environment(
    loader=FileSystemLoader(os.path.join(os.getcwd(), 'template')),
    autoescape=select_autoescape(['html', 'xml'])
)

r = redis.StrictRedis()

def get_list(name):
    return list(map(lambda x : x.decode('utf-8'), r.lrange(name, 0, 10)))

def get_data():
    data = zip(get_list('NAME'), get_list('CODE'), get_list('OPEN'), get_list('HIGH'), get_list('LOW'), get_list('CLOSE'))
    return data

def is_expired():
    return r.ttl("NAME") == -2

class BhavCopyData(object):
    @cherrypy.expose
    def index(self):
        if is_expired():
            download()
        template = env.get_template('data_temp.html')
        return template.render(data=get_data())

if __name__ == '__main__':
    conf = {
        '/': {
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/static' : {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'public'
        }
    }
    cherrypy.quickstart(BhavCopyData(), '/', conf)