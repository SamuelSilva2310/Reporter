# Report

## Working with ansible
All ansible playbook are stored in the *ansible/playboosk* directory

### **Running Setup**

The setup playbooks runs a number os tasks which will setup the project on all hosts

To run execute:
```sh
ansible-playbook -i <path_to_inventory.yml> <path_to_playbook_setup.yml>
```
The first time running this playbook we should see that ansible return **CHANGED** on some tasks.

After running again ansible should return **OK** on all tasks if no updates were made.


### **Starting Collector**

The collector is a python program which will be ran on all hosts at the same time and be stoped when needed.

To run execute:
```sh
ansible-playbook -i <path_to_inventory.yml> <path_to_playbook_run.yml>
```
Ansible will check if the program is already running on the hostm if not it will start the program and return **CHANGED**. If it is already running ansible will simply return **OK**


### **Stoping Collector**

When Stoping, ansible will make sure the collector is running on the host ans kill the process, after doing so it will collect all (.csv Export) from the hosts into a local folder.

To run execute:
```sh
ansible-playbook -i <path_to_inventory.yml> <path_to_playbook_stop.yml>
```
Ansible will check if the program is already running on the host, if it is, it kills the process, retrieves the (.csv Export) and returns **CHANGED**. If it is not running ansible will simply return **OK**.


## Create the Report

Finally, to create the report using all the exports from the hosts.

Execute the report maker main.py file:

```
python report_maker/main.py -i <input path for exports folder> -o <output filename of report>
```


