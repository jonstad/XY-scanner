import serial
import findserialport
import os
#   it is worth noting that the example above will not work on a Windows machine;
# the Arduino serial device takes some time to load,
# and when a serial connection is established it resets the Arduino.

# https://playground.arduino.cc/Interfacing/Python

commands = {-1: {}}


def print_menu():
    print("Current serial port is : {}".format(serial_port_name))
    print("*"*80)
    print("-1: Exit")
    print("0: Print menu ")
    print("1: Manual drive Y-axis")
    print("2: Get stepper position Y")
    print("3: Manual drive X-axis")
    print("4: Get stepper position X")
    print("5: Raster")
    print("11: Print list of available serial ports")
    print("*"*80)


def select_serial_port():
    serial_port = findserialport.serial_ports()
    count = 0
    for port in serial_port:
        print("{}:{}".format(count, port))
        count += 1
    if count == 0:
        input("No serial ports available. Press any key to continue")
        return serial_port_name
    else:
        selected_port_nr = int(input("Select port:"))
        return serial_port[selected_port_nr]


def command1(axis):
    while True:
        inp = str(input("Enter a number {}-axis ".format(axis)))
        try:
            cmd = ""
            if int(inp) == 0:
                cmd = "xB{}\n".format(inp)
            else:
                if axis == 'X':
                    cmd = "xX{}\n".format(inp)
                if axis == 'Y':
                    cmd = "xY{}\n".format(inp)
            ser.write(cmd.encode())
        except ValueError:
            if inp == "quit":
                print("main: ")
                break
            else:
                print("Not a valid value")


def command2(axis):
    if axis == 'X':
        ser.write("xGETXPOS\n".encode())
    if axis == 'Y':
        ser.write("xGETYPOS\n".encode())

    ack = False
    while not ack:
        s = ser.readline()
        if len(s) > 0:
            ack = True
            print("Current pos is: {}".format(s))


def raster_menu():
    raster_scans = 100
    print("1: Set new X limit")
    print("2: Set new y step")
    print("3: Set raster scans")
    print("4: Start raster")
    print("5: One line start")
    print("6: Stop raster")
    menu_choice=0
    while menu_choice !=-1:
        menu_choice = int(input("Raster choice: "))
        if menu_choice == 1:
            new_limit_x = int(input("New x limit: "))
            ser.write("xSETLIMITX{}\n".format(new_limit_x).encode())
        elif menu_choice == 2:
            new_step_y = int(input("New step y: "))
            ser.write("xSETSTEPY{}\n".format(new_step_y).encode())
        elif menu_choice == 3:
            raster_scans = int(input("Number of raster to make: "))
        elif menu_choice == 4:
            ser.write("xA{}\n".format(raster_scans).encode())
        elif menu_choice == 5:
            line = input("limitx,stepy,rasters")
            split_line = line.split(',')
            # new_limit_x = int(split_line[0])
            # new_step_y = int(split_line[1])
            # raster_scans = int(split_line[2])
            #Use tupple for fun
            new_limit_x, new_step_y, raster_scans = line.split(',')

            ser.write("xSETLIMITX{}\n".format(int(new_limit_x)).encode())
            ser.write("xSETSTEPY{}\n".format(int(new_step_y)).encode())
            ser.write("xA{}\n".format(int(raster_scans)).encode())
        elif menu_choice == 6:
            ser.write("xB{}\n".encode())


def init_serial_communication():
    global serial_port_name
    serial_port_name = "COM12"
    global ser
    ser = serial.Serial(serial_port_name, timeout=5)
    print(ser.readlines())


init_serial_communication()
command = ""
print_menu()
while command != -1:

    try:
        command = int(input("Please input menu command: "))
        if command == 11:
            serial_port_name = select_serial_port()
            print("You have selected {}".format(serial_port_name))
        elif command == 0:
            print_menu()
        elif command == 1:
            command1('Y')
        elif command == 2:
            command2('Y')
        elif command == 3:
            command1('X')
        elif command == 4:
            command2('X')
        elif command == 5:
            raster_menu();
        else:
            print("No command implemented")
    except ValueError:
        print("Could not convert data to an integer.")

try:
    ser.close()
finally:
    print("Shutdown")
