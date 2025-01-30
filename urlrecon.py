#!/usr/bin/python3

from datetime import datetime
import colorama
import json
import os

from colorama import Fore, Style

colorama.init()

# ------------------------------------------------------------------------

program = "XXX"

# passive -> 'crtsh', 'wayback', 'subfinder', 'assetfinder', 'rapiddns', 'abuseipdb', 'shodan'
passives = ['crtsh', 'wayback', 'subfinder', 'assetfinder', 'rapiddns', 'abuseipdb', 'shodan']

# resolvers -> '4char', 'chaos', 'assetnote', 'jhaddix', 'nokovo'
resolves = ['4char', 'chaos', 'assetnote', 'jhaddix', 'nokovo']

# ------------------------------------------------------------------------

def passive_handler(script, domain):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{timestamp} | {Fore.LIGHTMAGENTA_EX}script{Style.RESET_ALL} | {script} | Running")
    stored_file = f".saved"

    command = f"zsh -c '. ~/.zshrc && bb_{script}_subs {domain} > {stored_file}'"
    os.system(command)

    if os.path.exists(stored_file):
        line_count = os.popen(f"wc -l < {stored_file}").read().strip()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{timestamp} | {Fore.LIGHTMAGENTA_EX}script{Style.RESET_ALL} | {script} | found {line_count} subdomains gathered")
    else:
        line_count = 0

    command=f'zsh -c ". ~/.zshrc && bb_subscope subdomain add {stored_file} {domain} {program} --source {script}"'
    os.system(command)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{timestamp} | {Fore.LIGHTMAGENTA_EX}script{Style.RESET_ALL} | {script} | Finished")

# ------------------------------------------------------------------------

def resolver_asset(domain):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{timestamp} | {Fore.LIGHTMAGENTA_EX}script{Style.RESET_ALL} | Resolve Assets | Running")

    subdomains_file=f".subs"
    result=f".saved"

    command = f'bb_subscope subdomain list "*" "{domain}" "{program}" --brief > {subdomains_file}'
    os.system(command)

    command = f"""zsh -c '. ~/.zshrc && puredns resolve {subdomains_file} --write {result} --rate-limit 850  -r ~/.resolvers'"""
    os.system(command)

    if os.path.exists(result):
        line_count = os.popen(f"wc -l < {result}").read().strip()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{timestamp} | {Fore.LIGHTMAGENTA_EX}script{Style.RESET_ALL} | Resolve Assets | found {line_count} resolved subdomains")
    else:
        line_count = 0

    command = f'bb_subscope subdomain add {result} "{domain}" "{program}" --source selfres --resolved yes'
    os.system(command)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{timestamp} | {Fore.LIGHTMAGENTA_EX}script{Style.RESET_ALL} | Resolve Assets | Finished")

# ------------------------------------------------------------------------

def resolve_handler(script, domain):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{timestamp} | {Fore.LIGHTMAGENTA_EX}script{Style.RESET_ALL} | {script} | Running")

    wordlist_file=f".wordlist"
    result=f".saved"

    command = f"""zsh -c '. ~/.zshrc && cat /opt/wordlists/static_dns_{script}.txt | sed "s/$/.{domain}/g" > {wordlist_file}'"""
    os.system(command)

    command = f"""zsh -c '. ~/.zshrc && bb_dns_static {domain} {wordlist_file} > {result}'"""
    os.system(command)

    if os.path.exists(result):
        line_count = os.popen(f"wc -l < {result}").read().strip()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{timestamp} | {Fore.LIGHTMAGENTA_EX}script{Style.RESET_ALL} | {script} | found {line_count} resolved subdomains")
    else:
        line_count = 0

    command = f'bb_subscope subdomain add {result} "{domain}" "{program}" --source {script} --resolved yes'
    os.system(command)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{timestamp} | {Fore.LIGHTMAGENTA_EX}script{Style.RESET_ALL} | {script} | Finished")

# ------------------------------------------------------------------------

