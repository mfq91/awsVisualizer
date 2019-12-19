#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Librerías

import argparse
import boto3

autor = "Mauro Fernández Quiñones"

# Capturar datos de la cuenta

ec2 = boto3.client('ec2')
ec2Response = ec2.describe_instances() # Captura la salida de "ec2 describe-instances"

rds = boto3.client('rds')
rdsResponse = rds.describe_db_instances() # Captura la salida de "rds describe-db-instances"

iam = boto3.client('iam')
alias = iam.list_account_aliases()['AccountAliases'][0]

# Parámetros

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--instances", help="Mostrar instancias", action="store_true")
parser.add_argument("-e", "--ebs", help="Mostrar almacenamiento de las instancias", action="store_true")
parser.add_argument("-v", "--vpc", help="Mostrar solo vpc", action="store_true")
parser.add_argument("-r", "--rds", help="Mostrar solo rds", action="store_true")
parser.add_argument("--iam", help="Mostrar solo iam", action="store_true")
args = parser.parse_args()

# Cabecera de la salida

def cabecera():
    print("\n-----------------------------------")
    print("Cuenta: " + alias)
    print("-----------------------------------")

# Consultas EC2

def runningEC2Instances(): # Número de instancias corriendo
    running=0
    for i in ec2Response["Reservations"]:
        if i["Instances"][0]["State"]["Name"] == "running":
            running+=1
    print("\nNúmero de instancias corriendo: " + str(running))
def totalInstancias(): # Número total de instancias
    total=0
    for i in ec2Response["Reservations"]:
        for t in i["Instances"]:
            total+=1
    print("\nNúmero total de instancias: " + str(total))
def allInstances(): # Sacar Tag Name de todas las instancias corriendo
    print("\nInstancias:\n")
    for i in ec2Response["Reservations"]:
            for t in i.get('Instances')[0].get('Tags'):
                if t['Key'] == 'Name':
                    print('{:<35}'.format(t.get('Value'))
                    + '{:>30}'.format(i.get('Instances')[0].get('InstanceId'))
                    + '{:>15}'.format(i.get('Instances')[0].get('InstanceType'))
                    + '{:>15}'.format(i["Instances"][0]["State"]["Name"])
                    + '{:>15}'.format(i["Instances"][0]["Placement"]["AvailabilityZone"])
                    + '{:>40}'.format(i["Instances"][0]["KeyName"])
                    + '{:>25}'.format(i["Instances"][0]["ImageId"])
                    )
def cuentaPropietaria(): # id de la cuenta propietaria de las instancias EC2
    print("\nCuenta propietaria de las instancias ( tag name | cuenta propietaria )\n")
    for p in ec2Response["Reservations"]:
        for t in p.get('Instances')[0].get('Tags'):
            if t['Key'] == 'Name':
                print('{:>35}'.format(t.get('Value'))
                +'{:>30}'.format(p.get('OwnerId')))
def listPublicIps(): # Imprimir las ips públicas de las instancias EC2 corriendo
    print("\nPublic Ips ( tag name | PublicIpAddress )\n")
    for i in ec2Response["Reservations"]:
        if i["Instances"][0]["State"]["Name"] == "running":
            for t in i.get('Instances')[0].get('Tags'):
                if t['Key'] == 'Name':
                    if i.get('Instances')[0].get('PublicIpAddress') is not None:
                        print('{:<40}'.format(t.get('Value'))
                        + '{:<30}'.format(i.get('Instances')[0].get('PublicIpAddress')))
                    else:
                        print('{:<40}'.format(t.get('Value'))
                        + '{:<35}'.format("Esta instancia no tiene ip pública"))
def listPrivateIps(): # Imprimir las ips privadas de las instancias EC2
    print("\nPrivate Ips ( tag name | PrivateIpAddress )\n")
    for p in ec2Response["Reservations"]:
        for t in p.get('Instances')[0].get('Tags'):
            if t['Key'] == 'Name':
                print('{:<40}'.format(t.get('Value'))
                + '{:<40}'.format(p.get('Instances')[0].get('PrivateIpAddress')))
def listAllSecurityGroups(): # Listar todos los security groups
    print("\nSecurity Groups ( GroupName | GroupId ) \n")
    for p in ec2Response["Reservations"]:
        print('{:<60}'.format(p.get('Instances')[0].get('NetworkInterfaces')[0].get('Groups')[0].get('GroupName')) 
        + '{:<60}'.format(p.get('Instances')[0].get('NetworkInterfaces')[0].get('Groups')[0].get('GroupId')))
