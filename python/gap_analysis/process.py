import json
import unittest


def processSwaggerRecord(jsonData):
    swaggerSpecs = []
    for path, spec in jsonData['paths'].items():
        for pathType, apiData in spec.items():
            record = {}
            record['url'] = path
            record['type'] = pathType.upper()
            record['summary'] = ''
            if 'summary' in apiData:
                record['summary'] = apiData['summary'].strip()
            record['description'] = ''
            record['permissions'] = ''
            if 'description' in apiData:
                description = apiData['description'].strip()
                record['description'] = description
                permissionTag = "Permissions Required: "
                permissionsIndex = description.find(permissionTag)
                if (permissionsIndex > -1):
                    codeIndex = description.find("<code>", permissionsIndex)
                    if (codeIndex > -1):
                        record['permissions'] = description[codeIndex + 6 : description.find("</code>", permissionsIndex + len(permissionTag))]
                    else:
                        record['permissions'] = description[permissionsIndex + len(permissionTag) : description.find("</p>")]
            record['Total'] = 0
            record['applications'] = ''
            record['permissions check'] = ''
            #print(path + "\t" + pathType)
            swaggerSpecs.append(record)
    return swaggerSpecs


def extractPostmanRecord(postmanRequest):
    record = {}
    record['name'] = postmanRequest['name']
    record['type'] = postmanRequest['request']['method']
    #print(record['name'] + '\t' + record['type'])
    rawUrl = postmanRequest['request']['url']['raw']
    queryIndex = rawUrl.find('?')
    record['queryString'] = ''
    if (queryIndex > -1):
        record['queryString'] = rawUrl[queryIndex+1:]
        rawUrl = rawUrl[0:queryIndex]

    record['url'] = rawUrl[rawUrl.find('/'):]
    #record['pathParts'] = request['request']['url']['path']
    return record


def requestsMatch(swaggerAPI, postmanRequest):
    if ( (postmanRequest['type'] != None) and (swaggerAPI['type'] != postmanRequest['type']) ):
        return False
    if (swaggerAPI['url'] == postmanRequest['url']):
        return True
    #
    ## fuzzy url matching
    swaggerIndex = swaggerAPI['url'].find("/{")
    postmanIndex = postmanRequest['url'].find("/{{")
    if (swaggerIndex > -1):
        swaggerUrl = swaggerAPI['url'][0:swaggerIndex]
        if (postmanIndex > -1):
            postmanUrl = postmanRequest['url'][0:postmanIndex]
            if (swaggerUrl == postmanUrl):
                return True
        else:
            postmanUrl = postmanRequest['url'][0:len(swaggerUrl)]
            if (swaggerUrl == postmanUrl):
                return True
    return False


class TestExtractSwaggerRecord(unittest.TestCase):
    def test_1(self):

        swaggerJSON = """{
        "info": {"title":"","description":"","version":"1.2.3","x-ISC_Namespace":"DEFAULT"},
        "paths": {
            "/login/{app}": {
              "post": {
              "description":" This is a sample API description. <p>Permissions Required: (Authentication only)</p> ",
              "summary": " Deprecated ",
              "operationId": "Login",
              "x-ISC_CORS": false,
              "x-ISC_ServiceMethod": "Login",
              "parameters":[
                {"name":"app","in":"path","required":true,"type":"string"},
                {"name":"payloadBody","in":"body","description":"Request body contents","required":false,"schema":{"type":"string"}}
              ],
              "responses":{"default":{"description":"(Unexpected Error)"},"200":{"description":"(Expected Result)"}}
            }},
            "/patient/addPatient": {
              "post":{"operationId":"AddPatient",
                "description":" <p>Permissions Required: <code>%%addPatient</code></p> ","x-ISC_ServiceMethod":"NewPatient","x-ISC_CORS":true,
                "parameters":[{"name":"payloadBody","in":"body","description":"Request body contents","required":false,"schema":{"type":"string"}}],
                "responses":{"default":{"description":"(Unexpected Error)"},"200":{"description":"(Expected Result)"}}
              }
            }
        }}
        """

        records = processSwaggerRecord(json.loads(swaggerJSON))
        self.assertEqual(len(records), 2)

        record = records[0]
        self.assertEqual(record['type'], 'POST')
        self.assertEqual(record['url'], '/login/{app}')
        self.assertEqual(record['summary'], 'Deprecated')
        self.assertEqual(record['description'], 'This is a sample API description. <p>Permissions Required: (Authentication only)</p>')
        self.assertEqual(record['permissions'], '(Authentication only)')

        record = records[1]
        self.assertEqual(record['type'], 'POST')
        self.assertEqual(record['url'], '/patient/addPatient')
        self.assertEqual(record['summary'], '')
        self.assertEqual(record['description'], '<p>Permissions Required: <code>%%addPatient</code></p>')
        self.assertEqual(record['permissions'], '%%addPatient')



