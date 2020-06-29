import requests
import json
from itertools import chain

def fix_geant(auth_methods):
	eap_mschap = '<EAPMethod><Type>26</Type></EAPMethod>'
	noneap_mschap = '<NonEAPAuthMethod><Type>3</Type></NonEAPAuthMethod>'

	for auth_method in auth_methods:
		if '<EAPMethod><Type>21</Type></EAPMethod>' in auth_method:
			yield auth_method.replace(eap_mschap, noneap_mschap)
		else:
			yield auth_method

def error(message):
	return {
		'statusCode': 200,
		'body': message + "\n",
		'headers': {
			'Content-Type': 'text/plain',
			'Cache-Control': 'no-store',
		}
	}

def lambda_handler(event, context):
	e = event
	e = e.get('headers', e)
	e = e.get('requestContext', e)
	e = e.get('http', e.get('identity', e))
	ip = e.get('sourceIp', e.get('X-Forwarded-For', e.get('x-forwarded-for', '')))

	q = event.get('queryStringParameters', {})
	if q.get('action', '') != 'downloadInstaller':
		return error('Missing action=downloadInstaller')
	if q.get('device', '') != 'eap-config':
		return error('Missing device=eap-config')
	p = q.get('profile', 'NaN')
	try:
		profile = int(p)
	except ValueError:
		return error('Expecting profile=')

	url = 'https://cat.eduroam.org/user/API.php?action=downloadInstaller&device=eap-config&profile=' + p
	r = requests.get(url, headers={
		'Accept': 'application/eap-config',
		'User-Agent': 'python/requests catnip eap-config proxy',
		'X-Forwarded-For': ip
	})

	eapConfig = str(r.text)
	delim = '</AuthenticationMethod>'
	*auth_methods, rest = eapConfig.split(delim)
	eapConfigConverted = delim.join(chain(fix_geant(auth_methods), [rest]))
	headers = dict(r.headers)
	headers['Content-Length'] = len(eapConfigConverted)

	return {
		'statusCode': int(r.status_code),
		'headers': headers,
		'body': eapConfigConverted,
	}
