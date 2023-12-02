# Lesson 2 | Attack Oriented Programming

The student will be given access to a Linux shell (served via ttyd) as well as a compiled binary.  Running the binary reveals the need to brute-force a 4-digit pin.  Entering the correct pin will reveal the flag.

**NOTE:** Successful build of the Docker image requires Dockerfile and compiled "pin" binary to be placed in the same directory.  `start.sh` requires the program `ttyd.arm` to exist somewhere in `$PATH`.

## TODO

- Find a way to run `ttyd` from *within* the Docker container, rather than serving the container itself by running `ttyd` on the host OS.
- Organize the project's file structure a little better; possibly write a Makefile?