def listSecurityGroups(): # Listar security groups attacheados a cada instancia
    print ("\nSecurity Groups atacheados a cada instancia\n")
    for i in ec2Response["Reservations"]:
        for t in i.get('Instances')[0].get('Tags'):
            if t['Key'] == 'Name':
                print("----------------------------")
                print(t.get('Value'))
                print("----------------------------")
                print("\n")
                for k in i.get('Instances')[0].get('NetworkInterfaces')[0].get('Groups'):
                    print('{:<60}'.format(k.get('GroupName')) +
                    '{:<40}'.format(k.get('GroupId')))
                print("\n")
def listVolumes(): # Listar volúmenes attacheados a cada instancia
    print ("\nVolúmenes atacheados a cada instancia\n")
    for i in ec2Response["Reservations"]:
        for t in i.get('Instances')[0].get('Tags'):
            if t['Key'] == 'Name':
                print("----------------------------")
                print(t.get('Value'))
                print("----------------------------")
                print("\n")
                for k in i.get('Instances')[0]["BlockDeviceMappings"]:
                    print('{:<20}'.format("Device Name:") + '{:<20}'.format(k["DeviceName"]) 
                    + '{:<20}'.format("\nVolumeId:") + '{:<20}'.format(k['Ebs']['VolumeId']))
                    print("\n")

# Consultas RDS

def runningRDSInstances(): # Número de bbdd corriendo
    running=0
    for i in rdsResponse["DBInstances"]:
        if i["DBInstanceStatus"] == "available":
            running+=1
    print("\nNúmero de bbdd corriendo: " + str(running))
def totalRDSInstances(): # Número total de instancias
    total=0
    for i in rdsResponse["DBInstances"]:
        total+=1
    print("\nNúmero total de bbdd: " + str(total))
def listRDSInstances():
    print("\nBases de datos:\n")
    for i in rdsResponse["DBInstances"]:
        print('{:<30}'.format(i.get('DBInstanceIdentifier'))
        + '{:>15}'.format(i.get('DBInstanceClass'))
        + '{:^20}'.format(str(i.get('AllocatedStorage'))+ " GB")
        + '{:>15}'.format(i.get('DBInstanceStatus'))
        + '{:>15}'.format(i.get('Engine'))
        + '{:>15}'.format(i.get('AvailabilityZone')))

# Consultas IAM

def listarUsuariosIAM():
    iam_all_users = iam.list_users()
    print("\nUsuarios IAM:\n")
    for u in iam_all_users['Users']:
        print(u['UserName'])
def listarGruposIAM():
    iam_all_groups = iam.list_groups()
    print("\nGrupos IAM:\n")
    for g in iam_all_groups['Groups']:
        print(g['GroupName'])
def listarGruposDeUsuarios():
    print("\nGrupos de cada usuario:\n")
    users=iam.list_users()
    for key in users['Users']:
        print("\nGrupos de " + key['UserName'] + ":")
        List_of_Groups =  iam.list_groups_for_user(UserName=key['UserName'])
        for key in List_of_Groups['Groups']:
            print(key['GroupName'])

def listarPoliciesUsuarios():
    print("Listando policies")
def checkMFA():
    print("\nUsuarios con MFA:\n")
    users=iam.list_users()
    for key in users['Users']:
        List_of_MFA_Devices = iam.list_mfa_devices(UserName=key['UserName'])
        for key in List_of_MFA_Devices['MFADevices']:
            if key.get('UserName') is not None:
                print(key.get('UserName'))


cabecera()

if args.instances:
    runningEC2Instances()
    totalInstancias()
    allInstances()
elif args.ebs:
    listVolumes()
elif args.vpc:
    listAllSecurityGroups()
elif args.rds:
    runningRDSInstances()
    totalRDSInstances()
    listRDSInstances()
elif args.iam:
    listarUsuariosIAM()
    checkMFA()
else:
    runningEC2Instances()
    totalInstancias()
    allInstances()
    listVolumes()
    listAllSecurityGroups()
    runningRDSInstances()
    totalRDSInstances()
    listRDSInstances()
    listarUsuariosIAM()
    checkMFA()

print("\n")
