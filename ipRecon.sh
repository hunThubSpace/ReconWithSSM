#! /usr/bin/bash

# ------- Only fill these ------- #
asn="ASXXX"
program="XXX"
# ------------------------------- #

file_gz="$program.$asn.json.gz"

shodan download --fields ip_str,port,asn,hostname,domain,org,data,isp,os,product,version,vulns  --limit -1 $file_gz asn:$asn

gzip -d $file_gz
file_json=$(ls $file_gz | cut -d "." -f 1,2,3)

cat $file_json | jq -c '{ip_str, port, asn, hostname, domain, org, isp, os, product, version}' | \
     parallel -j 50 ' \
         ip=$(echo {} | jq -r ".ip_str")
         port=$(echo {} | jq -r ".port // 0")
         asn=$(echo {} | jq -r ".asn // \"none\"")
         hostname=$(echo {} | jq -r ".hostname // \"none\"")
         domain=$(echo {} | jq -r ".domain // \"none\"")
         organization=$(echo {} | jq -r ".org // \"none\"")
         data="https://www.shodan.io/host/$ip#$port"
         isp=$(echo {} | jq -r ".isp // \"none\"")
         os=$(echo {} | jq -r ".os // \"none\"")
         product=$(echo {} | jq -r ".product // \"none\"")
         version=$(echo {} | jq -r ".version // \"none\"")

         bb_subscope ip add $ip "$program" --port $port --asn $asn --hostname "$hostname" --domain "$domain" --organization "$organization" --isp "$isp" --os "$os" --product "$product" --version "$version" --data $data
     '
