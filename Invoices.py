import PySimpleGUI as sg
import subprocess
import docker  # type: ignore


def check_container_exists() -> str:
    client = docker.from_env()
    container_name = "dts_invoices"
    try:
        container = client.containers.get(container_name)
        return container.status
    except docker.errors.NotFound:
        return "not found"
    except DockerException:
        print("Unable to access Docker. Docker Desktop might not be running.")
        window["status"].update(
            "Unable to access Docker. Docker Desktop might not be running"
        )
        return "DockerError"


def create_container():
    client = docker.from_env()
    images = client.images.list()

    # check if image exits. If it does, create container. If not, build image and create container.
    if "dts_invoices" in images:
        subprocess.run(
            "docker run -it -v .:/app --name dts_invoives dts_invoices", shell=True
        )

    else:
        subprocess.run("docker build -t dts_invoices .", shell=True)
        subprocess.run(
            "docker run -it -v .:/app --name dts_invoices dts_invoices", shell=True
        )


def start_container():
    subprocess.run("docker start -ia dts_invoices", shell=True)


def stop_container():
    subprocess.run("docker stop dts_invoices", shell=True)


# -----------------------------------------GUI-----------------------------------------------------
sg.theme("Dark Blue 6")

layout = [
    [sg.Titlebar("DTS Invoices", background_color="black")],
    [sg.Text("GUI is frozen when process is running, use Ctrl + C")],
    [sg.Text("          to stop process in output shell/terminal.")],
    [sg.VPush()],
    [
        sg.Push(),
        sg.Button("Run Docker Container"),
        sg.Button("Run Python Program"),
        sg.Push(),
    ],
    [sg.Push(), sg.Button("Stop Container"), sg.Push()],
    [sg.Push(), sg.Text("", key="status"), sg.Push()],
    [sg.Push(), sg.Exit(), sg.Push()],
    [sg.VPush()],
]

window = sg.Window("DTS Invoices", layout=layout, size=(325, 205))

while True:
    event, values = window.read()

    if event == "Run Docker Container":
        if check_container_exists() == "not found":
            print("Creating Docker Container")
            window["status"].update("Creating and running Docker container")
            time.sleep(1)
            try:
                create_container()
            except KeyboardInterrupt:
                print("Interrupted. Stopping Docker Container")
                window["status"].update("Interrupted. Stopping Docker container")

        elif check_container_exists() == "running":
            print("DTS Invoices container is already running.")
            window["status"].update("DTS Invoices container is already running.")

        elif check_container_exists() == "exited":
            print("DTS Invoices container started.")
            window["status"].update("DTS Invoices container started.")
            time.sleep(1)
            try:
                start_container()
            except KeyboardInterrupt:
                print("Interrupted. Stopping Docker Container")
                window["status"].update("Interrupted. Stopping Docker Container")

    if event == "Run Python Program":
        subprocess.run("python watch.py", shell=True)
        window["status"].update("Running Python Program.")

    if event == "Stop Container":
        stop_container()
        if check_container_exists() == "exited":
            window["status"].update("Container already stopped.")
        else:
            window["status"].update("Container stopped.")

    if event == "Exit" or event == sg.WIN_CLOSED:
        break
