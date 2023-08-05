envassume
=========

Assume an AWS IAM role from AWS API credentials in environment variables.

Usage
-----

::

    usage: envassume [-h] [-i EXTERNAL_ID] [ARN] command [argument [argument ...]]

    optional arguments:
        -h, --help              show this help message and exit
        -i, --id EXTERNAL_ID    external id
        ARN                     AWS role ARN to assume (required if not set by environment variable)

    environment variables:
        environment must contain valid AWS API credentials

        AWS_ASSUME_ROLE=ARN
            no options can be present before the command if this is defined

        AWS_ASSUME_ID=EXTERNAL_ID

License
-------

Copyright (c) 2017 Warren Moore

This software may be redistributed under the terms of the MIT License.
See the file LICENSE for details.

Contact
-------

::

          @wamonite     - twitter
           \_______.com - web
    warren____________/ - email
