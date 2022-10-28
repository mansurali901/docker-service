from flask import Flask, render_template, redirect, url_for, request, session, g, Blueprint, abort, send_from_directory, flash, jsonify
import docker
from docker import client
import requests
import os


class Container:
    def wrapperFunction(stripdata):
        ContainerList = str(stripdata)
        CleanString = ContainerList.strip("<>Container: [], ")
        return CleanString 

    def listContainerAll(dhost):
        client = docker.DockerClient(base_url='tcp://'+ dhost)
        try:
            gotdata = client.containers.list()
            output = []
            for stripdata in client.containers.list():
                ContainerList = str(stripdata)
                cleancontent = Container.wrapperFunction(ContainerList)
                containersJson = {'containerID':  cleancontent}
                output.append(containersJson)
            return output
        except:
            abort(404)
    # List specific Container         
    def listContainerSpecific(dhost, userid):
        client = docker.DockerClient(base_url='tcp://'+ dhost)
        try:
            stripdata = client.containers.get(userid)
            output = []
            ContainerList = str(stripdata)
            cleancontent = Container.wrapperFunction(ContainerList)
            # Decorating String to JSON 
            containersJson = {'containerID': cleancontent}
            output.append(containersJson)
            return output
        except:
            return 'Container Not Found'
    def containerCreate(dhost, containerAttributes):
        client = docker.DockerClient(base_url='tcp://'+ dhost)
        # Construct JSON to Python variables
        ContainerImageName = containerAttributes['ContainerImageName']
        ContainerCommand = containerAttributes['ContainerCommand']
        ContainerName   = containerAttributes['userId']
        ContainerEnvironmentenv = containerAttributes['ContainerEnvironmentenv']
        ContainerEnvironmentRpass = containerAttributes['ContainerEnvironmentRpass']
        # Checking Container Status 
        ContainerCheck = Container.listContainerSpecific(dhost, ContainerName)
        if ContainerCheck is not 'Container Not Found':
            return 'Container is already created'
        else:     
            container = client.containers.run(ContainerImageName, ContainerCommand, detach=True, name=ContainerName, environment=['env='+ ContainerEnvironmentenv, 'ROOT_PASS=' + ContainerEnvironmentRpass])
            commandContainer = client.containers.get(ContainerName)
            commandContainer.exec_run('service ssh start', stdout=True)
            flash('Container has been container')
            return 'Container Created'
    def containerCommitdelete(dhost, userid):
        client = docker.DockerClient(base_url='tcp://'+ dhost)
        login = client.login('mansurali901', 'Welcome@1!')
        



