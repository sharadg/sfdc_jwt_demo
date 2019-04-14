# Python code for OAuth 2.0 JWT Bearer Token Flow with Salesforce 

This repo contains example source code for creating a connected app in salesforce and using JWT (JSON Web Token) Bearer Token Flow.

More details can be found [here](https://help.salesforce.com/articleView?id=remoteaccess_oauth_jwt_flow.htm&type=5)

## Dependencies
 - Credhub Service Broker for PCF. [Docs](https://docs.pivotal.io/credhub-service-broker/index.html)
 - Connected App that has already been registered in your Salesforce account and is set up to authenticate using OAuth JWT Tokens

## Testing in your environment
1. Create a Credhub Service Instance  
```less
cf create-service credhub default demo-credhub -c '{"demo-key": "demo-value"}'
```
2. Generate a Certificate & Private Key   
(I am using `credhub generate` to generate these in my environment but you can use any other tool like `keygen` or `openssl`)
```less
credhub generate -t certificate -n /demo/certificate -d 730 -c home.pcfdot.com -o Pivotal -u PA_South_Central -i Dallas -s TX -y US --self-sign
```
3. Update your credhub service instance with these credentials
- Retrive the generated credentials
```less
credhub get -n /demo/certificate -j
{
	"id": "7e383b52-bfb1-475c-a75f-d85b7647a880",
	"name": "/demo/certificate",
	"type": "certificate",
	"value": {
		"ca": "-----BEGIN CERTIFICATE-----<snipped>-----END CERTIFICATE-----\n",
		"certificate": "-----BEGIN CERTIFICATE-----<snipped>-----END CERTIFICATE-----\n",
		"private_key": "-----BEGIN RSA PRIVATE KEY-----<snipped>-----END RSA PRIVATE KEY-----\n"
	},
	"version_created_at": "2019-04-13T02:52:16Z"
}
```
- Update credhub service instance
```less
- cf update-service demo-credhub -c '{"demo-certificate": {
        "id": "7e383b52-bfb1-475c-a75f-d85b7647a880",
        "name": "/demo/certificate",
        "type": "certificate",
        "value": {
                "ca": "-----BEGIN CERTIFICATE-----<snipped>-----END CERTIFICATE-----\n",
                "certificate": "-----BEGIN CERTIFICATE-----<snipped>-----END CERTIFICATE-----\n",
                "private_key": "-----BEGIN RSA PRIVATE KEY-----<snipped>-----END RSA PRIVATE KEY-----\n"
        },
        "version_created_at": "2019-04-13T02:52:16Z"
}}'
```
4. `cf push` the app and hit the `/` endpoint which will print out the JWT Claim, Signed Claim and Received response
```less
cf push                                                                                                                                                                                                                       ⏎ ✹ ✚ ✭
Pushing from manifest to org westeros / space iron_throne as admin...
Using manifest file /Users/sgupta/development/python/sfdc_jwt_demo/manifest.yml
Deprecation warning: Use of 'buildpack' attribute in manifest is deprecated in favor of 'buildpacks'. Please see http://docs.cloudfoundry.org/devguide/deploy-apps/manifest.html#deprecated for alternatives and other app manifest deprecations. This feature will be removed in the future.

Getting app info...
Creating app with these attributes...
+ name:         sfdc_jwt_demo
  path:         /Users/sgupta/development/python/sfdc_jwt_demo
  buildpacks:
+   python_buildpack
+ disk quota:   1G
+ memory:       512M
  services:
+   demo-credhub
  routes:
+   sfdcjwtdemo.apps.home.pcfdot.com

Creating app sfdc_jwt_demo...
Mapping routes...
Binding services...
Comparing local files to remote cache...
Packaging files to upload...
Uploading files...
 4.53 MiB / 4.53 MiB [============================================================================================================================================================================================================] 100.00% 1s

Waiting for API to complete processing files...

Staging app and tracing logs...
   Downloading python_buildpack...
   Downloaded python_buildpack
   Cell 09742dc6-63c7-4b6f-96b8-f6763b0f8309 creating container for instance e8f1af1d-8434-4e33-b6ea-d7483fce889f
   Cell 09742dc6-63c7-4b6f-96b8-f6763b0f8309 successfully created container for instance e8f1af1d-8434-4e33-b6ea-d7483fce889f
   Downloading app package...
   Downloaded app package (6.5M)
   -----> Python Buildpack version 1.6.29
          **WARNING** [DEPRECATION WARNING]:
          **WARNING** Please use AppDynamics extension buildpack for Python Application instrumentation
          **WARNING** for more details: https://docs.pivotal.io/partners/appdynamics/multibuildpack.html
   -----> Supplying Python
   -----> Installing python 3.7.2
          Copy [/tmp/buildpacks/bd8c6bdbf926d0d302e7adc6f3c26cac/dependencies/b12389f89bb6014c36a5667d8b4c49c1/python-3.7.2-linux-x64-cflinuxfs3-2b800c6f.tgz]
   -----> Installing pip-pop 0.1.3
          Copy [/tmp/buildpacks/bd8c6bdbf926d0d302e7adc6f3c26cac/dependencies/859523d4d2137906b68eb4c8951d56b3/pip-pop-0.1.3-fc106ef6.tar.gz]
   -----> Running Pip Install
          Collecting certifi==2019.3.9 (from -r /tmp/app/requirements.txt (line 1))
            Downloading https://files.pythonhosted.org/packages/60/75/f692a584e85b7eaba0e03827b3d51f45f571c2e793dd731e598828d380aa/certifi-2019.3.9-py2.py3-none-any.whl (158kB)
          Collecting cfenv==0.5.3 (from -r /tmp/app/requirements.txt (line 2))
            Downloading https://files.pythonhosted.org/packages/15/b0/5fc4d8dc9fd0807b240cab217c26bb8a37ca22e8f86d0b0e896e6fc16655/cfenv-0.5.3-py2.py3-none-any.whl
          Collecting chardet==3.0.4 (from -r /tmp/app/requirements.txt (line 3))
            Downloading https://files.pythonhosted.org/packages/bc/a9/01ffebfb562e4274b6487b4bb1ddec7ca55ec7510b22e4c51f14098443b8/chardet-3.0.4-py2.py3-none-any.whl (133kB)
          Collecting Click==7.0 (from -r /tmp/app/requirements.txt (line 4))
            Downloading https://files.pythonhosted.org/packages/fa/37/45185cb5abbc30d7257104c434fe0b07e5a195a6847506c074527aa599ec/Click-7.0-py2.py3-none-any.whl (81kB)
          Collecting Flask==1.0.2 (from -r /tmp/app/requirements.txt (line 5))
            Downloading https://files.pythonhosted.org/packages/7f/e7/08578774ed4536d3242b14dacb4696386634607af824ea997202cd0edb4b/Flask-1.0.2-py2.py3-none-any.whl (91kB)
          Collecting furl==2.0.0 (from -r /tmp/app/requirements.txt (line 6))
            Downloading https://files.pythonhosted.org/packages/bd/b6/302ecc007de38274509d6397300afd2e274aba7f1c3c0a165b5f1e1a836a/furl-2.0.0-py2.py3-none-any.whl
          Collecting gunicorn==19.9.0 (from -r /tmp/app/requirements.txt (line 7))
            Downloading https://files.pythonhosted.org/packages/8c/da/b8dd8deb741bff556db53902d4706774c8e1e67265f69528c14c003644e6/gunicorn-19.9.0-py2.py3-none-any.whl (112kB)
          Collecting idna==2.8 (from -r /tmp/app/requirements.txt (line 8))
            Downloading https://files.pythonhosted.org/packages/14/2c/cd551d81dbe15200be1cf41cd03869a46fe7226e7450af7a6545bfc474c9/idna-2.8-py2.py3-none-any.whl (58kB)
          Collecting itsdangerous==1.1.0 (from -r /tmp/app/requirements.txt (line 9))
            Downloading https://files.pythonhosted.org/packages/76/ae/44b03b253d6fade317f32c24d100b3b35c2239807046a4c953c7b89fa49e/itsdangerous-1.1.0-py2.py3-none-any.whl
          Collecting Jinja2==2.10.1 (from -r /tmp/app/requirements.txt (line 10))
            Downloading https://files.pythonhosted.org/packages/1d/e7/fd8b501e7a6dfe492a433deb7b9d833d39ca74916fa8bc63dd1a4947a671/Jinja2-2.10.1-py2.py3-none-any.whl (124kB)
          Collecting MarkupSafe==1.1.1 (from -r /tmp/app/requirements.txt (line 11))
            Downloading https://files.pythonhosted.org/packages/98/7b/ff284bd8c80654e471b769062a9b43cc5d03e7a615048d96f4619df8d420/MarkupSafe-1.1.1-cp37-cp37m-manylinux1_x86_64.whl
          Collecting orderedmultidict==1.0 (from -r /tmp/app/requirements.txt (line 12))
            Downloading https://files.pythonhosted.org/packages/05/70/9f0a8867d4d98becf60dc5707e10b39930747ee914dae46414b69e33a266/orderedmultidict-1.0-py2.py3-none-any.whl
          Collecting pycrypto==2.6.1 (from -r /tmp/app/requirements.txt (line 13))
            Downloading https://files.pythonhosted.org/packages/60/db/645aa9af249f059cc3a368b118de33889219e0362141e75d4eaf6f80f163/pycrypto-2.6.1.tar.gz (446kB)
          Collecting requests==2.21.0 (from -r /tmp/app/requirements.txt (line 14))
            Downloading https://files.pythonhosted.org/packages/7d/e3/20f3d364d6c8e5d2353c72a67778eb189176f08e873c9900e10c0287b84b/requests-2.21.0-py2.py3-none-any.whl (57kB)
          Collecting six==1.12.0 (from -r /tmp/app/requirements.txt (line 15))
            Downloading https://files.pythonhosted.org/packages/73/fb/00a976f728d0d1fecfe898238ce23f502a721c0ac0ecfedb80e0d88c64e9/six-1.12.0-py2.py3-none-any.whl
          Collecting urllib3==1.24.1 (from -r /tmp/app/requirements.txt (line 16))
            Downloading https://files.pythonhosted.org/packages/62/00/ee1d7de624db8ba7090d1226aebefab96a2c71cd5cfa7629d6ad3f61b79e/urllib3-1.24.1-py2.py3-none-any.whl (118kB)
          Collecting Werkzeug==0.15.2 (from -r /tmp/app/requirements.txt (line 17))
            Downloading https://files.pythonhosted.org/packages/18/79/84f02539cc181cdbf5ff5a41b9f52cae870b6f632767e43ba6ac70132e92/Werkzeug-0.15.2-py2.py3-none-any.whl (328kB)
          Installing collected packages: certifi, six, orderedmultidict, furl, cfenv, chardet, Click, Werkzeug, itsdangerous, MarkupSafe, Jinja2, Flask, gunicorn, idna, pycrypto, urllib3, requests
            The script chardetect is installed in '/tmp/contents426746685/deps/0/python/bin' which is not on PATH.
            Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
            The script flask is installed in '/tmp/contents426746685/deps/0/python/bin' which is not on PATH.
            Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
            The scripts gunicorn and gunicorn_paster are installed in '/tmp/contents426746685/deps/0/python/bin' which is not on PATH.
            Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
            Running setup.py install for pycrypto: started
              Running setup.py install for pycrypto: finished with status 'done'
          Successfully installed Click-7.0 Flask-1.0.2 Jinja2-2.10.1 MarkupSafe-1.1.1 Werkzeug-0.15.2 certifi-2019.3.9 cfenv-0.5.3 chardet-3.0.4 furl-2.0.0 gunicorn-19.9.0 idna-2.8 itsdangerous-1.1.0 orderedmultidict-1.0 pycrypto-2.6.1 requests-2.21.0 six-1.12.0 urllib3-1.24.1
          You are using pip version 18.1, however version 19.0.3 is available.
          You should consider upgrading via the 'pip install --upgrade pip' command.
   Exit status 0
   Uploading droplet, build artifacts cache...
   Uploading build artifacts cache...
   Uploading droplet...
   Uploaded build artifacts cache (1.8M)
   Uploaded droplet (58.9M)
   Uploading complete
   Cell 09742dc6-63c7-4b6f-96b8-f6763b0f8309 stopping instance e8f1af1d-8434-4e33-b6ea-d7483fce889f
   Cell 09742dc6-63c7-4b6f-96b8-f6763b0f8309 destroying container for instance e8f1af1d-8434-4e33-b6ea-d7483fce889f

Waiting for app to start...

name:              sfdc_jwt_demo
requested state:   started
routes:            sfdcjwtdemo.apps.home.pcfdot.com
last uploaded:     Sun 14 Apr 15:26:36 CDT 2019
stack:             cflinuxfs3
buildpacks:        python

type:            web
instances:       1/1
memory usage:    512M
start command:   gunicorn -w 4 -t 600 sfdc_jwt_demo:app
     state     since                  cpu    memory          disk           details
#0   running   2019-04-14T20:26:50Z   0.0%   57.3M of 512M   212.5M of 1G
```
5. Try the URL in browser or using `curl` or `http`
```less
http -v --verify=no https://sfdcjwtdemo.apps.home.pcfdot.com                                                                                                                                                                  ⏎ ✹ ✚ ✭
GET / HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Host: sfdcjwtdemo.apps.home.pcfdot.com
User-Agent: HTTPie/1.0.2



HTTP/1.1 200 OK
Content-Length: 2302
Content-Type: application/json
Date: Sun, 14 Apr 2019 20:29:25 GMT
Server: gunicorn/19.9.0
X-Vcap-Request-Id: 1ab385f5-7476-40b0-4bce-20582e47df31

{
    "claim": "eyJhbGciOiJSUzI1NiJ9.eyJpc3MiOiAiM01WRzlaRjRic18uTUt1aXlScTlKMWwzM09BUjBqRm9RYmt4MWFtNEJ6aDVWRFUxTDVvU0I1MDBkeEtUd29iU1BBN051YVZnbDhWV3dXVjV0cF9WZyIsICJzdWIiOiAic2hndXB0YV9kZXZAcGl2b3RhbC5pbyIsICJhdWQiOiAiaHR0cHM6Ly9sb2dpbi5zYWxlc2ZvcmNlLmNvbSIsICJleHAiOiAxNTU1Mjc0MDY1fQ",
    "response_headers": {
        "Cache-Control": "no-cache,must-revalidate,max-age=0,no-store,private",
        "Content-Encoding": "gzip",
        "Content-Type": "application/json;charset=UTF-8",
        "Date": "Sun, 14 Apr 2019 20:29:25 GMT",
        "Expires": "Thu, 01 Jan 1970 00:00:00 GMT",
        "Set-Cookie": "BrowserId=3foRzQsDTfuKV3cawiLH-Q;Path=/;Domain=.salesforce.com;Expires=Thu, 13-Jun-2019 20:29:25 GMT;Max-Age=5184000, BrowserId=mRsLzCspRCGDw-YBByvG_w;Path=/;Domain=.salesforce.com;Expires=Thu, 13-Jun-2019 20:29:25 GMT;Max-Age=5184000",
        "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
        "Transfer-Encoding": "chunked",
        "Vary": "Accept-Encoding",
        "X-Content-Type-Options": "nosniff",
        "X-XSS-Protection": "1; mode=block"
    },
    "response_text": {
        "access_token": "00D2E000000ncKP!AQ4AQGLaeVPC1xft5DR1.yWAo3a5NbzC1qxBvq58i6Exm5e1oXKmzEm5Nh0bS__mxqqFIS6ddjZSGni3hNC6jKcUDzw2sKus",
        "id": "https://login.salesforce.com/id/00D2E000000ncKPUAY/0052E00000IMbxTQAT",
        "instance_url": "https://na91.salesforce.com",
        "scope": "visualforce web openid api id full",
        "token_type": "Bearer"
    },
    "signed_claim": "lAIWj-1EVxor-DckleFstxyE-opwyQw9hjTZsyyVw4jeGsywVH-h9L7uAB37kE7ppBMNPlgrRgfqSeVv8hI1uXHmAimOoUAx3EMXRWzELKU3qOD0YtxNN9jMtdhcR5txwV7theIa9MmFFJSWvADXrSeZsCFng1v_xz4JS2T-mX66yP5YgKHEXZ4fEHdoNZHEF8YL4m7x06W9JJpoy52iOJ_aDhH1vDO-dEMc126vp19tJk6gwp-LwAQ7BqEQqDl-Y1vJ6ZsktZwyelMhzI742RlyE6KY6TOgSWYBhd8x-UJ9i3BxSP-GLXXB-6fdwU3B84udG2x0VJWZIG6k2BDP4w",
    "target_payload": "eyJhbGciOiJSUzI1NiJ9.eyJpc3MiOiAiM01WRzlaRjRic18uTUt1aXlScTlKMWwzM09BUjBqRm9RYmt4MWFtNEJ6aDVWRFUxTDVvU0I1MDBkeEtUd29iU1BBN051YVZnbDhWV3dXVjV0cF9WZyIsICJzdWIiOiAic2hndXB0YV9kZXZAcGl2b3RhbC5pbyIsICJhdWQiOiAiaHR0cHM6Ly9sb2dpbi5zYWxlc2ZvcmNlLmNvbSIsICJleHAiOiAxNTU1Mjc0MDY1fQ.lAIWj-1EVxor-DckleFstxyE-opwyQw9hjTZsyyVw4jeGsywVH-h9L7uAB37kE7ppBMNPlgrRgfqSeVv8hI1uXHmAimOoUAx3EMXRWzELKU3qOD0YtxNN9jMtdhcR5txwV7theIa9MmFFJSWvADXrSeZsCFng1v_xz4JS2T-mX66yP5YgKHEXZ4fEHdoNZHEF8YL4m7x06W9JJpoy52iOJ_aDhH1vDO-dEMc126vp19tJk6gwp-LwAQ7BqEQqDl-Y1vJ6ZsktZwyelMhzI742RlyE6KY6TOgSWYBhd8x-UJ9i3BxSP-GLXXB-6fdwU3B84udG2x0VJWZIG6k2BDP4w"
}
```