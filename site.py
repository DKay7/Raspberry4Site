from http.server import BaseHTTPRequestHandler, HTTPServer
import psutil
import json
import os


class ServerHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):

        with open('main.html', 'r') as file:
            self.html_base = file.read()

        with open('status.html', 'r') as file:
            self.html_status = file.read()

        super().__init__(*args, **kwargs)

    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(self.html_base.encode('utf-8'))

        elif self.path.endswith(".gif"):
            self.send_response(200)
            self.send_header('Content-type', 'image/jpg')
            self.end_headers()
            
            with open(os.curdir + os.sep + self.path, 'rb') as file:
                self.wfile.write(file.read())

        elif self.path == "/status":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            self.html_status = self.html_status.format(cpu_t=cpu_temperature(),
                                                       cpu_l=cpu_load(),
                                                       disk_u=disk_space()[0] / 2**30,
                                                       disk_f=disk_space()[1] / 2**30,
                                                       disk_t=disk_space()[2] / 2**30)


            self.wfile.write(self.html_status.encode('utf-8'))

        else:
            self.send_error(404, "Page Not Found {}".format(self.path))

def server_thread(port):
    server_address = ('', port)
    httpd = HTTPServer(server_address, ServerHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()


def cpu_temperature():
    return psutil.sensors_temperatures()['cpu_thermal'][0].current

def disk_space():
    st = psutil.disk_usage(".")
    return (st.used, st.free, st.total)

def cpu_load() -> int:
    return int(psutil.cpu_percent())

def ram_usage() -> int:
    return int(psutil.virtual_memory().percent)


if __name__ == '__main__':
    port = 2020
    print("Starting server at port %d" % port)
    server_thread(port)