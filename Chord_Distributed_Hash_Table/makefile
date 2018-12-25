init: FORCE
	./init nodes.txt

FORCE:

startServer:
ifndef port
	@echo '***** Error - No port defined in make command *****'
	@echo 'command is - python3 startServer port=<port>' 
endif
	python3 PythonServer.py $(port)

startClient:
ifndef serverIP
	@echo '***** Error - No serverIP defined in make command *****'
	@echo 'command is - python3 startClient serverIP=<server IP address> port=<port>' 
endif

ifndef port
	@echo '***** Error - No port defined in make command *****'
	@echo 'command is - python3 startClient serverIP=<server IP address> port=<port>' 
endif
	python3 PythonClient.py $(serverIP) $(port)
