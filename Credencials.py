from enum import Enum


class Cred(Enum):
    Access = "AKIA5FTZBGWLTK6VOYUC"
    Secret = "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"
    country_Region = "israel"
    main_subnet = "10.0.0.0"
    prefix = 16
    max_subnet = main_subnet+ "/"+ str(prefix)

