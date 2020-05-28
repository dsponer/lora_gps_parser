import serial


ser = serial.Serial(port="COM30", baudrate="9600")
while True:
    while ser.inWaiting() > 0:
        line = ser.readline()
        if line:
            data = line.decode().strip()
            print(data)