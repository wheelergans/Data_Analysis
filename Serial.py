import serial
import time

addr = "/dev/tty.usbserial-FTGADTLD"
baud = 19200 ## baud rate for instrument

ser = serial.Serial(
    port = addr,\
    baudrate = baud,\
    timeout=20)

print("Connected to: " + ser.portstr)
ser.flush()
i = 0;
while True:
    i = i+1;
    ser.write("AT\r".encode())

    time.sleep(1)
    out =''
    while ser.inWaiting() > 0:
        out += ser.read(1).decode()

    if out != '':
        print(">>" + out)
        out=''

    ser.write("AT&K0\r".encode())
    time.sleep(1)
    out =''
    while ser.inWaiting() > 0:
        out += ser.read(1).decode()

    if out != '':
        print(">>" + out)
        out=''

    ser.write("AT+SBDWT=Hello World\r".encode())
    time.sleep(1)
    out =''
    while ser.inWaiting() > 0:
        out += ser.read(1).decode()

    if out != '':
        print(">>" + out)
        out=''

    ser.write("AT+SBDIX\r".encode())
    while ser.inWaiting() == 0:
        time.sleep(1)

    while ser.inWaiting() > 0:
            out += ser.read(1).decode()

    if out != '':
        print(">>" + out)
        out=''


    while int(out[out.find("+SBDIX: "):out.find("+SBDIX: ")+1])<5:

        while ser.inWaiting() > 0:
            out += ser.read(1).decode()

        if out != '':
            print(">>" + out)
            out=''

        while ser.inWaiting() == 0:
            time.sleep(1)
        out =''
        while ser.inWaiting() > 0:
            out += ser.read(1).decode()

        if out != '':
            print(out)

        ser.write("AT+SBDIX\r".encode())
        while ser.inWaiting() == 0:
            time.sleep(1)
        out =''

    time.sleep(30)
    print("Sent Message #: ",end ='')
    print(i)




# ser.write("AT&K0\r".encode())
# print(ser.readline().decode())
# ser.write("AT+SBDWT=Hello World\r".encode())
# print(ser.readline().decode())
# ser.write("AT+SBDIX\r".encode())
# print(ser.readline().decode())
#
#
# import time
# import serial
#
# # configure the serial connections (the parameters differs on the device you are connecting to)
# ser = serial.Serial(
#     port='/dev/ttyUSB1',
#     baudrate=9600,
#     parity=serial.PARITY_ODD,
#     stopbits=serial.STOPBITS_TWO,
#     bytesize=serial.SEVENBITS
# )
#
# ser.isOpen()
#
# print 'Enter your commands below.\r\nInsert "exit" to leave the application.'
#
# input=1
# while 1 :
#     # get keyboard input
#     input = raw_input(">> ")
#         # Python 3 users
#         # input = input(">> ")
#     if input == 'exit':
#         ser.close()
#         exit()
#     else:
#         # send the character to the device
#         # (note that I happend a \r\n carriage return and line feed to the characters - this is requested by my device)
#         ser.write(input + '\r\n')
#         out = ''
#         # let's wait one second before reading output (let's give device time to answer)
#         time.sleep(1)
#         while ser.inWaiting() > 0:
#             out += ser.read(1)
#
#         if out != '':
#             print ">>" + out
