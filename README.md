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
