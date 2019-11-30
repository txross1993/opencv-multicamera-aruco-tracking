#!/bin/bash
SECRET_NAME=${1}
USERNAME=${2}
PASSWORD=${3}
NAMESPACE=${4}

kubectl create secret generic ${SECRET_NAME} --from-literal=user=${USERNAME} --from-literal=pass=${PASSWORD} --namespace=${NAMESPACE}