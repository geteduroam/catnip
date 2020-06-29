catnip:
	pip3 install --upgrade -r requirements.txt -t ./catnip/

catnip.zip: lambda_function.py catnip
	cp lambda_function.py catnip/
	cd catnip; rm -f ../catnip.zip && zip -9 -r ../catnip.zip .
