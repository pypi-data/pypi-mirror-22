Internet
========

This module defines functions for enabling access to Internet domains. The
RESTful API uses these functions to generate a result. See the documentation for
each function and the unit tests for more information.

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

**Functions:**
--------------

### access_reCAPTCHA(site_key, url, \*\*agents)

Enables access to reCAPTCHA protected domains

**Args:**

|   Name   |  Type  |                    Description                    |
|----------|--------|---------------------------------------------------|
| site_key | String | The site key of the domain                        |
| url      | String | The URL of the domain                             |
| **agents | String | Key word arguments describing which agents to use |

**Returns:**

| Type  |                        Description                         |
|-------|------------------------------------------------------------|
| Tuple | A tuple containing a dictionary and the cost of the action |

Agents must be declared using the name of the module from which they are
located. The argument must be a dictionary containing the arguments you
would normally pass to instantiate that Agent.

Example:

	access_reCAPTCHA(
		'site key',
		'https://google.com'
		d3cryp7 = {'url': 'localhost'},
		rucaptcha = {'key': 'api key'}
	)


### access_solve_media(site_key, \*\*agents)

Enables access to Solve Media protected domains

**Args:**

|   Name   |  Type  |                    Description                    |
|----------|--------|---------------------------------------------------|
| site_key | String | The site key of the domain                        |
| **agents | String | Key word arguments describing which agents to use |

**Returns:**

| Type  |                        Description                         |
|-------|------------------------------------------------------------|
| Tuple | A tuple containing a dictionary and the cost of the action |

Agents must be declared using the name of the module from which they are
located. The argument must be a dictionary containing the arguments you
would normally pass to instantiate that Agent.

Example:

	access_solve_media(
		'site key',
		d3cryp7 = {'url': 'localhost'},
		rucaptcha = {'key': 'api key'}
	)