def permutation_handler(domain):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{timestamp} | {Fore.LIGHTMAGENTA_EX}script{Style.RESET_ALL} | permutation | Running")

    subs_file=".subs"
    wordlist_file=".wordlist"
    result=f".saved"

    command = f'zsh -c ". ~/.zshrc && bb_subscope subdomain list \'*\' {domain} {program} --brief > {subs_file}"'
    os.system(command)

    command = f"""zsh -c '. ~/.zshrc && bb_wlgen_dynamic_pertarget {subs_file} > {wordlist_file}'"""
    os.system(command)

    command = f"""zsh -c '. ~/.zshrc && bb_dns_static {domain} {wordlist_file} > {result}'"""
    os.system(command)

    if os.path.exists(result):
        line_count = os.popen(f"wc -l < {result}").read().strip()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{timestamp} | {Fore.LIGHTMAGENTA_EX}script{Style.RESET_ALL} | permutation | found {line_count} resolved subdomains")
    else:
        line_count = 0

    command = f'bb_subscope subdomain add {result} "{domain}" "{program}" --source permutation --resolved yes'
    os.system(command)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{timestamp} | {Fore.LIGHTMAGENTA_EX}script{Style.RESET_ALL} | permutation | Finished")

# ------------------------------------------------------------------------

def http_handler(domain):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{timestamp} | script | live_subdomains | Running")
    output = ".saved"

    useragent = "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15"

    command = f"""bb_subscope subdomain list '*' {domain} {program} --resolved yes --brief | httpx -silent -duc -j -sc -method -title -server -td -ip -cname -cdn -r 8.8.4.4,129.250.35.251,208.67.222.222 -H "{useragent}" > {output}"""
    
    exit_code = os.system(command)
    if exit_code != 0:
        print(f"Error executing command: {command}")
        return

    # Check if output file is created and has content
    if os.path.exists(output) and os.path.getsize(output) > 0:
        with open(output, 'r') as f:
            json_data = f.readlines()

        for json_entry in json_data:
            if json_entry.strip():
                try:
                    entry = json.loads(json_entry)
                except json.JSONDecodeError as e:
                    print(f"JSON decode error: {e} for entry: {json_entry}")
                    continue

                url = f'{entry.get("url")}:{entry.get("port")}'
                subdomain = entry.get('url').replace('https://', '').replace('http://', '').split('/')[0]
                scheme = entry.get('scheme', 'none')
                method = entry.get('method', 'none')
                port = entry.get('port', 'none')
                status_code = entry.get('status_code', 'none')
                ip_address = entry.get('host', 'none')
                title = entry.get('title', 'none')
                cname = entry.get('cname', ['N/A'])[0]
                cdn_name = entry.get('cdn_name', 'none')
                cdn_status = 'yes' if 'cdn_name' in entry else 'no'
                tech = ', '.join(entry.get('tech', [])) if entry.get('tech') else 'none'
                location = entry.get('location', 'none')
                webserver = entry.get('webserver', 'none')
                content_length = entry.get('content_length', '0')

                if location.startswith("/"):
                    location = f'{url}{location}'

                print(entry)
                command = f'bb_subscope url add {url} {subdomain} {domain} {program} --scope inscope --scheme {scheme} --method {method} --port {port} --status_code {status_code} --ip {ip_address} --title "{title}" --cname {cname} --cdn_status {cdn_status} --cdn_name {cdn_name} --webserver {webserver} --location {location} --webtech "{tech}" --content_length "{content_length}" --webserver "{webserver}"'
                os.system(command)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{timestamp} | {Fore.LIGHTMAGENTA_EX}script{Style.RESET_ALL} | live_subdomains | Finished")

# ------------------------------------------------------------------------

def list_domains(program):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    list_command = f'zsh -c ". ~/.zshrc && bb_subscope domain list \'*\' {program} --brief > .domains 2> /dev/null"'
    os.system(list_command)

    if os.path.exists('.domains'):
        with open('.domains', 'r') as f:
            domains = f.read().strip().splitlines()
        return domains
    else:
        print(f"{timestamp} | {Fore.RED}Error listing domains. Check if the command ran successfully.{Style.RESET_ALL}")
        return []

# ------------------------------------------------------------------------

domains = list_domains(program)

for domain in domains:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{timestamp} | {Fore.LIGHTRED_EX}target{Style.RESET_ALL} | {domain} | Running")

    if (domain != "" ):
        for method in passives:
            passive_handler(method, domain)

        resolver_asset(domain)

        for method in resolves:
             resolve_handler(method, domain)

        permutation_handler(domain)

        http_handler(domain)

    print(f"{timestamp} | {Fore.LIGHTRED_EX}target{Style.RESET_ALL} | {domain} | Finished")