class TestExtractPostmanRecord(unittest.TestCase):
    def test_1(self):

        postmanJSON = """{
            "name": "Testing - Non-existant user",
            "protocolProfileBehavior": {"disableBodyPruning": true},
            "request": {
                "auth": {"type": "oauth2"},
                "method": "GET",
                "header": [{
                        "key": "namespace",
                        "type": "text",
                        "value": "generic"
                }],
                "body": {
                    "mode": "urlencoded",
                    "urlencoded": []
                },
                "url": {
                    "raw": "{{url}}/user/getUser/Id?EmailAddress=bogus.email@example.com",
                    "host": ["{{url}}"],
                    "path": ["user","getUser","Id"],
                    "query": [{"key": "EmailAddress","value": "bogus.email@example.com"}]
                }
            },
            "response": []
        }
        """

        record = extractPostmanRecord(json.loads(postmanJSON))
        self.assertEqual(record['type'], 'GET')
        self.assertEqual(record['name'], 'Testing - Non-existant user')
        self.assertEqual(record['url'], '/user/getUser/Id')
        self.assertEqual(record['queryString'], 'EmailAddress=bogus.email@example.com')


class TestRequestsMatch(unittest.TestCase):
    def test_DifferentPostType(self):
        swaggerEntry = { 'type': 'GET', 'url': '/static/path' }
        postmanEntry = { 'type': 'POST', 'url': '/static/path' }
        self.assertFalse(requestsMatch(swaggerEntry, postmanEntry))

    def test_ExactMatch(self):
        swaggerEntry = { 'type': 'POST', 'url': '/static/path' }
        postmanEntry = { 'type': 'POST', 'url': '/static/path' }
        self.assertTrue(requestsMatch(swaggerEntry, postmanEntry))

    def test_DynamicURLs(self):
        swaggerEntry = { 'type': 'POST', 'url': '/static/path/{dynamicID}' }
        postmanEntry = { 'type': 'POST', 'url': '/static/path/{{dynamicID}}' }
        self.assertTrue(requestsMatch(swaggerEntry, postmanEntry))

    def test_DynamicURLwithHardcodedID(self):
        swaggerEntry = { 'type': 'POST', 'url': '/static/path/{dynamicID}' }
        postmanEntry = { 'type': 'POST', 'url': '/static/path/hardcodedID' }
        self.assertTrue(requestsMatch(swaggerEntry, postmanEntry))

    def test_MatchNoType(self):
        swaggerEntry = { 'type': 'POST', 'url': '/static/path/{dynamicID}' }
        otherEntry = { 'type': None, 'url': '/static/path' }
        self.assertTrue(requestsMatch(swaggerEntry, otherEntry))

    def test_NoMatch1(self):
        swaggerEntry = { 'type': 'POST', 'url': '/static/path' }
        postmanEntry = { 'type': 'POST', 'url': '/static/path/foo' }
        self.assertFalse(requestsMatch(swaggerEntry, postmanEntry))

    def test_NoMatch2(self):
        swaggerEntry = { 'type': 'POST', 'url': '/static/path/{dynamicID}' }
        postmanEntry = { 'type': 'POST', 'url': '/static/hardcodedID' }
        self.assertFalse(requestsMatch(swaggerEntry, postmanEntry))

    def test_NoMatchNoType(self):
        swaggerEntry = { 'type': 'POST', 'url': '/static/path/{dynamicID}' }
        otherEntry = { 'type': None, 'url': '/static/hardcodedID' }
        self.assertFalse(requestsMatch(swaggerEntry, otherEntry))
