#!/usr/bin/python3

#
#       filename:       alarm.py
#       author:         @KeiferC
#       date:           17 July 2019
#       version:        0.0.1
#       
#       description:    Alerts user when somthing shady is going
#                       on in the network
#
#       references:     
#          - https://0xbharath.github.io/art-of-packet-crafting-with-scapy/
#
#       usage:          python alarm.py ...
#

from scapy.all import *
import pcapy
import argparse
import sys

#########################################
# Main                                  #
#########################################
def main():
        parse_args()
        sys.exit()

#########################################
# Vuln detection functions              #
#########################################
#
# packet_callback()
#       
# Callback function for sniff function. Checks for insecure protocols
# (HTTP and FTP) and stealth scans (NULL, FIN, and XMAS)
#
# @param          packet object
# @return         n/a
#
def packet_callback(packet):
        try:
                if packet[TCP].dport == 80:
                        print("HTTP (web) traffic detected!")
                if packet[TCP].dport == 20":
                        print("FTP (web) traffic detected!")
        except:
                pass

#########################################
# Incident logging functions            #
#########################################

#########################################
# Command-line Interface                #
#########################################
#
# set_parser_args()
#       
# Sets up parser command-line arguments
#
# @param          n/a
# @return         argument parser
#
def set_parser_args():
        parser = argparse.ArgumentParser(
                description='A network sniffer that identifies basic \
                             vulnerabilities')

        parser.add_argument(
                '-i', 
                dest='interface', 
                help='Network interface to sniff on', 
                default='eth0')

        parser.add_argument(
                '-r', 
                dest='pcapfile', 
                help='A PCAP file to read')

        return parser.parse_args()

#
# parse_args()
#       
# Parses command-line arguments
#
# @param          n/a
# @return         n/a
#
def parse_args():
        args = set_parser_args()

        if args.pcapfile: # Reading from pcap file
                try:
                        print("Reading PCAP file %(filename)s..." % 
                              {"filename" : args.pcapfile})
                        sniff(offline=args.pcapfile, prn=packet_callback)  
                except:
                        print("Sorry, something went wrong reading PCAP \
                              file %(filename)s!" %
                              {"filename" : args.pcapfile})

        else: # Sniffing on interface
                print("Sniffing on %(interface)s... " % 
                      {"interface" : args.interface})
                try:
                        sniff(iface=args.interface, prn=packet_callback)
                except pcapy.PcapError:
                        print("Sorry, error opening network interface \
                              %(interface)s. It does not exist." % 
                              {"interface" : args.interface})
                except:
                        print("Sorry, can\'t read network traffic. \
                              Are you root?")

#########################################
# Function Calls                        #
#########################################
main()
