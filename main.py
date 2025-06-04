import subprocess, re, os, time

cf_t = ('Cloudflare', '1.1.1.1', '1.0.0.1')
g_t = ('Google public', '8.8.8.8', '8.8.4.4')
od_t = ('OpenDNS', '208.67.222.222', '208.67.220.220')
sh_t = ('Shecan', '178.22.122.100', '185.51.200.2')
a_t = ('Azad(403)', '10.202.10.202', '10.202.10.102')
print('Welcome to DNS changer')
print("""DNS servers list:
     ________________________________________
     | DNS server name  | DNS server number |
     |--------------------------------------|
     |    Cloudflare    |       (1)         |
     |--------------------------------------|
     |      Google      |       (2)         |
     |--------------------------------------|
     |     OpenDNS      |       (3)         |
     |--------------------------------------|
     |      Shecan      |       (4)         |
     |--------------------------------------|
     |     Azad(403)    |       (5)         |
     |--------------------------------------|
     |       DHCP       |       (d)         |
     |--------------------------------------|
     |     flush DNS    |       (f)         |
     |--------------------------------------|
     |>>>>>>>> created by D4rk $ide <<<<<<<<|
     ----------------------------------------
     """)
sd = input('select dns: ')  # 'sd' -> selected DNS
if sd == 'F' or 'f':
    uo = input("""    ___________________________
    | OS name |   OS number   |
    |-------------------------|
    |  Linux  |      (-)      |
    |-------------------------|
    | Windows |      (2)      |
    |-------------------------|
    |   Mac   |      (-)      |
    |-------------------------|

select your os: """)  # 'uo' -> user os
else:
    uo = input("""    ___________________________
    | OS name |   OS number   |
    |-------------------------|
    |  Linux  |      (1)      |
    |-------------------------|
    | Windows |      (2)      |
    |-------------------------|
    |   Mac   | Coming soon...|
    |-------------------------|

select your os: """)
if uo == '1':  # Linux section
    if sd == '1':
        os.system(f'echo nameserver {cf_t[1]} > /etc/resolv.conf && echo nameserver {cf_t[2]} >> /etc/resolv.conf')
    elif sd == '2':
        os.system(f'echo nameserver {g_t[1]} > /etc/resolv.conf && echo nameserver {g_t[2]} >> /etc/resolv.conf')
    elif sd == '3':
        os.system(f'echo nameserver {od_t[1]} > /etc/resolv.conf && echo nameserver {od_t[2]} >> /etc/resolv.conf')
    elif sd == '4':
        os.system(f'echo nameserver {sh_t[1]} > /etc/resolv.conf && echo nameserver {sh_t[2]} >> /etc/resolv.conf')
    elif sd == '5':
        os.system(f'echo nameserver {a_t[1]} > /etc/resolv.conf && echo nameserver {a_t[2]} >> /etc/resolv.conf')
    else:
        print('please type your dns server code.')
    udl = subprocess.run(['cat', '/etc/resolv.conf'], capture_output=True).stdout.decode()  # 'udl' -> user dns linux
    udlf = tuple(re.findall('nameserver (.*)', udl))  # 'udlf' -> user dns linux find
    if udlf == cf_t[1:]:
        print(f"You are now using the '{cf_t[0]}' DNS \nGood luck!")
        time.sleep(2)
        os.system('clear')
    elif udlf == g_t[1:]:
        print(f"You are now using the '{g_t[0]}' DNS \nGood luck!")
        time.sleep(2)
        os.system('clear')
    elif udlf == od_t[1:]:
        print(f"You are now using the '{od_t[0]}' DNS \nGood luck!")
        time.sleep(2)
        os.system('clear')
    elif udlf == sh_t[1:]:
        print(f"You are now using the '{sh_t[0]}' DNS \nGood luck!")
        time.sleep(2)
        os.system('clear')
    elif udlf == a_t[1:]:
        print(f"You are now using the '{a_t[0]}' DNS \nGood luck!")
        time.sleep(2)
        os.system('clear')
