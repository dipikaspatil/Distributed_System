#!/usr/bin/python3

import socket
import time
import os
import mimetypes
from _thread import *
import threading

'''
Informative commands/information  - 

wget http://g7-08:48353/test.html
wget --save-headers http://g7-08:48353/test.html
wget --server-response http://g7-08:48353/test.html
wget --limit-rate=100k http://10.33.1.8:60331/skype-ubuntu-precise_4.3.0.37-1_i386.deb
wget --server-response http://g7-08:48353/test.html

g7-08 - server host name
48353 - server port number
test.html - requested file

HTTP request message format 
GET /bar.html HTTP/1.1
Host: www.foo.com
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:28.0) Gecko/20100101 Firefox/28.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Connection: keep-alive


HTTP respoonce message format

HTTP/1.1 200 OK
Date: Thu, 02 Apr 2015 01:51:49 GMT
Server: Apache / 2.2.16(Debian)
Last - Modified: Tue, 10 Feb 2015 17: 56:15 GMT
Accept - Ranges: bytes
Content - Length: 2693
Content - Type: text / html
'''

'''
http server accepts GET request 

http_server class has below functions - 
start_server() - this function - creates new socket for server , bind it with OS selected port number 
               and listen client connection then it call wait_for_client()
               
wait_for_client() - this function - accepts client request and creates new thread and handover processing of client 
                  request to new thread by passing function process_request() and parameters in tuple form
                  
process_request() - this function - process actual client request i.e. GET request and create response message and then
                    call sends response to client and closes the client request               
'''


