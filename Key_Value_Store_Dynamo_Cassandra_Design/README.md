## CS557 : Programming Assignment 4 : Key-Value Store with Configurable Consistency
------------------------------------------------------------------------------------------------------------------

* **Command to generate Python Code from replica.proto file**:
	* protoc --python_out=./ KeyValueStore.proto

* **Command to run Replica Key-Value Store Server**:
	* **make start_replica name=\<Replica0> port=\<9090> consistency_mechanism=\<"Read_Repair" OR "Hinted_Handoff"> filename=\<list_replicas.txt> use_file=\<yes OR no>**
	* Examples:
		* make start_replica name=Replica0 port=9090 consistency_mechanism=Read_Repair filename=list_replicas.txt use_file=no
		* make start_replica name=Replica0 port=9090 consistency_mechanism=Hinted_Handoff filename=list_replicas.txt use_file=no
		* make start_replica name=Replica0 port=9090 consistency_mechanism=Read_Repair filename=list_replicas.txt use_file=yes
		* make start_replica name=Replica0 port=9090 consistency_mechanism=Hinted_Handoff filename=list_replicas.txt use_file=yes

* **Command to setup Replicas Connections with each other**:
	* **make setup_connection filename=\<list_replicas.txt>**
	* Example:
		* make setup_connection filename=list_replicas.txt

* **Command to run the Client**:
	* **make start_client coordinator_ip=\<10.33.1.96> coordinator_port=\<9090>**
	* Example:
		* make start_client coordinator_ip=10.33.1.96 coordinator_port=9090

------------------------------------------------------------------------------------------------------------------

* Pragramming Language:
	* PYTHON3

------------------------------------------------------------------------------------------------------------------

* Tasks done by **Dipika Suresh Patil**:
	* Implementation of key-value store - Initial replica setups.
	* Partial Implementation of basic client coordinator connectivity.
	* Partial implementation to handle replica request.
	* Implementation of GET and PUT requests between replica without RR and HH mechanisms.
	* Partial code for Read_Repair functionality.
	* Implementation of HintedHandoff mechanism with testing.

* Tasks done by **Nitesh Mishra**:
	* Implementation of connection setup between replicas (Full Duplex).
	* Implementation of one-client and one-coordinator with basic testing.
	* Change in design not to create FULL-DUPLEX sockets - not to save sockets.
	* Implementation of Read_Repair functionality with testing.
	* Partial implementation of Hinted Handoff mechanism.

------------------------------------------------------------------------------------------------------------------

* Completion status of the assignment: 
	* Tested all the required functionalities with Hinted-Handoff and Read-Repair consistency mechanisms.

------------------------------------------------------------------------------------------------------------------
