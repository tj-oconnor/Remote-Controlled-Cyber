from flask import Flask, render_template, request, redirect, url_for

import docker

app = Flask(__name__)
docker_client = docker.from_env()
docker_client.containers.prune()

docker_images = [
    "tjoconnor/service-king",
    "tjoconnor/service-crypto",
    "tjoconnor/service-hack",
    "tjoconnor/service-pwn-1",
    "tjoconnor/service-pwn-2",
    "tjoconnor/service-pwn-3",
    "tjoconnor/web-king",
    "tjoconnor/web-crypto",
    "tjoconnor/web-pwn-1",
    "tjoconnor/web-pwn-2",
    "tjoconnor/web-pwn-3"
]

start_opts = {
    "network_mode": "host",
    "devices": ["/dev/i2c-1"],
    "restart_policy": {"Name": "always"},
}

stop_opts = {
    "restart_policy": {"Name": "no"}
}

@app.route("/", methods=["GET", "POST"])
def home():
    containers = docker_client.containers.list(all=True)
    if request.method == "POST":
      try:
        image_name = request.form.get("image_name")
        action = request.form.get("action")

        if action == "start":
            docker_client.containers.run(image_name, **start_opts, detach=True, tty=True)
        elif action == "stop":
            for container in containers:
                if container.attrs['Config']['Image'] == image_name:
                    container.update(**stop_opts)
                    container.stop()
                    container.remove()
        return redirect(url_for('home'))
      except Exception as e:
        return render_template("error.html", error=e)

    container_states = {image: False for image in docker_images}
    for container in containers:
        if container.attrs['Config']['Image'] in docker_images:
            if container.status == 'running':
                container_states[container.attrs['Config']['Image']] = True
            else:
                container_states[container.attrs['Config']['Image']] = False

    return render_template("index.html", container_states=container_states)


if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=False, port=8888)
