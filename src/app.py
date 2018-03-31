from flask import *
from Graph import *
from AStar import * 
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
    # Dokumentasi Pemakaian 
    # dataDict erdiri atas 
    # -size (jumlah node yang berarti node dari 0 sampai size-1)
    # -Node (node beserta latitude dan longitude)
    # -adj (ini adalah ajasensi list)
    # -start (start node)
    # -goal (goal node)
    # Berikut contoh json yang dikirimkan
    # {"size":4,"node":[{"latitude":-6.890853531500832,"longitude":107.60832433328301},{"latitude":-6.890821577490572,"longitude":107.61042718515068},{"latitude":-6.892493834467413,"longitude":107.60995511636406},{"latitude":-6.892493834467413,"longitude":107.60822777375847}],"adj":[[2,3],[3],[3,0],[2,1,0]],"start":3,"goal":2}
    # pengaksesan size -> dataDict['size']
    # Pengaksesan node 0 -> dataDict['node'][0]
    # Pengaksesan latitude node 0 -> dataDict['node'][0].latitude atau dataDict['node'][0]['latitude'] dicoba saalah satu seharusnya bisa salah satu
    # Pengaksesan adjasensi list node 0 -> dataDict['adj'][0] (hasil ini adalah list of node, yanng merupakan sisi yang bersisian dengan node 0)
    # Pengaksesan start -> dataDict['start'] , ini adalah node start
    # Pengaksesan goal -> dataDict['goal'] , ini adalah node goal
    
    # Untuk pemakaian di peta/index.html
    # Klik 2 kali pin/marker untuk memasangkan edge atau sisi ke node lain, node yang ingin dipasangkan juga diklik 2 kali
    # Klik 1 kali pin/marker untuk menandai start node
    # Klik kanan 1 kali pin/marker untuk menandai goal Node
    # Klik pada peta untuk menambahkan pin
    # Pastikan semua kondisi diatas terpenuhi sebelum mengirim request

    #Return json
    #-Kalo bisa nanti kembaliannya list of node yang sudah terurut pathnya dari start ke goal, kalo bisa nama key json "path"
    #-Ditambah hitungan jarakanya , klo bisa keynya 'jarak'

    #PS
    #Kalo mau ngecek kembaliannya di console lognya sementara,nanti kalo udah selesai bilang biar aku parse di htmlnya
    #Mangats
    #kalo penjelasan diatas ada yang salah atau error langsung bilang ke aku yak.
    return data
if __name__ == '__main__':
    app.run(debug= True)