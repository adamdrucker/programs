from bottle import Bottle, run, static_file, template

# create an instance of Bottle
app = Bottle()


# bind function to the 'root route'
@app.route('/')
def index():
    return template('index', name="Adam")


# bind function to the route '/hello'
@app.route('/hello')
def hello():
    return "Hello!"


# this function serves the specified image from
# the specified root directory
# the trick being you need to request to exact file name
# ex: 'dskt01.png'
@app.route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root='/home/adam/Pictures')





# run the app listening on port 8888
# http://localhost:8888
run(app, host='localhost', port=8888, reloader=True)

