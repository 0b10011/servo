import os
import datetime
import taskcluster

task_id = os.environ["DECISION_TASK_ID"] + "-child-task"
payload = {
    "taskGroupId": os.environ["DECISION_TASK_ID"],
    "provisionerId": "aws-provisioner-v1",
    "workerType": "github-worker",
    "created": taskcluster.fromNowJSON(""),
    "deadline": taskcluster.fromNowJSON("1 hour"),
    "metadata": {
        "name": "Taskcluster experiments for Servo: Child task",
        "description": "",
        "owner": os.environ["DECISION_TASK_OWNER"],
        "source": os.environ["DECISION_TASK_SOURCE"],
    }
    "payload": {
        "maxRunTime": 600,
        "image": "buildpack-deps:bionic-scm",
        "command": [
            "/bin/bash", "--login", "-c", """
                git clone %(DECISION_TASK_CLONE_URL)s repo &&
                cd repo &&
                git checkout %(DECISION_TASK_COMMIT_SHA)s &&
                python2.7 child-task.py
            """ % os.environ
        ]
    }
}
result = taskcluster.Queue().createTask(task_id, payload)
print("task created…? %r" % result)
