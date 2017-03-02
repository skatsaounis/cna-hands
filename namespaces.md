# Namespaces

The goal of this exercise is to have a first, hands-on experience with Linux namespaces.
In specific, we will get a first idea around PID and NET namespaces. 

For this purpose, we will use the `unshare` Linux utility which is a wrapper around the `unshare` system call. 
Using it, we will spawn a new program inside one or more new namespaces, which are specified as command line options. 

## PID namespace

1. Run `bash` into a new PID namespace
  ```
  sudo unshare --fork --pid --mount-proc /bin/bash
  ```

2. Inspect processes from inside: 
  ```
  top
  ```
  
  Inspect processes from outside (host console):
  ```
  pgrep -xa top
  ```
  What do you observe?
  
3. Inspect network interfaces from inside: 
  ```
  ip link
  ```
  What do you observe?
  
4. Exit from process (and from namespace)
  ```
  exit
  ```

## NET namespace
  
1. Now, run `bash` inside a new PID __and__ NET namespace. 
  ```
  sudo unshare --fork --pid --net --mount-proc /bin/bash
  ```
  
2. Inspect network interfaces from inside: 
  ```
  ip link
  ```
  What do you observe?
  
