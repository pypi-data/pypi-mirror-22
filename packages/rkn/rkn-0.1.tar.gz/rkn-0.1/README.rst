Description
-----------

This module provide only one function: it check if domain is listed on http://eais.rkn.gov.ru/

You need anti-captcha.com API key for using this module.

Example usage:

    >>> from rkn import check_rkn
    >>> result = check_rkn.query("domain.name", "YOUR_API_KEY_HERE")
    >>> print (result)
