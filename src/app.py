from flask import *
app = Flask(__name__)

'''
Routers
'''

# Route to index
@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug= True)