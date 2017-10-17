from flask import Flask,render_template,request,jsonify
import datetime
import json
import paho.mqtt.client as mqtt
import time
import random
import cv2
from multiprocessing import Process, Value, Pool, cpu_count
import base64

app = Flask(__name__)


    

@app.route("/ajaxmqtt")
def ajax():
    ip =  request.args.get('ip','192.168.124.88')
    port = int(request.args.get('port'))
    client = request.args.get('client','1')
    topic = request.args.get('topic')
    qos = int(request.args.get('qos'))
    ##使用表單的方式取值
    #ip = request.form['ip']
    #port = int(request.form['port'])
    #client = request.form['client']
    #topic = request.form['topic']
    #qos = int(request.form['qos'])
    print(type(port))
    result = {
      'ip':ip,
      'port':port,
      'client':client,
      'topic':topic,
      'qos':qos
    }
    sendMQTT(result)
    #pool = Pool(2)
    #pool.apply_async(sendMQTT, args=(result,))
    #pool.close()
    #pool.join()

    return jsonify(result=result)
 

def sendMQTT(result):
    ip = result['ip']
    port = result['port']
    client = result['client']
    topic = result['topic']
   
    qos = result['qos']
    def on_connect(pahoClient, obj, flags, rc):

        print("Connected Code =",rc)
        #pahoClient.subscribe(topic)

    def on_publish(pahoClient, packet, mid):
    # Once published, disconnect
        print("Published")
        #pahoClient.disconnect()
    def on_message(pahoClient, userdata, msg):
        print("this topic is:",msg.topic)
        print("this payload is:",str(msg.payload.decode('utf-8')))
        print("this qos is:",msg.qos)    
    mqttc = mqtt.Client() #create new instance
    mqttc.connect(ip,port) #connect to broker
    mqttc.on_connect = on_connect
    mqttc.on_publish = on_publish
    #當接收到訊息時的callback
    mqttc.on_message = on_message
    #已拍照的圖像做傳輸
    #filename = "~~~~~.jpg"
    #image = createImage(filename)
    
    
    mqttc.loop_start()
    while True:
        ran = random.randint(0,10)
        #base64image = convertImageToBase64()
        data = json.dumps({"t":int(time.time()),"w":"rg","l":[{"n":"di1","v":ran},{"n":"di2","v":ran}]})
        mqttc.publish(topic,data,qos=qos)
        time.sleep(1)
    #mqttc.loop_forever()
    #mqttc.loop_stop()
#把圖片傳換成base64格式
def convertImageToBase64():
    with open("../opencvProjects/recogimage.jpg", "rb") as image_file:
        encoded = base64.b64encode(image_file.read())
    return encoded

def createImage(filename):
    camimage = cv2.VideoCapture(0)
    if camimage.isOpened():
        ret, img = camimage.read()
        #此處可能用讀檔的方式,或是有辦法持續傳遞鏡頭的圖像
        bytearray(img)

@app.route('/setting/<name>')
def setting(name):
    now = datetime.datetime.now()
    timeString = now.strftime("%Y-%m-%d %H:%M")
    templateData = {
      'title' : 'HELLO!',
      'time': timeString
    }
    return render_template('hello.html', name=name,**templateData)



if __name__ == "__main__":
    def startWebserver():
        app.run(host='0.0.0.0', debug=True, use_reloader=False)
    startWebserver()
    #app.run(host='0.0.0.0', debug=True) #default port=5000 

