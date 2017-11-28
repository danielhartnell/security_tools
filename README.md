# autobounty

## Summary

Ultimately, I would like to use this tool to automate some of the common tasks
I perform when looking for security bug bounties.

### Monolith structure

- App organization partially modeled off Mozilla's Observatory scanner
- Web interface to inspect domains for an arbitrary company
- API for retrieving and storing domain objects and related data
- Celery for background scanning
- MongoDB for data storage
- Scanner
    - Retrieve a list of apex domains from DB
    - Run a full scan on each with Sublist3r
    - Subbrute dictionary attack on all subdomains

### DB structure

```
{
	"_id": ObjectId("5a0fe1766ad5f6b967c3ad7d"),
	"org": "New Relic",
	"fqdn": "www.newrelic.com",
	"status": {
		"active": True,
		"last_dns_resolution": "01-01-2017"
	}
}
```

#### Basic response collection

```
{
	"_id" : ObjectId("5a0fe1766ad5f6b967c3ad7d"),
	"responseHeaders": {
		"Server": "nginx",
		"Content-Type": "application/x-msdownload",
		"Status": "301 Moved Permanently",
		"Location": "http://newrelic.com/",
		"X-Rack-Cache": "miss",
		"X-Served-By": "cache-sea1026-SEA",
		"X-Timer": "S1511080259.204629,VS0,VE0"
	},
	"firstResponseCode": "301",
	"finalResponseCode": "200",
	"eachResponseCode": ["301", "301", "200"]
}
```

#### Directory enumeration

```
{
	"_id" : ObjectId("5a0fe1766ad5f6b967c3ad7d"),
	"scan_complete": True,
	"last_scan": "01-01-2017",
	"directories": [
		"/",
		"/assets",
		"/assets/images",
		"/assets/css",
		"/.git"
	],
	"files": [
		"/.git/.gitignore",
		"/assets/css/style.css",
		"/secret-backup.zip"
	]
}
```

#### Fingerprinting functionality and services

```
{
	"_id" : ObjectId("5a0fe1766ad5f6b967c3ad7d"),
	"services": {
		"SAML": {
			"active": True,
			"idp": "Auth0",
			"metadata_url": "/saml/metadata"
		},
		"www": {
			"server": "nginx",
			"version": "1.22.1",
		},
		"ports": [22, 80, 443]
	}
}
```

#### Known issues

```
{
	"_id" : ObjectId("5a0fe1766ad5f6b967c3ad7d"),
	"issues": {
		"open_redirect": True,
		"subdomain_hijacking": {
			"vulnerable": True,
			"service": "CloudFront",
			"response": "Unknown distribution ID"
		},
		"cves": [
			"cve123",
			"cve456",
			"cve789"
		]
	}
}
```

#### Ideas

- Keep webpage source to track diffs over time
- Extract new domains from CSP headers, HTML, etc.
    - If the domain uses the same nameservers, high likelihood that it is good
- Manipulate query parameters
- Think about how I want to keep records up to date without huge backlog
- Experiment with joining collections together
- Introduce notifcations
- Migrate the website to AWS and setup a CI/CD pipeline
- Introduce testing
- Sanitize user input
- Add authentication
- Create docker-compose setup with Redis, MongoDB and celery workers for test
- Plan the introduction of new scans to make it easy
- Aggregate response times and feature flags
- Attempt to infer deployment schedule
- Cleanup Sublist3r and subbrute integration
- Make sure both do not use multiprocess
- Setup an additional listener for host header injection
    - Do what Burp does
    - Set a unique host header for the transaction
    - Listen for connections from reverse proxies or other nodes
- Support uploading a list of domains for scanning
- Create a configuration page
- Configs should be scoped to one or more domains
- Check for open redirects
- Moderately passive, quick, opportunity to infer and identify behavior
- Change content type and test for XXE
-