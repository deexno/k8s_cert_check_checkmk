#!/bin/bash

certificates_source_folders=("/etc/kubernetes/pki/" "/etc/kubernetes/pki/etcd/")
echo "<<<k8s_cert_check>>>"

for certificates_folder in ${certificates_source_folders[@]}; do
    certificates="$(ls $certificates_folder/*.crt)"

    for certificate in $certificates
    do
        certificate_file_name=$(basename $certificate)
        certificate_name="${certificate_file_name/.crt/}"

        certificate_expiration_data="$(openssl x509 -in $certificate -enddate -noout)"
        certificate_expiration_date_string=${certificate_expiration_data/notAfter=/}
        certificate_expiration_date="$(date --date="$certificate_expiration_date_string" --utc +"%d-%m-%Y")"

        certificate_issuer="$(openssl x509 -in $certificate -issuer -noout)"

        echo "${certificate_issuer##* } $certificate_name $certificate_expiration_date"
    done
done
