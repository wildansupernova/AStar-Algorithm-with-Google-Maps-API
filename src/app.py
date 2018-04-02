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
    print(dataDict)

    # get nodes from dataDict
    nodeList = []
    edgeList = []
    # create Graph
    G = Graph(nodeList, edgeList)
    
    # create and add nodes from dataDict to nodeList
    for i in range (0, len(dataDict['node'])):
        N = LocationNode(i, dataDict['node'][i]['longitude'], dataDict['node'][i]['latitude'])
        G.nodeList.append(N)
        i += 1
    
    # create and add edges from dataDict to edgeList
    for i in range (0, len(dataDict['adj'])):
        firstNode = G.nodeList[i]
        for j in range (0, len(dataDict['adj'][i])):
            if dataDict['adj'][i][j] > i:
                secondNode = G.nodeList[dataDict['adj'][i][j]]
                E = WeightedEdge(firstNode, secondNode, HarversineDistance(firstNode, secondNode))
                G.edgeList.append(E)

    # set edge list to solve
    SetEdgeList(G.edgeList)
    # set heuristic distance func for A* shortest path algorithm
    SetHeuristicDistanceFunc(HarversineDistance)
    # get solution path
    solution = GetShortestPath(G.nodeList[dataDict['start']], G.nodeList[dataDict['goal']])
    path, cost = solution

    # cast list of nodes in path into only its node indices
    pathNodeIdx = []
    for node in path:
        pathNodeIdx.append(node.value)
    # for node in pathNodeIdx:
    #     print(node)
    # print(cost)

    # get solution as a dictionary with key path and cost
    solutionDict = {
        'path' : pathNodeIdx,
        'cost' : cost
    }

    # convert the solution dictionary to json to be returned
    solutionJson = json.dumps(solutionDict)
    print(solutionJson)
    # Untuk pemakaian di peta/index.html
    # Klik 2 kali pin/marker untuk memasangkan edge atau sisi ke node lain, node yang ingin dipasangkan juga diklik 2 kali
    # Klik 1 kali pin/marker untuk menandai start node , warna akan berubah menjadi ungu
    # Klik kanan 1 kali pin/marker untuk menandai goal Node , warna akan berubah menjadi kuning , yang ini sabar agak lama
    # Klik pada peta untuk menambahkan pin
    # Pastikan semua kondisi diatas terpenuhi sebelum mengirim request

    #Return json
    #-Kalo bisa nanti kembaliannya list of node yang sudah terurut pathnya dari start ke goal, kalo bisa nama key json "path"
    #-Ditambah hitungan jarakanya , klo bisa keynya 'jarak'

    #PS
    #Kalo mau ngecek kembaliannya di console lognya sementara,nanti kalo udah selesai bilang biar aku parse di htmlnya
    #Mangats
    #kalo penjelasan diatas ada yang salah atau error langsung bilang ke aku yak.
    
    return solutionJson

if __name__ == '__main__':
    app.run(debug= True)