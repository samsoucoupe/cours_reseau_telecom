import socket
import struct


def analyze_mac_address(mac_address):
    """
    Analyze a MAC address byte array.
    Input: mac_address is a byte array of 6 bytes
    """
    return mac_address.hex(":")


def analyze_ethernet_header(frame):
    """
    Analyze the Ethernet header of a frame.
    Input: frame is a byte array
    """
    eth_header = frame[0:14]
    eth_mac_dest, eth_mac_src, eth_type = struct.unpack('!6s6sH', eth_header)
    return (analyze_mac_address(eth_mac_dest), analyze_mac_address(eth_mac_src), eth_type)


def analyze_ethernet_type(frame):
    """
    Analyze the Ethernet type of a frame.
    Input: frame is a byte array
    """
    eth_header = frame[0:14]
    eth_type = struct.unpack('!H', eth_header[12:14])[0]
    return eth_type


def analyze_ipv4_header(frame):
    ip_header = frame[14:34]
    ipv4_fields = struct.unpack('!BBHHHBBH4s4s', ip_header)

    version = ipv4_fields[0] >> 4  # 4 bits de poids fort
    ttl = ipv4_fields[5]
    protocol = ipv4_fields[6]
    # IPV4 IP addresses are 32 bits long
    src_ip = socket.inet_ntoa(ipv4_fields[8])
    dst_ip = socket.inet_ntoa(ipv4_fields[9])

    print(f"Version : {version}")
    print(f"Time to live : {ttl}")
    print(f"Source IP : {src_ip}")
    print(f"Destination IP : {dst_ip}")

    return protocol


def analyze_ipv6_header(frame):
    # Analyse du header IPv6 (cf https://fr.wikipedia.org/wiki/IPv6)
    ipv6_header = frame[14:54]
    ipv6_fields = struct.unpack('!BBHHBB16s16s', ipv6_header)

    version = ipv6_fields[0] >> 4  # 4 bits de poids fort
    traffic_class = (ipv6_fields[0] & 0x0F) << 4 | (
            ipv6_fields[1] >> 4)  # 4 bits de poids faible + 4 bits de poids fort
    flow_label = (ipv6_fields[1] & 0x0F) << 16 | ipv6_fields[2]  # 4 bits de poids faible + 16 bits de poids fort
    payload_length = ipv6_fields[3]
    next_header = ipv6_fields[4]
    hop_limit = ipv6_fields[5]
    src_ip = socket.inet_ntop(socket.AF_INET6, ipv6_fields[6])
    dst_ip = socket.inet_ntop(socket.AF_INET6, ipv6_fields[7])

    print(f"Version : {version}")
    print(f"Traffic class : {traffic_class}")
    print(f"Flow label : {flow_label}")
    print(f"Payload length : {payload_length}")
    print(f"Hop limit : {hop_limit}")
    print(f"Source IP : {src_ip}")
    print(f"Destination IP : {dst_ip}")

    # Analyse du protocole
    print("=" * 60)

    return next_header


def analyze_ipv4_tcp_header(frame):
    tcp_header = frame[34:54]
    tcp_fields = struct.unpack('!HHLLBBHHH', tcp_header)

    print(f"Source port : {tcp_fields[0]}")
    print(f"Destination port : {tcp_fields[1]}")
    print(f"Sequence number : {tcp_fields[2]}")
    print(f"Acknowledgment number : {tcp_fields[3]}")

    data = frame[54:]
    print(f"Data : {data}")


def analyze_ipv6_tcp_header(frame):
    # Analyse du header TCP (cf https://fr.wikipedia.org/wiki/Transmission_Control_Protocol)
    tcp_header = frame[54:74]
    tcp_fields = struct.unpack('!HHLLBBHHH', tcp_header)

    print(f"Source port : {tcp_fields[0]}")
    print(f"Destination port : {tcp_fields[1]}")
    print(f"Sequence number : {tcp_fields[2]}")
    print(f"Acknowledgment number : {tcp_fields[3]}")

    data = frame[74:]
    print(f"Data : {data}")


def analyze_ipv4_udp_header(frame):
    udp_header = frame[34:42]
    udp_fields = struct.unpack('!HHHH', udp_header)

    print(f"Source port : {udp_fields[0]}")
    print(f"Destination port : {udp_fields[1]}")
    print(f"Length : {udp_fields[2]}")
    print(f"Checksum : {udp_fields[3]}")

    data = frame[42:]

    print(f"Data : {data}")


def analyze_ipv6_udp_header(frame):
    # Analyse du header UDP (cf https://fr.wikipedia.org/wiki/User_Datagram_Protocol)
    udp_header = frame[54:62]
    udp_fields = struct.unpack('!HHHH', udp_header)

    print(f"Source port : {udp_fields[0]}")
    print(f"Destination port : {udp_fields[1]}")
    print(f"Length : {udp_fields[2]}")
    print(f"Checksum : {udp_fields[3]}")

    data = frame[62:]

    print(f"Data : {data}")


def analyze_ipv4_icmp_header(frame):
    icmp_header = frame[34:42]
    icmp_fields = struct.unpack('!BBHHH', icmp_header)

    icmp_type = icmp_fields[0]
    icmp_code = icmp_fields[1]
    icmp_checksum = icmp_fields[2]
    icmp_id = icmp_fields[3]
    icmp_seq = icmp_fields[4]

    if icmp_type == 8:
        print(f"Type : Echo request")
    elif icmp_type == 0:
        print(f"Type : Echo reply")
    else:
        print(f"Type : {icmp_type}")

    print(f"Code : {icmp_code}")
    print(f"Checksum : {icmp_checksum}")
    print(f"Identifier : {icmp_id}")
    print(f"Sequence number : {icmp_seq}")

    data = frame[42:]

    print(f"Data : {data}")


