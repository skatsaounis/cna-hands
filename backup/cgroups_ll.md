# Cgroups

0. Login as root
    ```
    sudo su
    ```

1. Create two control groups, a "red" and a "blue", under the controllers `cpu` and `cpuset`
    ```
    mkdir /sys/fs/cpu/red/
    mkdir /sys/fs/cpuset/red/
    mkdir /sys/fs/cpu/blue/
    mkdir /sys/fs/cpuset/blue/
    ```
    
   Inspect the tunables:
    ```
    ls -l /sys/fs/cgroup/cpu/red
    ls -l /sys/fs/cgroup/cpuset/red
    ```

2. Read the default values of `cpu.shares` and `cpuset.cpus` tunables
    ```
    cat /sys/fs/cgroup/cpu/red/cpu.shares
    cat /sys/fs/cgroup/cpu/red/cpuset.cpus

    cat /sys/fs/cgroup/cpu/blue/cpu.shares
    cat /sys/fs/cgroup/cpu/blue/cpuset.cpus
    ```

3. Modify both cgroups, so that they assign __CPU 0 only__ (and mem 0) to tasks of these groups
  
    ```
    echo 0 > /sys/fs/cgroup/cpuset/red/cpuset.cpus 
    echo 0 > /sys/fs/cgroup/cpuset/red/cpuset.mems 

    echo 0 > /sys/fs/cgroup/cpuset/blue/cpuset.cpus
    echo 0 > /sys/fs/cgroup/cpuset/blue/cpuset.mems 
    ```

4. Launch two CPU intensive processes

    ```
    dd if=/dev/zero of=/dev/null &
    dd if=/dev/zero of=/dev/null &
    ```

  and get their PIDs
    ```
    ps aux|grep dd
    ```


5. Move first process to the "red" group, and the other to the "blue" one 
    ```
    echo <PID1> > /sys/fs/cgroup/cpu/red/tasks
    echo <PID1> > /sys/fs/cgroup/cpuset/red/tasks
    echo <PID2> > /sys/fs/cgroup/cpu/blue/tasks
    echo <PID2> > /sys/fs/cgroup/cpuset/blue/tasks
    ```

    and inspect their CPU usage
    ```
    top
    ```

6. Change their CPU shares so that PID1 gets 75% of CPU 0 time, and PID2 gets 25% of CPU 1 time
    ```
    echo 768 > /sys/fs/cgroup/cpu/red/cpu.shares 
    echo 256 > /sys/fs/cgroup/cpu/blue/cpu.shares 
    ```
    
    and inspect their CPU usage again
    ```
    top
    ```

7. Stop processes
    ```
    killall dd 
    ```
