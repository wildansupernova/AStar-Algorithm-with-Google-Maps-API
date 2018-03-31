from flask import *
app = Flask(__name__)

'''
Routers
'''

# Route to index
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compute',methods=['POST'])
def compute():
    data  = request.data
    dataDict = json.loads(data)
    return data
if __name__ == '__main__':
    app.run(debug= True)