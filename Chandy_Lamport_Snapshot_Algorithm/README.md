## CS557 : Programming Assignment 3 : Distributed Banking Application
------------------------------------------------------------------------------------------------------------------

* Command to run Bank Controller:
    * make start_controller balance=\<5000> filename=\<branches.txt>

* Command to run Bank Branch:
    * make start_branch bname=\<branch1> port=\<9091> interval=\<1000>

------------------------------------------------------------------------------------------------------------------

* Pragramming Language:
	* PYTHON3

------------------------------------------------------------------------------------------------------------------

* Tasks done by Dipika Suresh Patil:
	* Implementation of Branch Socket.
	* Implementation of communication between controller and branches.
	* Implementation of InitBranch message between controller and branches.
	* Implementation to setup Duplex connection between all branches in the system.
	* Implementation of transfer amount functionality.
	* Implementation of Transfer and Receive money within bank branches.

* Tasks done by Nitesh Mishra:
	* Implementation of InitSnapshot at Controller side.
	* Partial implementation of InitSnapshot in BankBranch.
	* Implementation of InitSnapshot, RetrieveSnapshot and ReturnSnapshot functionalities.
	* Fixed bug to increase local balance atomically within branch.
	* Added some useful debug messages to replicate the Packet Loss in TCP connections.
	* Fixed receive bandwidth to 10000 and backlog count to 100 in order to prevent message loss.
	* Include _VarintEncoder and _DecodeVarint to fix lost update issue.

------------------------------------------------------------------------------------------------------------------

* Completion status of the assignment: **FULL IMPLEMENTATION**
	* Tested all the required functionalities with variable number of bank branches and random time_interval.

------------------------------------------------------------------------------------------------------------------
