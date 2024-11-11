from enum import Enum


class Cred(Enum):
    Access = "AKIA5FTZBGWLQ7OMS4GZ"
    Secret = "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"
    country_Region = "israel"
    main_subnet = "10.0.0.0"
    prefix = 16
    max_subnet = main_subnet+ "/"+ str(prefix)
    key_name = "AWS1_key_Acess"