elif uo == '2':  # Windows section
    cnc = subprocess.run(['ipconfig', '/all'], capture_output=True).stdout.decode()  # 'cnc' -> cmd network check
    cenf = list(re.findall('Ethernet adapter (.*):', cnc))  # 'cenf' -> cmd ethernet network find
    cwnf = list(re.findall('Wireless LAN adapter (.*):', cnc))  # 'cwnf' -> cmd wifi network find
    if sd == 'F' or 'f':
        cfd = subprocess.run(['ipconfig', '/flushdns'])  # 'cfd' -> Cmd flush DNS
    else:
        num = 0
        nl = []  # 'nl' -> Network list
        head = ('    ' + 71 * '_')
        body = ('    |' + 69 * '-' + '|')
        print(head, '    |' + (18 * ' ') + 'Network name' + (18 * ' ') + '|   Network number   |', body, sep='\n')
        for network in cenf:
            num += 1
            nn = (int(abs(float(len(network) - 48) // 2)) * ' ' + f'{network}' + int(abs(float(len(network) - 48) / 2)) * ' ' )  # 'nn' -> Network name
            nc = (f'        ({num})         ')  # 'nc' -> Network code
            # print('    |' + int(abs(float(len(network) - 48) // 2)) * ' ' + f'{network}' + int(abs(float(len(network) - 48) / 2)) * ' ' + '|' + f'        ({num})         |', body, sep='\n')
            print('    |' + nn + '|' + nc + '|', body, sep='\n')
            nl.append(network)

        for network in cwnf:
            num += 1
            nn = (int(abs(float(len(network) - 48) // 2)) * ' ' + f'{network}' + int(abs(float(len(network) - 48) / 2)) * ' ' )  # 'nn' -> Network name
            nc = (f'        ({num})         ')  # 'nc' -> Network code
            # print('    |' + int(abs(float(len(network) - 48) // 2)) * ' ' + f'{network}' + int(abs(float(len(network) - 48) / 2)) * ' ' + '|' + f'        ({num})         |', body, sep='\n')
            print('    |' + nn + '|' + nc + '|', body, sep='\n')
            nl.append(network)
        ns = int(input('\nselect your network: '))  # 'ns' -> Network select

    if sd == '1':
        cpds = os.system(f'netsh interface ipv4 set dns "{nl[ns-1]}" static {cf_t[1]}')
        csds = os.system(f'netsh interface ipv4 add dns "{nl[ns-1]}" {cf_t[2]} index=2')
        print(f"You are now using the '{cf_t[0]}' DNS \nGood luck!")
        time.sleep(2)
        os.system('cls')
    elif sd == '2':
        cpds = os.system(f'netsh interface ipv4 set dns "{nl[ns-1]}" static {g_t[1]}')
        csds = os.system(f'netsh interface ipv4 add dns "{nl[ns-1]}" {g_t[2]} index=2')
        print(f"You are now using the '{g_t[0]}' DNS \nGood luck!")
        time.sleep(2)
        os.system('cls')
    elif sd == '3':
        cpds = os.system(f'netsh interface ipv4 set dns "{nl[ns-1]}" static {od_t[1]}')
        csds = os.system(f'netsh interface ipv4 add dns "{nl[ns-1]}" {od_t[2]} index=2')
        print(f"You are now using the '{od_t[0]}' DNS \nGood luck!")
        time.sleep(2)
        os.system('cls')
    elif sd == '4':
        cpds = os.system(f'netsh interface ipv4 set dns "{nl[ns-1]}" static {sh_t[1]}')
        csds = os.system(f'netsh interface ipv4 add dns "{nl[ns-1]}" {sh_t[2]} index=2')
        print(f"You are now using the '{sh_t[0]}' DNS \nGood luck!")
        time.sleep(2)
        os.system('cls')
    elif sd == '5':
        cpds = os.system(f'netsh interface ipv4 set dns "{nl[ns-1]}" static {a_t[1]}')
        csds = os.system(f'netsh interface ipv4 add dns "{nl[ns-1]}" {a_t[2]} index=2')
        print(f"You are now using the '{a_t[0]}' DNS \nGood luck!")
        time.sleep(2)
        os.system('cls')
    elif sd == 'd' or 'D':
        cpds = os.system(f'netsh interface ipv4 set dns "{nl[ns-1]}" dhcp')
    elif sd == 'F' or 'f':
        pass
    else:
        print('please type your dns server code.')
