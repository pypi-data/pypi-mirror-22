****************
xldeploy-py
****************
Python SDK for XL-Deploy_.

.. _XL-Deploy: https://xebialabs.com/products/xl-deploy


Usage
=======

.. code:: python

    import xldeploy

    config = xldeploy.Config(protocol="http", host="localhost", port="4516", context_path="deployit", username="admin", password="admin")
    # or
    config = xldeploy.Config()
    client = xldeploy.Client(config)

    # repository
    repository = client.repository
    print repository.exists("Applications/EC2/1.0/ec2")
    print repository.exists("Applications/EC2/1.0/wrong")
    ci = repository.read("Applications/EC2/1.0/ec2")
    print ci.amiId

    # deployment
    deployment = client.deployment
    deploymentRef = deployment.prepare_initial("Applications/NIApp/1.0", "Environments/awsEnv")
    depl = deployment.prepare_auto_deployeds(deploymentRef)
    task = deployment.create_task(depl)
    task.start()
    print task.task_id

Installation
============
::

    $ pip install xldeploy-py
