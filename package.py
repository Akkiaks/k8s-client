#!/usr/bin/python3 -tt

import pkg_resources
import urllib.request
import json
import click
import pprint
import os
import sys
import platform
import yaml
from prettytable import PrettyTable
from kubernetes import client, config, watch


__author__ = "Akash Haridas Dhongade"

#"""

#  Checking if the Kubernetes python package is installed or not 

#"""

#print ("Checking if Kubernetes is install.....")


#for package in ['kubernetes']:
#    try:
#        dist = pkg_resources.get_distribution(package)
#        if not dist:
#            print('{} ({}) is installed'.format(dist.key, dist.version))
#        #print ("Please fallow the below option to run the script")
#    except pkg_resources.DistributionNotFound:
#        print('{} is NOT Installed'.format(package))
#        val = raw_input("Do you want to install the package(y/n  :")
#        if val == y:
#            os.system("git clone --recursive https://github.com/kubernetes-client/python.git")
#            os.system(" cd ./python & python setup.py install & cd ..")


@click.group()
def main():
    """
    CLI for checking if K8S cluster is provisioned and deploy the application 
    """
    pass
    
def status_data():
    '''
    function queries the kube to list the items
    
    '''
    import subprocess
    pods_name = subprocess.check_output("kubectl get pods", shell=True)
    return pods_name
    
def kube_deploy():
    '''
    function to deploy the bookinfo demo site
    '''
    os.system("kubectl apply -f book.yaml")
    os.system("kubectl expose deployment productpage-v1 --type=LoadBalancer --name=product")
    return " Deployment Created. Status=", status_data()


@main.command()
#@click.option('--pods', '-a', help= 'list all the running Pods' )
#@click.argument('pods')
def Kube_status():
    '''
    function queries the kubernetes cluster and provide running Pods
    '''
    pods = status_data()
    if not pods:
        click.echo("Bookinfo Deployement not found")
        val = input("Do you want to proceed with the deployement(y/n): ")
        if val == "y":
            deploy = kube_deploy()
            print (deploy)

        else:
                sys.exit()
        
    else:
        print(status_data())
    #else: click.echo("deplyement not found.. ")

@main.command()
def ser_check():
    '''
        function return the product page of the application deployed on minikube
    '''
    import subprocess
    api_url = subprocess.Popen("minikube service product --url", shell=True, stdout=subprocess.PIPE, universal_newlines=True).communicate()[0]
    with urllib.request.urlopen(api_url) as response:
        if response.getcode() == 200:
           source = response.read()
           print ("\n\nProduct page is accessible form cluster : \n\n\n",source )
        else:
            print("An error occurred while attempting to retrieve data from the API.")



@main.command()
def k8s_status():
    '''
    function to list all the resources in k8s cluster
    '''
    
    config.load_kube_config()

    v1 = client.CoreV1Api()
    ret = v1.list_pod_for_all_namespaces(watch=False)
    pods = ret.items
    pods_name = [pod.metadata.name for pod in pods]
    pods_status = [pod.status.phase for pod in pods]
    print ("Listing all the pods status:")
    table = PrettyTable(['Pod Name', 'Status'])
    for i in range(len(pods)):
        table.add_row(list(zip(pods_name, pods_status))[i])
        print (table)


@main.command()
def del_deploy():
    '''
    function to delete the deployement
    '''
    os.system("kubectl delete -f book.yaml")
    os.system("kubectl delete service product")


@main.command()
def node_traffic():
    '''
    function to list the overall status of node
    '''
    os.system("kubectl describe node")



if __name__ == '__main__':
    main()



