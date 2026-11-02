from network import WLAN
import socket
import time
import gc

gc.collect()

class TCPServer:
    def __init__(self, wifi_ssid, wifi_pass, connect, port, timeout = .1):
        self.wifi_ssid = wifi_ssid
        self.wifi_pass = wifi_pass
        self.connect = connect
        self.port = port
        
        if connect:
            mode = WLAN.IF_STA
        else:
            mode = WLAN.IF_AP
        
        self.wlan = WLAN(mode)
        self.wlan.active(True)
        
        if connect:
            self.wlan.connect(wifi_ssid, wifi_pass)
            while not self.wlan.isconnected():
                time.sleep(.1)
        else:
            self.wlan.config(essid = wifi_ssid, password = wifi_pass, authmode = 3)
        
        self.addr = (self.wlan.ifconfig()[0], port)
        
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.settimeout(timeout)
        self.server.bind(("0.0.0.0", port))
        self.server.listen(5)
        self.client = None

    def connect_wifi(self):
        if not self.wlan.isconnected() and self.connect:
            self.wlan.connect(self.wifi_ssid, self.wifi_pass)

            while not self.wlan.isconnected():
                time.sleep(1)

        return self.wlan.isconnected()
    
    def accept(self):
        try:
            client, addr = self.server.accept()
            
            self.client = client
            
            return addr
        except Exception as e:
            print(e)
    
    def recv(self):
        try:
            if self.client is not None:
                text = self.client.recv(1024).decode()
                
                return text

        except Exception as e:
            print(e)
            
    def send(self, tex):
        try:
            if self.client is not None:
                self.client.send(text.encode())

        except Exception as e:
            print(e)
    
    def sendall(self, text):
        try:
            if self.client is not None:
                self.client.sendall(text.encode())
        except Exception as e:
            print(e)
    
    def close(self):
        if self.client is not None:
            self.client.close()
            self.client = None

class TCPClient:
    def __init__(self, wifi_ssid, wifi_pass, connect, port, timeout = .1):
        self.wifi_ssid = wifi_ssid
        self.wifi_pass = wifi_pass
        self.connect = connect
        self.port = port
        
        if connect:
            mode = WLAN.IF_STA
        else:
            mode = WLAN.IF_AP
        
        self.wlan = WLAN(mode)
        self.wlan.active(True)
        
        if connect:
            self.wlan.connect(wifi_ssid, wifi_pass)
            while not self.wlan.isconnected():
                time.sleep(.1)
        else:
            self.wlan.config(essid = wifi_ssid, password = wifi_pass, authmode = 3)
        
        self.addr = (self.wlan.ifconfig()[0], port)

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.settimeout(timeout)

    def connect_wifi(self):
        if not self.wlan.isconnected() and self.connect:
            self.wlan.connect(self.wifi_ssid, self.wifi_pass)

            while not self.wlan.isconnected():
                time.sleep(.1)

        return self.wlan.isconnected()

    def connect(self, addr):
        try:
            self.client.connect(addr)
            return True
        except Exception as e:
            print(e)
            return False

    def recv(self):
        try:
            if self.client is not None:
                text = self.client.recv(1024).decode()
                
                return text
                
        except Exception as e:
            print(e)

    def send(self, text):
        try:
            if self.client is not None:
                self.client.send(text.encode())

        except Exception as e:
            print(e)
    
    def sendall(self, text):
        try:
            if self.client is not None:
                self.client.sendall(text.encode())
        except Exception as e:
            print(e)

    def close(self):
        self.client.close()

class UDPSocket:
    def __init__(self, wifi_ssid, wifi_pass, connect, port, timeout):
        self.wifi_ssis = wifi_ssid
        self.wifi_pass = wifi_pass
        self.port = port
        
        if connect:
            mode = WLAN.IF_STA
        else:
            mode = WLAN.IF_AP
        
        self.wlan = WLAN(mode)
        self.wlan.active(True)
        
        if connect:
            self.wlan.connect(wifi_ssid, wifi_pass)
            while not self.wlan.isconnected():
                time.sleep(.1)
        else:
            self.wlan.config(essid = wifi_ssid, password = wifi_pass, authmode = 3)
        
        self.addr = self.wlan.ifconfig()[0]
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.settimeout(timeout)
        self.sock.bind(("0.0.0.0", port))
    
    def connect_wifi(self):
        if not self.wlan.isconnected() and self.connect:
            self.wlan.connect(self.wifi_ssid, self.wifi_pass)

            while not self.wlan.isconnected():
                time.sleep(.1)

        return self.wlan.isconnected()
    
    def send(self, text, receiver, byte = False):
        if byte:
            self.sock.sendto(text, (receiver, self.port))
        else:
            self.sock.sendto(text.encode(), (receiver, self.port))
    
    def recv(self, byte = False):
        try:
            text, addr = self.sock.recvfrom(1024)
        except:
            return
        
        if byte:
            return (text, addr[0])
        else:
            return (text.decode(), addr[0])
