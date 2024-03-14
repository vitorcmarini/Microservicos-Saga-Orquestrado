import os
import threading
import subprocess

threads = []


def build_application(app):
    threads.append(app)
    print("Building application {}".format(app))
    os.system("cd {} && gradle build -x test".format(app))
    print("Application {} finished building!".format(app))
    threads.remove(app)


def docker_compose_up():
    print("Running containers!")
    os.popen("docker-compose up --build -d").read()
    print("Pipeline finished!")


def build_all_applications():
    print("Starting to build applications!")
    threading.Thread(target=build_application,
                     args={"order-service"}).start()
    threading.Thread(target=build_application,
                     args={"orchestrator-service"}).start()
    threading.Thread(target=build_application,
                     args={"product-validation-service"}).start()
    threading.Thread(target=build_application,
                     args={"payment-service"}).start()
    threading.Thread(target=build_application,
                     args={"inventory-service"}).start()


def remove_remaining_containers():
    print("Removing all containers.")
    subprocess.run(["docker-compose", "down"], check=True)
    result = subprocess.run(["docker", "ps", "-aq"], capture_output=True, text=True, check=True)
    containers = result.stdout.split('\n')
    containers.remove('')
    if len(containers) > 0:
        print(f"There are still {len(containers)} containers created")
        for container in containers:
            print(f"Stopping container {container}")
            subprocess.run(["docker", "container", "stop", container], check=True)
        subprocess.run(["docker", "container", "prune", "-f"], check=True)


if __name__ == "__main__":
    print("Pipeline started!")
    build_all_applications()
    while len(threads) > 0:
        pass
    remove_remaining_containers()
    threading.Thread(target=docker_compose_up).start()
