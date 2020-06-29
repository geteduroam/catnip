# Catnip

Inline eap-config converter, "temporary" solution to https://github.com/GEANT/CAT/pull/191

- Make sure pip3 is installed (https://pip.pypa.io/en/stable/installing/) and in PATH


## Running on Amazon Lambda

- Build a deployment .zip by running

		make catnip.zip

- In AWS, create an empty Lamba function
- In the section for Function code, upload your ZIP, Python 3.7 or higher and set handler to `lambda_function.lambda_handler` (the default)