class http_server:
    file_info_dictionary = {}  # to check number of times particular client request is processed
    print_lock = threading.Lock()

    '''
    this function - creates new socket for server , bind it with OS selected port number 
    and listen client connection then it call wait_for_client()
    '''

    def start_server(self):
        # if www folder does not exist then we can return with message
        if not (os.path.isdir("./www")):
            print("www directory not found on server side...")
            return
        # create socket
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #print("socket created successfully at server side")
        except socket.error as err:
            print("socket creation failed at server side ", err)
            return

        # Next bind to the port
        # we have inputted an empty string
        # this makes the server listen to requests
        # coming from other computers on the network

        self.s.bind(("", 0))  # bind takes one argument as tuple and binds port with ip
        # backlog connection - here 6 connections are kept waiting if the server is busy ..if a 6th socket trys to connect then the connection is refused.
        self.s.listen(6)

        print("Server Host Name is - ", socket.gethostname())
        print("Server IP address (Host Address) is - ", socket.gethostbyname(socket.gethostname()))
        print("Server Port is - ", self.s.getsockname()[1])
        self.wait_for_client()

    '''
    this function - accepts client request and creates new thread and handover processing of client 
    request to new thread by passing function process_request() and parameters in tuple form
    '''

    def wait_for_client(self):
        while True:
            # accept function call return client information as tuple
            # one newly created socket for every new client and
            # second is address of client which include IP as well as port
            client_new_socket, client_addr = self.s.accept()
            start_new_thread(self.process_request, (client_new_socket, client_addr))

    '''
    this function creates header in HTTP response format 
    after header lines - there should be one extra carriage return and line feed (/n) is needed
    
    Date : The date and time the response is originated in the format defined by RFC 7231 Date/Time Formats 2 .
    Server : A name for your HTTP server.
    Last-Modified : Last modified time and date of the requested resource, also in RFC 7231 Date/- Time Formats.
    Content-Type : The MIME type of this content. The mime.types file located at /etc/mime.types to determine 
                   the correct MIME type given a filename extension. If a file- name extension 
                   is not found in the mime.types file, you can use application/octet-stream.
    Content-Length : The length of the requested resource in bytes.
    '''

    def create_header(self, response_code, ip_file_path):
        header = ""
        if response_code == 200:  # when page found
            try:
                header += "HTTP/1.1 200 OK\n"
                header += "Date: " + time.strftime("%a, %d %b %Y %H:%M:%S %Z", time.gmtime()) + "\n"
                header += "Server: CS557_Dipika_Test_Server" + "\n"
                header += "Last-Modified: " + time.strftime("%a, %d %b %Y %H:%M:%S %Z", time.gmtime(os.path.getmtime(ip_file_path))) + "\n"
                header += "Accept-Ranges: bytes" + "\n"
                header += "Content-Length: " + str(os.path.getsize(ip_file_path)) + "\n"
                if mimetypes.guess_type(ip_file_path)[0] is None:
                    header += "Content-Type: " + "application/octet-stream" + "\n\n"
                else:
                    header += "Content-Type: " + mimetypes.guess_type(ip_file_path)[0] + "\n\n"
            except Exception as e:
                print("Error in create header", e)
                header += "\n"
        elif response_code == 404:  # when page not found
            header += "HTTP/1.1 404 Not Found\n"
            header += "Date: " + time.strftime("%a, %d %b %Y %H:%M:%S %Z", time.gmtime()) + "\n"
            header += "Server: CS557_Dipika_Test_Server" + "\n\n"

        return header

    '''
    this function actually processes request thorugh seperate thread created by main thread
    it takes two input parameters - 
    client's socket created by accept() function call by server
    client address - which is tuple with 2 values client_ip and client_port
    '''

    def process_request(self, client_new_socket, client_addr):
        request_status = False
        request_msg = client_new_socket.recv(1024)  # receive client request
        request_msg = bytes.decode(request_msg)  # convert byte formed message into string form
        request_method = request_msg.split(" ")[0]  # request type is first space seperated word of request message
        if (request_method == "GET"):  # check GET request type
            request_file_path = request_msg.split(" ")[1]  # file_path is second space seperated word of request message
            request_file_path = "./www" + request_file_path  # www folder of current directory has objects at server side
            try:
                fd = open(request_file_path, 'rb')  # open file - read mode and byte form to avoid data curruption
                response_file = fd.read()
                fd.close()
                response_header = self.create_header(200, request_file_path)  # 200 is responce type - it means OK
                response_msg = response_header.encode() + response_file  # concat byte encoded header with file
                request_status = True
            except Exception as e:
                response_header = self.create_header(404, request_file_path)
                response_file = "<!DOCTYPE html><html><body><h1>Requested Page Not Found</h1></body></html>"
                response_msg = (response_header + response_file).encode()

            client_new_socket.send(response_msg)
            if (request_status == True):
                self.print_client_info(request_msg.split(" ")[1], client_addr[0], client_addr[1])

        else:
            print("Unknown request")
        client_new_socket.close()  # closing the client socket / connection

    '''
    this function is called by multiple threads at a time - so it needs to made thread safe before invoking
    this function prints details of client request in below format 
    
    requested resource
    client IP : client’s IP address in dotted decimal representation
    client port : client’s port number
    access times : the number of times this resource has been requested since the start of the HTTP server
    
    eg - /bar.html|128.226.118.20|4759|1
         /pics/foo.jpg|128.226.118.20|6001|1
         /bar.html|128.226.118.26|6550|2
         
    dictionary - data structure needed to check number of times particular client request is processed     
    '''

    def print_client_info(self, file_path, client_ip, client_port):
        self.print_lock.acquire()  # acquire lock for critical section of multithreaded program
        if file_path not in self.file_info_dictionary:
            self.file_info_dictionary[file_path] = 1
        else:
            self.file_info_dictionary[file_path] += 1

        print(file_path, "|", client_ip, "|", client_port, "|", self.file_info_dictionary[file_path])
        self.print_lock.release()  # release lock for critical section of multithreaded program


'''
this function creates object of http_Server class and call start_server function
'''

def main_method():
    obj = http_server()
    obj.start_server()


'''
start point of python program
'''
if __name__ == '__main__':
    main_method()
