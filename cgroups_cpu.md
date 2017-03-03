# Cgroups

The goal of this hands-on session is to get familiar with configuring cgroups to control 
resource allocation to processes. We will use the `cpu` cgroup as the target resources. 

In particular, you will learn how to adjust the proportion of CPU cycles that a process gets over another.

1. At first, inspect the contents of the `cpu` group 
    ```
    ls /sys/fs/cgroup/cpu/
    ```
    
    This is the "root" group for the `cpu` subsystem, meaning that
    every process initially belongs there, since no special adjustments have been yet made 
    to change the portion of CPU time that processes get. 
    The processes belonging to a cgroup are registered in the `tasks` file, so initially the 
    following file should contain all the PIDs of the system: 
    ```
    cat /sys/fs/cgroup/cpu/tasks
    ```
    
    Under the `cpu` subsystem, you can see a number of tunable parameters, like `cpu.shares`.
    `cpu.shares` specifies a relative share of CPU time available to the tasks in a cgroup. 
    
    What is the current value of this parameter in the root group? 
    ```
    cat /sys/fs/cgroup/cpu/cpu.shares
    ```

1. Create two control groups under the `cpu` subsystem, a __"realtime"__ and a __"batch"__, 
    making all the tunable parameters of the `cpu` subsystem writable by current user
    ```
    sudo cgcreate -a $USER -g cpu:realtime
    sudo cgcreate -a $USER -g cpu:batch
    ```
   
   Notice that two new subdirs have been created under the root cpu hierarchy:
    ```
    ls /sys/fs/cgroup/cpu/
    ```

   As no special adjustments have been yet made, the default values for `cpu.shares` should 
   be those of the parent (i.e. "root"). Verify it:
    ```
    cat /sys/fs/cgroup/cpu/realtime/cpu.shares
    cat /sys/fs/cgroup/cpu/batch/cpu.shares
    ```

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
    sudo cgclassify -g cpu:realtime <PID1>
    sudo cgclassify -g cpu:batch <PID2>
    ```

    What is their CPU usage? 
    ```
    top
    ```

1. Change their CPU shares so that the process in the "realtime" group gets 75% of CPU 0 
   time, while the process in the "batch" group gets 25% of CPU 0 time. 
   
   NOTE: it is the relative weights of `cpu.shares` that matter, not their absolute values. 
    ```
    echo ??? > /sys/fs/cgroup/cpu/realtime/cpu.shares 
    echo ??? > /sys/fs/cgroup/cpu/batch/cpu.shares 
    ```
    
    What is their CPU usage now?
    ```
    top
    ```
         
1. Stop processes and delete cgroups 

    ```
    killall dd 
    sudo cgdelete -g cpu:realtime -g cpu:batch
    ```
