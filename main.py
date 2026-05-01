import subprocess, re, os, time, platform, json


class DnsServer:
    def load_data(file):
        try:
            f = open(file, encoding = 'utf-8')
            data = json.load(f)
            f.close()
            return data
        except FileNotFoundError:
            print('Database not found!!!')
            return []
        except json.JSONDecodeError:
            print("Error decoding JSON. The file may be corrupted or empty.")
            return []
        except Exception as e:
            print(e)
            return []

    def save_changes(file, changes):
        try:
            f = open(file, 'w', encoding = 'utf-8')
            json.dump(changes, f, indent = 2)
            f.close()
        except:
            print('Failed to save changes!')

    def new_dns(name, dns1, dns2):
        try:
            data = DnsServer.load_data('dns_dictionary.json')
            data.append({
                'DNS Server Name': name,
                'Primary DNS Server': dns1,
                'Secondary DNS Server': dns2
            })
            DnsServer.save_changes('dns_dictionary.json', data)
            print('Custom DNS created successfully.')
        except:
            print('Failed to create custom DNS.')

    def ping(in_ip, method):
        match method:
            case 0:  # Win 8.1, 10, 11
                try:
                    avg, lost = '--', '-%'
                    # _ = subprocess.run(['ping', '-n', '4', f'{in_ip}'],capture_output=True).stdout
                    # avg = re.findall('Average = (.*)ms', str(_))
                    # lost = str(re.findall('Lost = (.*)loss', str(_))).split(' ')[1].strip('(')
                    # if avg == []:
                    #     avg = '-1'
                    # else:
                    #     avg = avg[0]
                    return avg, lost
                except:
                    print('Ping process failed.')
                    return ''
            case 1:  # Linux
                try:
                    _ = subprocess.run(['ping', '-c4', f'{in_ip}'],capture_output=True).stdout
                    avg = str(re.findall('min/avg/max/mdev = (.*)', str(_))).split('/')
                    lost = str(re.findall('received, (.*) packet loss', str(_))).strip("['']")
                    if avg == ['[]']:
                        avg = '-1'
                    else:
                        avg = avg[1]
                    return avg, lost
                except:
                    print('Ping process failed.')
                    return ''
            # case 2:  # Win 7
            #     for i in dns_servers.load_data():
            #         print(i['DNS Server Name'] + '111')

    def settings(change, io = 0):
        try:
            data = DnsServer.load_data('settings.json')
            match change:
                case 0:
                    return data
                case 1:
                    data[0]['auto flush dns'] = io
                    DnsServer.save_changes('settings.json', data)
                    return 'Setting updated successfully.'
                case 2:
                    data[0]['ipv4'] = io
                    DnsServer.save_changes('settings.json', data)
                    return 'Setting updated successfully.'
                case 3:
                    data[0]['ipv6'] = io
                    DnsServer.save_changes('settings.json', data)
                    return 'Setting updated successfully.'
        except:
            return 'Failed to change settings.'

if DnsServer.load_data('dns_dictionary.json') == [] or DnsServer.load_data('settings.json') == []:
    print('Bye')
    exit()

_ = DnsServer.load_data('settings.json')
aflush, i4, i6 = _[0]['auto flush dns'], _[0]['ipv4'], _[0]['ipv6']
system, node, release, version, machine, cpu = platform.uname()
print('Welcome to DNS changer')
valid_networks = []