def analyze_ipv6_icmp_header(frame):
    # Analyse du header ICMPv6 (cf https://fr.wikipedia.org/wiki/Internet_Control_Message_Protocol_V6)
    icmpv6_header = frame[54:62]
    icmpv6_fields = struct.unpack('!BBHHH', icmpv6_header)

    icmpv6_type = icmpv6_fields[0]
    icmpv6_code = icmpv6_fields[1]
    icmpv6_checksum = icmpv6_fields[2]
    icmpv6_identifier = icmpv6_fields[3]
    icmpv6_sequence_number = icmpv6_fields[4]

    if icmpv6_type == 128:
        print("Type : Echo request")
    elif icmpv6_type == 129:
        print("Type : Echo reply")

    print(f"Code : {icmpv6_code}")
    print(f"Checksum : {icmpv6_checksum}")
    print(f"Identifier : {icmpv6_identifier}")
    print(f"Sequence number : {icmpv6_sequence_number}")

    data = frame[62:]

    print(f"Data : {data}")


def analyze_arp_header(frame):
    # Analyse du header ARP (cf https://fr.wikipedia.org/wiki/Address_Resolution_Protocol)
    arp_header = frame[14:42]
    arp_fields = struct.unpack('!HHBBH6s4s6s4s', arp_header)

    arp_hardware_type = arp_fields[0]
    arp_protocol_type = arp_fields[1]
    arp_hardware_size = arp_fields[2]
    arp_protocol_size = arp_fields[3]
    arp_opcode = arp_fields[4]
    arp_sender_mac = arp_fields[5].hex(":")
    arp_sender_ip = socket.inet_ntoa(arp_fields[6])
    arp_target_mac = arp_fields[7].hex(":")
    arp_target_ip = socket.inet_ntoa(arp_fields[8])

    if arp_hardware_type == 1:
        print("Hardware type : Ethernet")
    elif arp_hardware_type == 6:
        print("Hardware type : IEEE 802 Networks")
    elif arp_hardware_type == 7:
        print("Hardware type : ARCNET")
    elif arp_hardware_type == 15:
        print("Hardware type : Frame Relay")

    if arp_protocol_type == 0x0800:
        print("Protocol type : IPv4")
    elif arp_protocol_type == 0x0806:
        print("Protocol type : ARP")
    elif arp_protocol_type == 0x8035:
        print("Protocol type : RARP")
    elif arp_protocol_type == 0x86DD:
        print("Protocol type : IPv6")

    print(f"Hardware size : {arp_hardware_size}")
    print(f"Protocol size : {arp_protocol_size}")

    if arp_opcode == 1:
        print("Opcode : Request")
    elif arp_opcode == 2:
        print("Opcode : Reply")

    print(f"Sender MAC : {arp_sender_mac}")
    print(f"Sender IP : {arp_sender_ip}")
    print(f"Target MAC : {arp_target_mac}")
    print(f"Target IP : {arp_target_ip}")
    pass


ETH_TYPE_IPv4 = 0x0800
ETH_TYPE_IPv6 = 0x86DD
ETH_TYPE_ARP = 0x0806
ETH_WOL = 0x0842


def analyze_semantics(frame):
    """
    Analyze an Ethernet frame.
    Input: frame is a byte array
    """
    print("-" * 60)
    print(f"\nTrame Ethernet en cours d'analyse (longueur {len(frame)} octets) :")
    print("=" * 60)

    # Analyse du header ETHERNET
    eth_mac_dest, eth_mac_src, eth_type = analyze_ethernet_header(frame)

    print(f"Destination MAC \t: {eth_mac_dest}")
    print(f"Source MAC \t: {eth_mac_src}")

    # Analyse du type de la trame
    eth_type_str = hex(analyze_ethernet_type(frame))

    print(f"Type de trame \t: {eth_type_str}")
    print("=" * 60)

    # IPv4
    if eth_type == ETH_TYPE_IPv4:
        print("Type : IPv4")

        # Analyse du header IPv4 (cf https://fr.wikipedia.org/wiki/IPv4)
        protocol = analyze_ipv4_header(frame)

        # Analyse du protocole
        print("=" * 60)

        # https://en.wikipedia.org/wiki/List_of_IP_protocol_numbers
        if protocol == 6:
            print("Protocol : TCP")

            # Analyse du header TCP (cf https://fr.wikipedia.org/wiki/Transmission_Control_Protocol)
            analyze_ipv4_tcp_header(frame)
        elif protocol == 17:
            print("Protocol : UDP")

            # Analyse du header UDP (cf https://fr.wikipedia.org/wiki/User_Datagram_Protocol)
            analyze_ipv4_udp_header(frame)
        elif protocol == 1:
            print("Protocol : ICMP")

            # Analyse du header ICMP (cf https://fr.wikipedia.org/wiki/Internet_Control_Message_Protocol)
            analyze_ipv4_icmp_header(frame)

        else:
            print(f"Protocol : {protocol}")

    elif eth_type == ETH_TYPE_IPv6:
        print("Type : IPv6")
        next_header = analyze_ipv6_header(frame)

        if next_header == 6:
            print("Protocol : TCP")
            analyze_ipv6_tcp_header(frame)
        elif next_header == 17:
            print("Protocol : UDP")
            analyze_ipv6_udp_header(frame)
        elif next_header == 58:
            print("Protocol : ICMPv6")
            analyze_ipv6_icmp_header(frame)
        else:
            print(f"Protocol : {next_header}")

    elif eth_type == ETH_TYPE_ARP:
        print("Type : ARP")
        analyze_arp_header(frame)
    elif eth_type == ETH_WOL:
        print("Type : WOL")
    else:
        print(f"Type : {eth_type}")
