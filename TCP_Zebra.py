import socket

#list of commands to execute
#for the full list of commands visit https://docs.zebra.com/us/en/printers/software/zpl-pg/sgd-command-support/sgds-supported-for-industrial-printers.html
#or execute a grateful command in bash to get all of them at once: (echo '! U1 getvar "allcv"' ; sleep 1) | nc 10.55.154.116 9100 > all_variables.txt

commands = {
    'Mode':'device.product_name',
    'Status':'device.status',
    'Wired IP':'internal_wired.ip.addr',
    'Wired netmask':'internal_wired.ip.netmask',
    'Wired IP gateway':'internal_wired.ip.gateway',
    'Wired MAC':'internal_wired.mac_addr',
    'Wireless IP':'wlan.ip.addr',
    'Uptime':'device.uptime',
    'Printing_darkness':'zpl.relative_darkness',
    'Printing_speed':'media.speed',
    'Printing_tearoff':'ezpl.tear_off',
    'Printing_mediatype':'ezpl.media_type',
    'Printing_sensor':'device.sensor_select',
    'Printing_printmethod':'ezpl.print_method',
    'Printing_width':'ezpl.print_width',
    'Printing_length':'zpl.label_length'}

socket.setdefaulttimeout(5) #sets the timeout in case printer doesn't respond

printer_ip = input("Enter printer IP: ")

def get_printer_info(printer_ip):
    try:
        with socket.socket() as tcp_connection:
            tcp_connection.connect((printer_ip, 9100))
            for command in commands:
                cmd = f'! U1 getvar "{commands[command]}"\r\n' #\r\n needed to make it a complete command for the printer
                tcp_connection.sendall(cmd.encode()) #converting command into bytes and sending
                response = tcp_connection.recv(2048).decode(errors='ignore').strip('"') #receive in 2048byte chunk and decode the response
                print(f"{commands[command]:25} -> {response}")
    except TimeoutError:
        print(f">>>No response from the device: {printer_ip}")
    except Exception as e:
        print(f">>>Error: {e}")

if __name__ == "__main__":
    get_printer_info(printer_ip)


#To be added:
#GUI with all the printers + packstations + a button to show data + a button to print test label with marked corners, some data and barcode to scan
#+button to upload correct configuration
#+GUI can actually use snmp to load printer status for all the known printers when opening the program
#edit this line:                 print(f"{commands[command]:25} → {response}") to get the keys -> responses not the commands -> responses