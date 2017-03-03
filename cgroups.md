# Cgroups

The goal of this hands-on session is to get familiar with configuring cgroups to control 
resource allocation to processes.
We will use the `cpu` and `cpuset` cgroups as the target resources. 

In particular, you will learn how to:
- pin a process into a subset of CPUs to run on
- adjust the proportion of CPU cycles that a process gets over another

1. At first, inspect the contents of the `cpu` and `cpuset` groups. 
    ```
    ls /sys/fs/cgroup/cpu/
    ls /sys/fs/cgroup/cpuset/
    ```
    
    These are the "root" groups for `cpu` and `cpuset` subsystems, meaning that
    every process initially belongs there, since no special adjustments have been yet made 
    to the resource allocation of any process. The processes belonging to a cgroup is 
    registered in the `tasks` file: 
    ```
    cat /sys/fs/cgroup/cpu/tasks
    ```
    
    Under the `cpu` subsystem, you can see a number of tunable parameters, like `cpu.shares`.
    `cpu.shares` specifies a relative share of CPU time available to the tasks in a cgroup. 
    
    What is the current value of this parameter in the root group? 
    ```
    cat /sys/fs/cgroup/cpu/cpu.shares
    ```
    
    Similarly, `cpuset.cpus` specifies the CPUs of the platform where processes belonging to 
    the group are allowed to run. 
    
    Which are the CPUs that processes of the root group are allowed to run?
    ```
    cat /sys/fs/cgroup/cpuset/cpuset.cpus
    ```

1. Create two control groups under the `cpu` and `cpuset` subsystems, a __"realtime"__ and a __"batch"__, 
    making all the tunable parameters of the `cpu`,`cpuset` controllers writable by current user
    ```
    sudo cgcreate -a $USER -g cpu,cpuset:realtime
    sudo cgcreate -a $USER -g cpu,cpuset:batch
    ```
   
   Notice that two new subdirs have been created under the root hierarchies:
    ```
    ls /sys/fs/cgroup/cpu/
    ls /sys/fs/cgroup/cpuset/
    ```

   As no special adjustments have been yet made, the default values for `cpu.shares` should 
   be those of the parent (i.e. "root"), while `cpuset.cpus` should be empty. Verify it:
    ```
    cat /sys/fs/cgroup/cpu/realtime/cpu.shares
    cat /sys/fs/cgroup/cpuset/realtime/cpuset.cpus
    cat /sys/fs/cgroup/cpu/batch/cpu.shares
    cat /sys/fs/cgroup/cpuset/batch/cpuset.cpus
    ```

1. Modify both cgroups under the `cpuset` subsystem, so that tasks belonging to both of them 
   will run on __CPU 0 only__ . (NOTE: there aren't any tasks assigned to these groups yet)
  
    ```
    echo 0 > /sys/fs/cgroup/cpuset/realtime/cpuset.cpus 
    echo 0 > /sys/fs/cgroup/cpuset/batch/cpuset.cpus
    echo 0 > /sys/fs/cgroup/cpuset/realtime/cpuset.mem 
    echo 0 > /sys/fs/cgroup/cpuset/batch/cpuset.mem
    ```
    
    NOTE: the last 2 commands are mandatory for cpuset allocation to work correctly. They 
    specify that the tasks of the cgroups should be also bound to memory node 0. 

1. Launch two CPU intensive processes

    ```
    dd if=/dev/zero of=/dev/null &
    dd if=/dev/zero of=/dev/null &
    ```

  and get their PIDs
    ```
    pgrep -x dd
    ```

1. Move each process to a separate cgroup 
    ```
    sudo cgclassify -g cpu,cpuset:realtime <PID1>
    sudo cgclassify -g cpu,cpuset:batch <PID2>
    ```

    and inspect their CPU usage
    ```
    top
    ```

1. What is their CPU usage? 
    ```
    top
    ```

1. Change their CPU shares so that the process in the "realtime" group gets 75% of CPU 0 
   time, while the process in the "batch" group gets 25% of CPU 0 time:
    ```
    echo ??? > /sys/fs/cgroup/cpu/realtime/cpu.shares 
    echo ??? > /sys/fs/cgroup/cpu/batch/cpu.shares 
    ```
    
    What is their CPU usage now?
    ```
    top
    ```
    
    NOTE: if you were running the processes on a multicore VM with 2+ CPUs _without having adjusted 
    their allowed CPUs to CPU 0_, then you would see that both processes would get 100% of CPU time. 
    Why is that?
      
1. Stop processes and delete cgroups 

    ```
    killall dd 
    sudo cgdelete -g cpu,cpuset:realtime -g cpu,cpuset:batch
    ```
