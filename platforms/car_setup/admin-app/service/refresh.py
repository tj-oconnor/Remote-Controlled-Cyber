import docker

docker_images = [
    "tjoconnor/service-king",
    "tjoconnor/service-crypto",
    "tjoconnor/service-hack",
    "tjoconnor/service-pwn",
    "tjoconnor/web-king",
    "tjoconnor/web-crypto",
    "tjoconnor/web-pwn"
]

def pull_docker_images(images):
    client = docker.from_env()
    for image in images:
        try:
            print(f"Pulling image: {image}")
            client.images.pull(image)
            print(f"Successfully pulled image: {image}")
        except docker.errors.ImageNotFound:
            print(f"Image not found: {image}")
        except docker.errors.APIError as e:
            print(f"Error pulling image: {image}")
            print(str(e))

pull_docker_images(docker_images)