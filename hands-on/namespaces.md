# Namespaces

1. Create a new PID namespace and run bash in it
  ```
  sudo unshare --fork --pid --mount-proc bash
  ```

2. Inspect processes from inside: 
  ```
  top
  ```
  
  Inspect processes from outside (host console):
  ```
  pstree -p | grep top
  ```
  
3. Inspect networks from inside: 
  ```
  ip a
  ```
  
4. Exit from process (and from namespace)
  ```
  exit
  ```
  
5. Create a new PID and NET namespace and run bash again
  ```
  sudo unshare --fork --pid --net --mount-proc bash
  ```
  
6. Inspect networks from inside: 
  ```
  ip a
  ```
