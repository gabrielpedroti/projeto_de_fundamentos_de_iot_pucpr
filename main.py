from wifi_lib import conecta
import urequests
import dht
import machine
import time
import network

#Pinos para controle do DHT e relé
dht_sensor = dht.DHT11(machine.Pin(4))
PIN_RELAY = machine.Pin(2, machine.Pin.OUT)

#Dados para envio ao thingspeak
API_WRITE_KEY = "7JVW6ZSIZXPUFXIA"
THINGSPEAK_URL = "http://api.thingspeak.com/update"

#Coleta de dados do sensor DHT
def read_dht():
    dht_sensor.measure()
    temp = dht_sensor.temperature()
    umidade = dht_sensor.humidity()
    return temp, umidade

#Controle do relé
def control_relay(temp, umidade):
    if temp > 31 or umidade > 70:
        PIN_RELAY.value(1)  #Liga o relé
    else:
        PIN_RELAY.value(0)  #Desliga o relé
        
#Envio de dados para o thingspeak
def send_to_thingspeak(temp, umidade):
    payload = "api_key={}&field1={}&field2={}".format(API_WRITE_KEY, temp, umidade)
    response = urequests.post(THINGSPEAK_URL, data=payload)
    response.close()
    urequests.get("http://api.thingspeak.com/clear_cache")

#Conecta à rede Wi-Fi
def main():
    print("Conectando a rede...")
    station = conecta("GED_WIFI", "mesmasenha")
    if not station.isconnected():
        print("Não conectado")
        return
    
    print("Conectado!")
    
    while True:
        #Leitura do sensor DHT11
        temp, umidade = read_dht()
        #Envia os dados para o ThingSpeak
        send_to_thingspeak(temp, umidade)
        #Controle do relé
        control_relay(temp, umidade)
        #Imprime os dados
        print("Enviando dados para o servidor...\nTemperatura: {}ºC - Umidade: {}%".format(temp, umidade))
        #Tempo a cade leitura/envio de dados
        time.sleep(5)

if __name__ == "__main__":
    main()