def settings_menu():
    _ = DnsServer.load_data('settings.json')
    aflush, i4, i6 = _[0]['auto flush dns'], _[0]['ipv4'], _[0]['ipv6']
    sett_head = ('     ' + 30 * '_')  # 'sett_head' -> Settings menu header
    sett_body = ('     |' + 28 * '-' + '|')  # 'sett_body' -> Settings menu body
    os.system('cls')
    autoflush = (int(abs(float(len('Auto Flush DNS') - 20) // 2)) * ' ' + 'Auto Flush DNS' + int(abs(float(len('Auto Flush DNS') - 20) / 2)) * ' ')
    ipv4 = (int(abs(float(len('IPv4 Protocol') - 20) // 2)) * ' ' + 'IPv4 Protocol' + int(abs(float(len('IPv4 Protocol') - 20) / 2)) * ' ')
    ipv6 = (int(abs(float(len('IPv6 Protocol') - 20) // 2)) * ' ' + 'IPv6 Protocol' + int(abs(float(len('IPv6 Protocol') - 20) / 2)) * ' ')
    print(f"{sett_head}\n     |{autoflush}| {' ON  ' if aflush == 1 else ' OFF '} |\n{sett_body}\n     |{ipv4}| {' ON  ' if i4 == 1 else ' OFF '} |\n{sett_body}\n     |{ipv6}| {' ON  ' if i6 == 1 else ' OFF '} |\n{sett_body}\n")
    while True:
        change = input('Edit (example: auto flush on, ipv4 off): ')
        match change.lower():
            case 'q':
                os.system('cls')
                break
            case 'auto flush on':
                DnsServer.settings(1, 1)
                settings_menu()
            case 'auto flush off':
                DnsServer.settings(1, 0)
                settings_menu()
            case 'ipv4 on':
                DnsServer.settings(2, 1)
                settings_menu()
            case 'ipv4 off':
                DnsServer.settings(2, 0)
                settings_menu()
            case 'ipv6 on':
                DnsServer.settings(3, 1)
                settings_menu()
            case 'ipv6 off':
                DnsServer.settings(3, 0)
                settings_menu()
            case _:
                print('Please enter and for exit enter q')

match system:
    case 'Windows':  # Windows section
        valid_codes = ['f', 'd', 's', 'q']
        dls = []
        def dns_menu():
            os.system('cls')
            dl = 0
            dl_head = ('     ' + 67 * '_')  # 'dl_head' -> Dns list header
            dl_body = ('     |' + 65 * '-' + '|')  # 'dl_body' -> Dns list body
            dl_foot = (
                        '     |>>>>>>>>>>> created by D4rk $ide & Amirmohammad-Seifi <<<<<<<<<<<|' + '\n' + '     ' + 67 * '-')  # 'dl_foot' -> Dns list footer
            print(f'{dl_head}\n     |  DNS server name  |    DNS server ping    |  DNS server number  |\n{dl_body}')
            for dns in DnsServer.load_data('dns_dictionary.json'):
                dl += 1
                dn = (int(abs(float(len(dns['DNS Server Name']) - 19) // 2)) * ' ' + f"{dns['DNS Server Name']}" + int(
                    abs(float(len(dns['DNS Server Name']) - 19) / 2)) * ' ')
                dc = (int(abs(float(len(str(dl)) - 18) // 2)) * ' ' + f'({dl})' + int(
                    abs(float(len(str(dl)) - 20) / 2)) * ' ')
                _ = DnsServer.ping(dns['Primary DNS Server'], 0)
                dp1 = f" ping: {_[0]}ms"
                dpl1 = (int(abs(float(len(_[1]) + len(dp1) - 19) // 2)) * ' ' + f"pl:{_[1]}" + int(
                    abs(float(len(_[1]) + len(dp1) - 19) / 2)) * ' ')
                _ = DnsServer.ping(dns['Secondary DNS Server'], 0)
                dp2 = f" ping: {_[0]}ms"
                dpl2 = (int(abs(float(len(_[1]) + len(dp2) - 19) // 2)) * ' ' + f"pl:{_[1]}" + int(
                    abs(float(len(_[1]) + len(dp2) - 19) / 2)) * ' ')
                print(f'''     |                   |{dp1} {dpl1}|                     |
     |{dn}|                       |{dc}|
     |                   |{dp2} {dpl2}|                     |
{dl_body}''')
                dls.append(dns)
            for i in range(1, dl + 1):
                valid_codes.append(str(i))
            DHCP = (int(abs(float(len('DHCP') - 19) // 2)) * ' ' + 'DHCP' + int(abs(float(len('DHCP') - 19) / 2)) * ' ')
            Flush = (int(abs(float(len('flush DNS') - 19) // 2)) * ' ' + 'flush DNS' + int(
                abs(float(len('flush DNS') - 19) / 2)) * ' ')
            settings = (int(abs(float(len('settings menu') - 19) // 2)) * ' ' + 'settings menu' + int(
                abs(float(len('settings menu') - 19) / 2)) * ' ')
            quit = (int(abs(float(len('quit') - 19) // 2)) * ' ' + 'quit' + int(abs(float(len('quit') - 19) / 2)) * ' ')
            print(
                f'     |{DHCP}|                       |         (d)         |\n{dl_body}\n     |{Flush}|                       |         (f)         |\n{dl_body}\n     |{settings}|                       |         (s)         |\n{dl_body}\n     |{quit}|                       |         (q)         |\n{dl_body}\n{dl_foot}')

        def flush_dns():
            _ = subprocess.run(['ipconfig', '/flushdns'], capture_output=True)  # 'cfd' -> Cmd flush DNS
            print('Successfully flushed the DNS Resolver Cache.')

        _ = subprocess.run(['ipconfig', '/all'], capture_output=True).stdout.decode('utf-8')
        _ = str(_).split('\r\n\r\n')
        _ = [[_[x], _[x + 1]] for x in range(0, len(_) - 1, 2)]
        net_list = []
        for i in range(len(_)):
            if 'Host Name' in _[i][1] or 'Media disconnected' in _[i][1]:
                continue
            else:
                net_list.append(_[i][0][:-1])

        match release:
            case '7':
                def dns_loader_win7(dnscode):
                    cpds = os.system(f'netsh interface ipv4 set dns "{nl[int(ns) - 1]}" static {dnscode["Primary DNS Server"]}')  # 'cpds' -> cmd primary DNS set
                    csds = os.system(f'netsh interface ipv4 add dns "{nl[int(ns) - 1]}" {dnscode["Secondary DNS Server"]} index=2')  # 'csds' -> cmd secondary DNS set
                    print(f"You are now using the '{dnscode['DNS Server Name']}' DNS \nGood luck!")
                    time.sleep(2)
                    os.system('cls')
                while True:
                    sd = input('select dns: ')  # 'sd' -> selected DNS
                    if sd in valid_codes:
                        match sd:
                            case 'f':
                                cfd = subprocess.run(['ipconfig', '/flushdns'])  # 'cfd' -> Cmd flush DNS
                                time.sleep(2)
                                os.system('cls')
                            case 'd':
                                num = 0
                                nl = []  # 'nl' -> Network list
                                head = ('    ' + 89 * '_')
                                body = ('    |' + 87 * '-' + '|')
                                print(head, '    | Connection type |' + (18 * ' ') + 'Network name' + (18 * ' ') + '|   Network number   |', body, sep='\n')
                                for network in net_list:
                                    if 'Ethernet adapter' in network:
                                        num += 1
                                        nn = (int(abs(float(len(network[17:]) - 48) // 2)) * ' ' + f'{network[17:]}' + int(abs(float(len(network[17:]) - 48) / 2)) * ' ' )  # 'nn' -> Network name
                                        nc = (f'        ({num})         ')  # 'nc' -> Network code
                                        print('    |     Ethernet    |' + nn + '|' + nc + '|', body, sep='\n')
                                        nl.append(network[17:])
                                    elif 'Wireless LAN adapter' in network:
                                        num += 1
                                        nn = (int(abs(float(len(network[21:]) - 48) // 2)) * ' ' + f'{network[21:]}' + int(abs(float(len(network[21:]) - 48) / 2)) * ' ' )  # 'nn' -> Network name
                                        nc = (f'        ({num})         ')  # 'nc' -> Network code
                                        print('    |       Wi-Fi     |' + nn + '|' + nc + '|', body, sep='\n')
                                        nl.append(network[21:])
                                for i in range(1, len(nl) + 1):
                                    valid_networks.append(str(i))
                                while True:
                                    ns = input('select your network: ')  # 'ns' -> Network select
                                    if ns in valid_networks:
                                        cpds = os.system(f'netsh interface ipv4 set dns "{nl[int(ns) - 1]}" dhcp')
                                        print(f"Now your DNS set on Dynamic Host Configuration Protocol(DHCP) \nGood luck!")
                                        time.sleep(2)
                                        os.system('cls')
                                        break
                                    else:
                                        print('Please enter a valid network code.')
                            case _:
                                num = 0
                                nl = []  # 'nl' -> Network list
                                head = ('    ' + 89 * '_')
                                body = ('    |' + 87 * '-' + '|')
                                print(head, '    | Connection type |' + (18 * ' ') + 'Network name' + (18 * ' ') + '|   Network number   |', body, sep='\n')
                                for network in net_list:
                                    if 'Ethernet adapter' in network:
                                        num += 1
                                        nn = (int(abs(float(len(network[17:]) - 48) // 2)) * ' ' + f'{network[17:]}' + int(abs(float(len(network[17:]) - 48) / 2)) * ' ' )  # 'nn' -> Network name
                                        nc = (f'        ({num})         ')  # 'nc' -> Network code
                                        print('    |     Ethernet    |' + nn + '|' + nc + '|', body, sep='\n')
                                        nl.append(network[17:])
                                    elif 'Wireless LAN adapter' in network:
                                        num += 1
                                        nn = (int(abs(float(len(network[21:]) - 48) // 2)) * ' ' + f'{network[21:]}' + int(abs(float(len(network[21:]) - 48) / 2)) * ' ' )  # 'nn' -> Network name
                                        nc = (f'        ({num})         ')  # 'nc' -> Network code
                                        print('    |       Wi-Fi     |' + nn + '|' + nc + '|', body, sep='\n')
                                        nl.append(network[21:])
                                for i in range(1, len(nl) + 1):
                                    valid_networks.append(str(i))
                                while True:
                                    ns = input('select your network: ')  # 'ns' -> Network select
                                    if ns in valid_networks:
                                        dns_loader_win7((dls[int(sd) - 1]), dls[int(sd) - 1])
                                        break
                                    else:
                                        print('Please enter a valid network code.')
                        break
                    else:
                        print('Please enter a valid DNS code.')
            case _:
                def dns_loader_windows(dnscode):
                    try:
                        _ = subprocess.run(['netsh', 'interface', 'ip', 'set', 'dns', f'name="{nl[int(ns) - 1]}"', 'static', dnscode['Primary DNS Server']], capture_output = True)
                        a = re.findall('returncode=(.*), stdout', str(_))
                        _ = subprocess.run(['netsh', 'interface', 'ip', 'add', 'dns', f'name="{nl[int(ns) - 1]}"', dnscode['Secondary DNS Server'], 'index=2'], capture_output = True)
                        b = re.findall('returncode=(.*), stdout', str(_))
                        if a[0] == '1' or b[0] == '1':
                            print('DNS Changing Process Failed.')
                        else:
                            if aflush == 1:
                                print(f"You are now using the '{dnscode['DNS Server Name']}' DNS")
                                flush_dns()
                                print('Good luck!')
                            else:
                                print(f"You are now using the '{dnscode['DNS Server Name']}' DNS \nGood luck!")
                        time.sleep(2)
                        os.system('cls')
                    except:
                        print('DNS Changing Process Failed.')
                while True:
                    dns_menu()
                    sd = input('select dns: ')  # 'sd' -> selected DNS
                    if sd in valid_codes:
                        match sd:
                            case 'f':
                                flush_dns()
                                time.sleep(2)
                                os.system('cls')
                            case 'd':
                                num = 0
                                nl = []  # 'nl' -> Network list
                                head = ('    ' + 89 * '_')
                                body = ('    |' + 87 * '-' + '|')
                                print(head, '    | Connection type |' + (18 * ' ') + 'Network name' + (18 * ' ') + '|   Network number   |', body, sep='\n')
                                for network in net_list:
                                    if 'Ethernet adapter' in network:
                                        num += 1
                                        nn = (int(abs(float(len(network[17:]) - 48) // 2)) * ' ' + f'{network[17:]}' + int(abs(float(len(network[17:]) - 48) / 2)) * ' ' )  # 'nn' -> Network name
                                        nc = (f'        ({num})         ')  # 'nc' -> Network code
                                        print('    |     Ethernet    |' + nn + '|' + nc + '|', body, sep='\n')
                                        nl.append(network[17:])
                                    elif 'Wireless LAN adapter' in network:
                                        num += 1
                                        nn = (int(abs(float(len(network[21:]) - 48) // 2)) * ' ' + f'{network[21:]}' + int(abs(float(len(network[21:]) - 48) / 2)) * ' ' )  # 'nn' -> Network name
                                        nc = (f'        ({num})         ')  # 'nc' -> Network code
                                        print('    |       Wi-Fi     |' + nn + '|' + nc + '|', body, sep='\n')
                                        nl.append(network[21:])
                                for i in range(1, len(nl) + 1):
                                    valid_networks.append(str(i))
                                while True:
                                    ns = input('select your network: ')  # 'ns' -> Network select
                                    if ns in valid_networks:
                                        cpds = subprocess.run(['netsh', 'interface', 'ipv4', 'set', 'dnsservers', f'name="{nl[int(ns) - 1]}"', 'source=dhcp'], capture_output = True)
                                        a = re.findall('returncode=(.*), stdout', str(cpds))
                                        if a[0] == '1':
                                            print('DNS Changing Process Failed.')
                                        else:
                                            print(f"Now your DNS set on Dynamic Host Configuration Protocol(DHCP) \nGood luck!")
                                        time.sleep(2)
                                        os.system('cls')
                                        break
                                    else:
                                        print('Please enter a valid network code.')
                            case 's':
                                settings_menu()
                            case 'q':
                                exit()
                            case _:
                                num = 0
                                nl = []  # 'nl' -> Network list
                                head = ('    ' + 89 * '_')
                                body = ('    |' + 87 * '-' + '|')
                                print(head, '    | Connection type |' + (18 * ' ') + 'Network name' + (18 * ' ') + '|   Network number   |', body, sep='\n')
                                for network in net_list:
                                    if 'Ethernet adapter' in network:
                                        num += 1
                                        nn = (int(abs(float(len(network[17:]) - 48) // 2)) * ' ' + f'{network[17:]}' + int(abs(float(len(network[17:]) - 48) / 2)) * ' ' )  # 'nn' -> Network name
                                        nc = (f'        ({num})         ')  # 'nc' -> Network code
                                        print('    |     Ethernet    |' + nn + '|' + nc + '|', body, sep='\n')
                                        nl.append(network[17:])
                                    elif 'Wireless LAN adapter' in network:
                                        num += 1
                                        nn = (int(abs(float(len(network[21:]) - 48) // 2)) * ' ' + f'{network[21:]}' + int(abs(float(len(network[21:]) - 48) / 2)) * ' ' )  # 'nn' -> Network name
                                        nc = (f'        ({num})         ')  # 'nc' -> Network code
                                        print('    |       Wi-Fi     |' + nn + '|' + nc + '|', body, sep='\n')
                                        nl.append(network[21:])
                                for i in range(1, len(nl) + 1):
                                    valid_networks.append(str(i))
                                while True:
                                    ns = input('select your network: ')  # 'ns' -> Network select
                                    if ns in valid_networks:
                                        dns_loader_windows((dls[int(sd) - 1]))
                                        break
                                    else:
                                        print('Please enter a valid network code.')
                    else:
                        print('Please enter a valid DNS code.')
    case 'Linux':  # Linux section
        if DnsServer.load_data('dns_dictionary.json') == []:
            print('Bye')
            exit()
        dl = 0
        dl_head = ('     ' + 67 * '_')  # 'dl_head' -> Dns list header
        dl_body = ('     |' + 65 * '-' + '|')  # 'dl_body' -> Dns list body
        dl_foot = (
                    '     |>>>>>>>>>>> created by D4rk $ide & Amirmohammad-Seifi <<<<<<<<<<<|' + '\n' + '     ' + 67 * '-')  # 'dl_foot' -> Dns list footer
        print(f'{dl_head}\n     |  DNS server name  |    DNS server ping    |  DNS server number  |\n{dl_body}')
        dls = []
        valid_codes = ['d']
        for dns in DnsServer.load_data('dns_dictionary.json'):
            dl += 1
            dn = (int(abs(float(len(dns['DNS Server Name']) - 19) // 2)) * ' ' + f"{dns['DNS Server Name']}" + int(
                abs(float(len(dns['DNS Server Name']) - 19) / 2)) * ' ')
            dc = (int(abs(float(len(str(dl)) - 18) // 2)) * ' ' + f'({dl})' + int(
                abs(float(len(str(dl)) - 20) / 2)) * ' ')
            _ = DnsServer.ping(dns['Primary DNS Server'], 1)
            dp1 = f" ping: {_[0]}ms"
            dpl1 = (int(abs(float(len(_[1]) + len(dp1) - 19) // 2)) * ' ' + f"pl:{_[1]}" + int(
                abs(float(len(_[1]) + len(dp1) - 19) / 2)) * ' ')
            _ = DnsServer.ping(dns['Secondary DNS Server'], 1)
            dp2 = f" ping: {_[0]}ms"
            dpl2 = (int(abs(float(len(_[1]) + len(dp2) - 19) // 2)) * ' ' + f"pl:{_[1]}" + int(
                abs(float(len(_[1]) + len(dp2) - 19) / 2)) * ' ')
            print(f'''     |                   |{dp1} {dpl1}|                     |
             |{dn}|                       |{dc}|
             |                   |{dp2} {dpl2}|                     |
        {dl_body}''')
            dls.append(dns)
        for i in range(1, dl + 1):
            valid_codes.append(str(i))
        DHCP = (int(abs(float(len('DHCP') - 19) // 2)) * ' ' + 'DHCP' + int(abs(float(len('DHCP') - 19) / 2)) * ' ')
        print(f'     |{DHCP}|                       |         (d)         |\n{dl_body}\n{dl_foot}')


        def dns_loader_linux(dnscode):
            os.system(f"nmcli con mod {slicer} ipv4.dns {dnscode['Primary DNS Server']}")
            os.system(f"nmcli con mod {slicer} +ipv4.dns {dnscode['Secondary DNS Server']}")
            os.system(f'nmcli con mod {slicer} ipv4.ignore-auto-dns yes')
            os.system(f'nmcli con down {slicer} && nmcli con up {slicer}')


        while True:
            sd = input('select dns: ')  # 'sd' -> selected DNS
            if sd in valid_codes:
                match sd:
                    case 'd':
                        net_names = []
                        net_types = []
                        net_devices = []
                        connections = str(subprocess.run(['nmcli', 'con', 'show'], capture_output=True).stdout).strip(
                            "b'").split('\\n')
                        for connection in range(1, len(connections) - 1):
                            net_names.append(str(connections[connection].split('  ')[0]))
                            net_types.append(str(connections[connection]).rstrip(' ').split('  ')[-2])
                            net_devices.append(str(connections[connection]).rstrip(' ').split('  ')[-1])
                        nl_head = ('    ' + 105 * '_')
                        nl_body = ('    |' + 103 * '-' + '|')
                        print(nl_head, '    |' + (18 * ' ') + 'Network name' + (
                                    18 * ' ') + '| Connection type |' + ' Connection device |' + ' Network number |',
                              nl_body, sep='\n')
                        for i in range(len(net_names)):
                            nn = (int(abs(float(len(net_names[i]) - 48) // 2)) * ' ' + f'{net_names[i]}' + int(
                                abs(float(len(net_names[i]) - 48) / 2)) * ' ')  # 'nn' -> Network name
                            nt = (int(abs(float(len(net_types[i]) - 17) // 2)) * ' ' + f'{net_types[i]}' + int(
                                abs(float(len(net_types[i]) - 17) / 2)) * ' ')
                            nd = (int(abs(float(len(net_devices[i]) - 19) // 2)) * ' ' + f'{net_devices[i]}' + int(
                                abs(float(len(net_devices[i]) - 19) / 2)) * ' ')
                            nc = (int(abs(float(len(str(i)) - 14) // 2)) * ' ' + f'({i + 1})' + int(
                                abs(float(len(str(i)) - 14) / 2)) * ' ')
                            print('    |' + nn + '|' + nt + '|' + nd + '|' + nc + '|', nl_body, sep='\n')
                        for i in range(1, len(net_names) + 1):
                            valid_networks.append(str(i))
                        while True:
                            ns = input('select your network: ')  # 'ns' -> Network select
                            if ns in valid_networks:
                                slicer = net_names[int(ns) - 1]
                                slicer = slicer.replace(' ', r'\ ')
                                _ = subprocess.run(['systemd-resolve', '--status'], capture_output=True)
                                _ = re.findall(f'{net_devices[int(ns) - 1]}(.*)Default Route', str(_))
                                _ = re.findall('DNS Servers: (.*)n', str(_))
                                last_dnses = str(_[0]).rstrip('\\').split(' ')
                                for i in last_dnses:
                                    os.system(f'nmcli con mod {slicer} -ipv4.dns {i}')
                                os.system(f'nmcli con mod {slicer} ipv4.ignore-auto-dns no')
                                os.system(f'nmcli con down {slicer} && nmcli con up {slicer}')
                                print(f"Your DNS has been restored to its original state.\nGood luck!")
                                time.sleep(2)
                                os.system('clear')
                                break
                            else:
                                print('Please enter a valid network code.')
                    case _:
                        net_names = []
                        net_types = []
                        net_devices = []
                        connections = str(subprocess.run(['nmcli', 'con', 'show'], capture_output=True).stdout).strip(
                            "b'").split('\\n')
                        for connection in range(1, len(connections) - 1):
                            net_names.append(str(connections[connection].split('  ')[0]))
                            net_types.append(str(connections[connection]).rstrip(' ').split('  ')[-2])
                            net_devices.append(str(connections[connection]).rstrip(' ').split('  ')[-1])
                        nl_head = ('    ' + 105 * '_')
                        nl_body = ('    |' + 103 * '-' + '|')
                        print(nl_head, '    |' + (18 * ' ') + 'Network name' + (
                                    18 * ' ') + '| Connection type |' + ' Connection device |' + ' Network number |',
                              nl_body, sep='\n')
                        for i in range(len(net_names)):
                            nn = (int(abs(float(len(net_names[i]) - 48) // 2)) * ' ' + f'{net_names[i]}' + int(
                                abs(float(len(net_names[i]) - 48) / 2)) * ' ')  # 'nn' -> Network name
                            nt = (int(abs(float(len(net_types[i]) - 17) // 2)) * ' ' + f'{net_types[i]}' + int(
                                abs(float(len(net_types[i]) - 17) / 2)) * ' ')
                            nd = (int(abs(float(len(net_devices[i]) - 19) // 2)) * ' ' + f'{net_devices[i]}' + int(
                                abs(float(len(net_devices[i]) - 19) / 2)) * ' ')
                            nc = (int(abs(float(len(str(i)) - 14) // 2)) * ' ' + f'({i + 1})' + int(
                                abs(float(len(str(i)) - 14) / 2)) * ' ')
                            print('    |' + nn + '|' + nt + '|' + nd + '|' + nc + '|', nl_body, sep='\n')
                        for i in range(1, len(net_names) + 1):
                            valid_networks.append(str(i))
                        while True:
                            ns = input('select your network: ')  # 'ns' -> Network select
                            if ns in valid_networks:
                                slicer = net_names[int(ns) - 1]
                                slicer = slicer.replace(' ', r'\ ')
                                dns_loader_linux((dls[int(sd) - 1]))
                                print(
                                    f"You are now using the '{(dls[int(sd) - 1])["DNS Server Name"]}' DNS \nGood luck!")
                                time.sleep(2)
                                os.system('clear')
                                break
                            else:
                                print('Please enter a valid network code.')
                break
            else:
                print('Please enter a valid code.')
    case _:
        print('Failed to detect os!')