# Generated by h2py from c:\microsoft sdk\include\sspi.h
ISSP_LEVEL = 32
ISSP_MODE = 1
ISSP_LEVEL = 32
ISSP_MODE = 0
ISSP_LEVEL = 32
ISSP_MODE = 1


def SEC_SUCCESS(Status): return ((Status) >= 0)

SECPKG_FLAG_INTEGRITY = 1
SECPKG_FLAG_PRIVACY = 2
SECPKG_FLAG_TOKEN_ONLY = 4
SECPKG_FLAG_DATAGRAM = 8
SECPKG_FLAG_CONNECTION = 16
SECPKG_FLAG_MULTI_REQUIRED = 32
SECPKG_FLAG_CLIENT_ONLY = 64
SECPKG_FLAG_EXTENDED_ERROR = 128
SECPKG_FLAG_IMPERSONATION = 256
SECPKG_FLAG_ACCEPT_WIN32_NAME = 512
SECPKG_FLAG_STREAM = 1024
SECPKG_FLAG_NEGOTIABLE = 2048
SECPKG_FLAG_GSS_COMPATIBLE = 4096
SECPKG_FLAG_LOGON = 8192
SECPKG_FLAG_ASCII_BUFFERS = 16384
SECPKG_FLAG_FRAGMENT = 32768
SECPKG_FLAG_MUTUAL_AUTH = 65536
SECPKG_FLAG_DELEGATION = 131072
SECPKG_FLAG_READONLY_WITH_CHECKSUM = 262144
SECPKG_ID_NONE = 65535

SECBUFFER_VERSION = 0
SECBUFFER_EMPTY = 0
SECBUFFER_DATA = 1
SECBUFFER_TOKEN = 2
SECBUFFER_PKG_PARAMS = 3
SECBUFFER_MISSING = 4
SECBUFFER_EXTRA = 5
SECBUFFER_STREAM_TRAILER = 6
SECBUFFER_STREAM_HEADER = 7
SECBUFFER_NEGOTIATION_INFO = 8
SECBUFFER_PADDING = 9
SECBUFFER_STREAM = 10
SECBUFFER_MECHLIST = 11
SECBUFFER_MECHLIST_SIGNATURE = 12
SECBUFFER_TARGET = 13
SECBUFFER_CHANNEL_BINDINGS = 14
SECBUFFER_ATTRMASK = (-268435456)
SECBUFFER_READONLY = (-2147483648)
SECBUFFER_READONLY_WITH_CHECKSUM = 268435456
SECBUFFER_RESERVED = 1610612736

SECURITY_NATIVE_DREP = 16
SECURITY_NETWORK_DREP = 0

SECPKG_CRED_INBOUND = 1
SECPKG_CRED_OUTBOUND = 2
SECPKG_CRED_BOTH = 3
SECPKG_CRED_DEFAULT = 4
SECPKG_CRED_RESERVED = -268435456

ISC_REQ_DELEGATE = 1
ISC_REQ_MUTUAL_AUTH = 2
ISC_REQ_REPLAY_DETECT = 4
ISC_REQ_SEQUENCE_DETECT = 8
ISC_REQ_CONFIDENTIALITY = 16
ISC_REQ_USE_SESSION_KEY = 32
ISC_REQ_PROMPT_FOR_CREDS = 64
ISC_REQ_USE_SUPPLIED_CREDS = 128
ISC_REQ_ALLOCATE_MEMORY = 256
ISC_REQ_USE_DCE_STYLE = 512
ISC_REQ_DATAGRAM = 1024
ISC_REQ_CONNECTION = 2048
ISC_REQ_CALL_LEVEL = 4096
ISC_REQ_FRAGMENT_SUPPLIED = 8192
ISC_REQ_EXTENDED_ERROR = 16384
ISC_REQ_STREAM = 32768
ISC_REQ_INTEGRITY = 65536
ISC_REQ_IDENTIFY = 131072
ISC_REQ_NULL_SESSION = 262144
ISC_REQ_MANUAL_CRED_VALIDATION = 524288
ISC_REQ_RESERVED1 = 1048576
ISC_REQ_FRAGMENT_TO_FIT = 2097152
ISC_REQ_HTTP = 0x10000000
ISC_RET_DELEGATE = 1
ISC_RET_MUTUAL_AUTH = 2
ISC_RET_REPLAY_DETECT = 4
ISC_RET_SEQUENCE_DETECT = 8
ISC_RET_CONFIDENTIALITY = 16
ISC_RET_USE_SESSION_KEY = 32
ISC_RET_USED_COLLECTED_CREDS = 64
ISC_RET_USED_SUPPLIED_CREDS = 128
ISC_RET_ALLOCATED_MEMORY = 256
ISC_RET_USED_DCE_STYLE = 512
ISC_RET_DATAGRAM = 1024
ISC_RET_CONNECTION = 2048
ISC_RET_INTERMEDIATE_RETURN = 4096
ISC_RET_CALL_LEVEL = 8192
ISC_RET_EXTENDED_ERROR = 16384
ISC_RET_STREAM = 32768
ISC_RET_INTEGRITY = 65536
ISC_RET_IDENTIFY = 131072
ISC_RET_NULL_SESSION = 262144
ISC_RET_MANUAL_CRED_VALIDATION = 524288
ISC_RET_RESERVED1 = 1048576
ISC_RET_FRAGMENT_ONLY = 2097152

ASC_REQ_DELEGATE = 1
ASC_REQ_MUTUAL_AUTH = 2
ASC_REQ_REPLAY_DETECT = 4
ASC_REQ_SEQUENCE_DETECT = 8
ASC_REQ_CONFIDENTIALITY = 16
ASC_REQ_USE_SESSION_KEY = 32
ASC_REQ_ALLOCATE_MEMORY = 256
ASC_REQ_USE_DCE_STYLE = 512
ASC_REQ_DATAGRAM = 1024
ASC_REQ_CONNECTION = 2048
ASC_REQ_CALL_LEVEL = 4096
ASC_REQ_EXTENDED_ERROR = 32768
ASC_REQ_STREAM = 65536
ASC_REQ_INTEGRITY = 131072
ASC_REQ_LICENSING = 262144
ASC_REQ_IDENTIFY = 524288
ASC_REQ_ALLOW_NULL_SESSION = 1048576
ASC_REQ_ALLOW_NON_USER_LOGONS = 2097152
ASC_REQ_ALLOW_CONTEXT_REPLAY = 4194304
ASC_REQ_FRAGMENT_TO_FIT = 8388608
ASC_REQ_FRAGMENT_SUPPLIED = 8192
ASC_REQ_NO_TOKEN = 16777216
ASC_RET_DELEGATE = 1
ASC_RET_MUTUAL_AUTH = 2
ASC_RET_REPLAY_DETECT = 4
ASC_RET_SEQUENCE_DETECT = 8
ASC_RET_CONFIDENTIALITY = 16
ASC_RET_USE_SESSION_KEY = 32
ASC_RET_ALLOCATED_MEMORY = 256
ASC_RET_USED_DCE_STYLE = 512
ASC_RET_DATAGRAM = 1024
ASC_RET_CONNECTION = 2048
ASC_RET_CALL_LEVEL = 8192
ASC_RET_THIRD_LEG_FAILED = 16384
ASC_RET_EXTENDED_ERROR = 32768
ASC_RET_STREAM = 65536
ASC_RET_INTEGRITY = 131072
ASC_RET_LICENSING = 262144
ASC_RET_IDENTIFY = 524288
ASC_RET_NULL_SESSION = 1048576
ASC_RET_ALLOW_NON_USER_LOGONS = 2097152
ASC_RET_ALLOW_CONTEXT_REPLAY = 4194304
ASC_RET_FRAGMENT_ONLY = 8388608

SECPKG_CRED_ATTR_NAMES = 1
SECPKG_ATTR_SIZES = 0
SECPKG_ATTR_NAMES = 1
SECPKG_ATTR_LIFESPAN = 2
SECPKG_ATTR_DCE_INFO = 3
SECPKG_ATTR_STREAM_SIZES = 4
SECPKG_ATTR_KEY_INFO = 5
SECPKG_ATTR_AUTHORITY = 6
SECPKG_ATTR_PROTO_INFO = 7
SECPKG_ATTR_PASSWORD_EXPIRY = 8
SECPKG_ATTR_SESSION_KEY = 9
SECPKG_ATTR_PACKAGE_INFO = 10
SECPKG_ATTR_USER_FLAGS = 11
SECPKG_ATTR_NEGOTIATION_INFO = 12
SECPKG_ATTR_NATIVE_NAMES = 13
SECPKG_ATTR_FLAGS = 14
SECPKG_ATTR_USE_VALIDATED = 15
SECPKG_ATTR_CREDENTIAL_NAME = 16
SECPKG_ATTR_TARGET_INFORMATION = 17
SECPKG_ATTR_ACCESS_TOKEN = 18
SECPKG_ATTR_TARGET = 19
SECPKG_ATTR_AUTHENTICATION_ID = 20

# attributes from schannel.h
SECPKG_ATTR_REMOTE_CERT_CONTEXT = 83
SECPKG_ATTR_LOCAL_CERT_CONTEXT = 84
SECPKG_ATTR_ROOT_STORE = 85
SECPKG_ATTR_SUPPORTED_ALGS = 86
SECPKG_ATTR_CIPHER_STRENGTHS = 87
SECPKG_ATTR_SUPPORTED_PROTOCOLS = 88
SECPKG_ATTR_ISSUER_LIST_EX = 89
SECPKG_ATTR_CONNECTION_INFO = 90
SECPKG_ATTR_EAP_KEY_BLOCK = 91
SECPKG_ATTR_MAPPED_CRED_ATTR = 92
SECPKG_ATTR_SESSION_INFO = 93
SECPKG_ATTR_APP_DATA = 94

SECPKG_NEGOTIATION_COMPLETE = 0
SECPKG_NEGOTIATION_OPTIMISTIC = 1
SECPKG_NEGOTIATION_IN_PROGRESS = 2
SECPKG_NEGOTIATION_DIRECT = 3
SECPKG_NEGOTIATION_TRY_MULTICRED = 4
SECPKG_CONTEXT_EXPORT_RESET_NEW = 1
SECPKG_CONTEXT_EXPORT_DELETE_OLD = 2
SECQOP_WRAP_NO_ENCRYPT = (-2147483647)
SECURITY_ENTRYPOINT_ANSIW = "InitSecurityInterfaceW"
SECURITY_ENTRYPOINT_ANSIA = "InitSecurityInterfaceA"
SECURITY_ENTRYPOINT16 = "INITSECURITYINTERFACEA"
SECURITY_ENTRYPOINT_ANSI = SECURITY_ENTRYPOINT_ANSIW
SECURITY_ENTRYPOINT_ANSI = SECURITY_ENTRYPOINT_ANSIA
SECURITY_ENTRYPOINT = SECURITY_ENTRYPOINT16
SECURITY_ENTRYPOINT_ANSI = SECURITY_ENTRYPOINT16
SECURITY_SUPPORT_PROVIDER_INTERFACE_VERSION = 1
SECURITY_SUPPORT_PROVIDER_INTERFACE_VERSION_2 = 2
SASL_OPTION_SEND_SIZE = 1
SASL_OPTION_RECV_SIZE = 2
SASL_OPTION_AUTHZ_STRING = 3
SASL_OPTION_AUTHZ_PROCESSING = 4
SEC_WINNT_AUTH_IDENTITY_ANSI = 1
SEC_WINNT_AUTH_IDENTITY_UNICODE = 2
SEC_WINNT_AUTH_IDENTITY_VERSION = 512
SEC_WINNT_AUTH_IDENTITY_MARSHALLED = 4
SEC_WINNT_AUTH_IDENTITY_ONLY = 8
SECPKG_OPTIONS_TYPE_UNKNOWN = 0
SECPKG_OPTIONS_TYPE_LSA = 1
SECPKG_OPTIONS_TYPE_SSPI = 2
SECPKG_OPTIONS_PERMANENT = 1

SEC_E_INSUFFICIENT_MEMORY = -2146893056
SEC_E_INVALID_HANDLE = -2146893055
SEC_E_UNSUPPORTED_FUNCTION = -2146893054
SEC_E_TARGET_UNKNOWN = -2146893053
SEC_E_INTERNAL_ERROR = -2146893052
SEC_E_SECPKG_NOT_FOUND = -2146893051
SEC_E_NOT_OWNER = -2146893050
SEC_E_CANNOT_INSTALL = -2146893049
SEC_E_INVALID_TOKEN = -2146893048
SEC_E_CANNOT_PACK = -2146893047
SEC_E_QOP_NOT_SUPPORTED = -2146893046
SEC_E_NO_IMPERSONATION = -2146893045
SEC_E_LOGON_DENIED = -2146893044
SEC_E_UNKNOWN_CREDENTIALS = -2146893043
SEC_E_NO_CREDENTIALS = -2146893042
SEC_E_MESSAGE_ALTERED = -2146893041
SEC_E_OUT_OF_SEQUENCE = -2146893040
SEC_E_NO_AUTHENTICATING_AUTHORITY = -2146893039
SEC_I_CONTINUE_NEEDED = 590610
SEC_I_COMPLETE_NEEDED = 590611
SEC_I_COMPLETE_AND_CONTINUE = 590612
SEC_I_LOCAL_LOGON = 590613
SEC_E_BAD_PKGID = -2146893034
SEC_E_CONTEXT_EXPIRED = -2146893033
SEC_I_CONTEXT_EXPIRED = 590615
SEC_E_INCOMPLETE_MESSAGE = -2146893032
SEC_E_INCOMPLETE_CREDENTIALS = -2146893024
SEC_E_BUFFER_TOO_SMALL = -2146893023
SEC_I_INCOMPLETE_CREDENTIALS = 590624
SEC_I_RENEGOTIATE = 590625
SEC_E_WRONG_PRINCIPAL = -2146893022
SEC_I_NO_LSA_CONTEXT = 590627
SEC_E_TIME_SKEW = -2146893020
SEC_E_UNTRUSTED_ROOT = -2146893019
SEC_E_ILLEGAL_MESSAGE = -2146893018
SEC_E_CERT_UNKNOWN = -2146893017
SEC_E_CERT_EXPIRED = -2146893016
SEC_E_ENCRYPT_FAILURE = -2146893015
SEC_E_DECRYPT_FAILURE = -2146893008
SEC_E_ALGORITHM_MISMATCH = -2146893007
SEC_E_SECURITY_QOS_FAILED = -2146893006
SEC_E_UNFINISHED_CONTEXT_DELETED = -2146893005
SEC_E_NO_TGT_REPLY = -2146893004
SEC_E_NO_IP_ADDRESSES = -2146893003
SEC_E_WRONG_CREDENTIAL_HANDLE = -2146893002
SEC_E_CRYPTO_SYSTEM_INVALID = -2146893001
SEC_E_MAX_REFERRALS_EXCEEDED = -2146893000
SEC_E_MUST_BE_KDC = -2146892999
SEC_E_STRONG_CRYPTO_NOT_SUPPORTED = -2146892998
SEC_E_TOO_MANY_PRINCIPALS = -2146892997
SEC_E_NO_PA_DATA = -2146892996
SEC_E_PKINIT_NAME_MISMATCH = -2146892995
SEC_E_SMARTCARD_LOGON_REQUIRED = -2146892994
SEC_E_SHUTDOWN_IN_PROGRESS = -2146892993
SEC_E_KDC_INVALID_REQUEST = -2146892992
SEC_E_KDC_UNABLE_TO_REFER = -2146892991
SEC_E_KDC_UNKNOWN_ETYPE = -2146892990
SEC_E_UNSUPPORTED_PREAUTH = -2146892989
SEC_E_DELEGATION_REQUIRED = -2146892987
SEC_E_BAD_BINDINGS = -2146892986
SEC_E_MULTIPLE_ACCOUNTS = -2146892985
SEC_E_NO_KERB_KEY = -2146892984

ERROR_IPSEC_QM_POLICY_EXISTS = 13000
ERROR_IPSEC_QM_POLICY_NOT_FOUND = 13001
ERROR_IPSEC_QM_POLICY_IN_USE = 13002
ERROR_IPSEC_MM_POLICY_EXISTS = 13003
ERROR_IPSEC_MM_POLICY_NOT_FOUND = 13004
ERROR_IPSEC_MM_POLICY_IN_USE = 13005
ERROR_IPSEC_MM_FILTER_EXISTS = 13006
ERROR_IPSEC_MM_FILTER_NOT_FOUND = 13007
ERROR_IPSEC_TRANSPORT_FILTER_EXISTS = 13008
ERROR_IPSEC_TRANSPORT_FILTER_NOT_FOUND = 13009
ERROR_IPSEC_MM_AUTH_EXISTS = 13010
ERROR_IPSEC_MM_AUTH_NOT_FOUND = 13011
ERROR_IPSEC_MM_AUTH_IN_USE = 13012
ERROR_IPSEC_DEFAULT_MM_POLICY_NOT_FOUND = 13013
ERROR_IPSEC_DEFAULT_MM_AUTH_NOT_FOUND = 13014
ERROR_IPSEC_DEFAULT_QM_POLICY_NOT_FOUND = 13015
ERROR_IPSEC_TUNNEL_FILTER_EXISTS = 13016
ERROR_IPSEC_TUNNEL_FILTER_NOT_FOUND = 13017
ERROR_IPSEC_MM_FILTER_PENDING_DELETION = 13018
ERROR_IPSEC_TRANSPORT_FILTER_PENDING_DELETION = 13019
ERROR_IPSEC_TUNNEL_FILTER_PENDING_DELETION = 13020
ERROR_IPSEC_MM_POLICY_PENDING_DELETION = 13021
ERROR_IPSEC_MM_AUTH_PENDING_DELETION = 13022
ERROR_IPSEC_QM_POLICY_PENDING_DELETION = 13023
WARNING_IPSEC_MM_POLICY_PRUNED = 13024
WARNING_IPSEC_QM_POLICY_PRUNED = 13025
ERROR_IPSEC_IKE_NEG_STATUS_BEGIN = 13800
ERROR_IPSEC_IKE_AUTH_FAIL = 13801
ERROR_IPSEC_IKE_ATTRIB_FAIL = 13802
ERROR_IPSEC_IKE_NEGOTIATION_PENDING = 13803
ERROR_IPSEC_IKE_GENERAL_PROCESSING_ERROR = 13804
ERROR_IPSEC_IKE_TIMED_OUT = 13805
ERROR_IPSEC_IKE_NO_CERT = 13806
ERROR_IPSEC_IKE_SA_DELETED = 13807
ERROR_IPSEC_IKE_SA_REAPED = 13808
ERROR_IPSEC_IKE_MM_ACQUIRE_DROP = 13809
ERROR_IPSEC_IKE_QM_ACQUIRE_DROP = 13810
ERROR_IPSEC_IKE_QUEUE_DROP_MM = 13811
ERROR_IPSEC_IKE_QUEUE_DROP_NO_MM = 13812
ERROR_IPSEC_IKE_DROP_NO_RESPONSE = 13813
ERROR_IPSEC_IKE_MM_DELAY_DROP = 13814
ERROR_IPSEC_IKE_QM_DELAY_DROP = 13815
ERROR_IPSEC_IKE_ERROR = 13816
ERROR_IPSEC_IKE_CRL_FAILED = 13817
ERROR_IPSEC_IKE_INVALID_KEY_USAGE = 13818
ERROR_IPSEC_IKE_INVALID_CERT_TYPE = 13819
ERROR_IPSEC_IKE_NO_PRIVATE_KEY = 13820
ERROR_IPSEC_IKE_DH_FAIL = 13822
ERROR_IPSEC_IKE_INVALID_HEADER = 13824
ERROR_IPSEC_IKE_NO_POLICY = 13825
ERROR_IPSEC_IKE_INVALID_SIGNATURE = 13826
ERROR_IPSEC_IKE_KERBEROS_ERROR = 13827
ERROR_IPSEC_IKE_NO_PUBLIC_KEY = 13828
ERROR_IPSEC_IKE_PROCESS_ERR = 13829
ERROR_IPSEC_IKE_PROCESS_ERR_SA = 13830
ERROR_IPSEC_IKE_PROCESS_ERR_PROP = 13831
ERROR_IPSEC_IKE_PROCESS_ERR_TRANS = 13832
ERROR_IPSEC_IKE_PROCESS_ERR_KE = 13833
ERROR_IPSEC_IKE_PROCESS_ERR_ID = 13834
ERROR_IPSEC_IKE_PROCESS_ERR_CERT = 13835
ERROR_IPSEC_IKE_PROCESS_ERR_CERT_REQ = 13836
ERROR_IPSEC_IKE_PROCESS_ERR_HASH = 13837
ERROR_IPSEC_IKE_PROCESS_ERR_SIG = 13838
ERROR_IPSEC_IKE_PROCESS_ERR_NONCE = 13839
ERROR_IPSEC_IKE_PROCESS_ERR_NOTIFY = 13840
ERROR_IPSEC_IKE_PROCESS_ERR_DELETE = 13841
ERROR_IPSEC_IKE_PROCESS_ERR_VENDOR = 13842
ERROR_IPSEC_IKE_INVALID_PAYLOAD = 13843
ERROR_IPSEC_IKE_LOAD_SOFT_SA = 13844
ERROR_IPSEC_IKE_SOFT_SA_TORN_DOWN = 13845
ERROR_IPSEC_IKE_INVALID_COOKIE = 13846
ERROR_IPSEC_IKE_NO_PEER_CERT = 13847
ERROR_IPSEC_IKE_PEER_CRL_FAILED = 13848
ERROR_IPSEC_IKE_POLICY_CHANGE = 13849
ERROR_IPSEC_IKE_NO_MM_POLICY = 13850
ERROR_IPSEC_IKE_NOTCBPRIV = 13851
ERROR_IPSEC_IKE_SECLOADFAIL = 13852
ERROR_IPSEC_IKE_FAILSSPINIT = 13853
ERROR_IPSEC_IKE_FAILQUERYSSP = 13854
ERROR_IPSEC_IKE_SRVACQFAIL = 13855
ERROR_IPSEC_IKE_SRVQUERYCRED = 13856
ERROR_IPSEC_IKE_GETSPIFAIL = 13857
ERROR_IPSEC_IKE_INVALID_FILTER = 13858
ERROR_IPSEC_IKE_OUT_OF_MEMORY = 13859
ERROR_IPSEC_IKE_ADD_UPDATE_KEY_FAILED = 13860
ERROR_IPSEC_IKE_INVALID_POLICY = 13861
ERROR_IPSEC_IKE_UNKNOWN_DOI = 13862
ERROR_IPSEC_IKE_INVALID_SITUATION = 13863
ERROR_IPSEC_IKE_DH_FAILURE = 13864
ERROR_IPSEC_IKE_INVALID_GROUP = 13865
ERROR_IPSEC_IKE_ENCRYPT = 13866
ERROR_IPSEC_IKE_DECRYPT = 13867
ERROR_IPSEC_IKE_POLICY_MATCH = 13868
ERROR_IPSEC_IKE_UNSUPPORTED_ID = 13869
ERROR_IPSEC_IKE_INVALID_HASH = 13870
ERROR_IPSEC_IKE_INVALID_HASH_ALG = 13871
ERROR_IPSEC_IKE_INVALID_HASH_SIZE = 13872
ERROR_IPSEC_IKE_INVALID_ENCRYPT_ALG = 13873
ERROR_IPSEC_IKE_INVALID_AUTH_ALG = 13874
ERROR_IPSEC_IKE_INVALID_SIG = 13875
ERROR_IPSEC_IKE_LOAD_FAILED = 13876
ERROR_IPSEC_IKE_RPC_DELETE = 13877
ERROR_IPSEC_IKE_BENIGN_REINIT = 13878
ERROR_IPSEC_IKE_INVALID_RESPONDER_LIFETIME_NOTIFY = 13879
ERROR_IPSEC_IKE_INVALID_CERT_KEYLEN = 13881
ERROR_IPSEC_IKE_MM_LIMIT = 13882
ERROR_IPSEC_IKE_NEGOTIATION_DISABLED = 13883
ERROR_IPSEC_IKE_NEG_STATUS_END = 13884
CRYPT_E_MSG_ERROR = ((-2146889727))
CRYPT_E_UNKNOWN_ALGO = ((-2146889726))
CRYPT_E_OID_FORMAT = ((-2146889725))
CRYPT_E_INVALID_MSG_TYPE = ((-2146889724))
CRYPT_E_UNEXPECTED_ENCODING = ((-2146889723))
CRYPT_E_AUTH_ATTR_MISSING = ((-2146889722))
CRYPT_E_HASH_VALUE = ((-2146889721))
CRYPT_E_INVALID_INDEX = ((-2146889720))
CRYPT_E_ALREADY_DECRYPTED = ((-2146889719))
CRYPT_E_NOT_DECRYPTED = ((-2146889718))
CRYPT_E_RECIPIENT_NOT_FOUND = ((-2146889717))
CRYPT_E_CONTROL_TYPE = ((-2146889716))
CRYPT_E_ISSUER_SERIALNUMBER = ((-2146889715))
CRYPT_E_SIGNER_NOT_FOUND = ((-2146889714))
CRYPT_E_ATTRIBUTES_MISSING = ((-2146889713))
CRYPT_E_STREAM_MSG_NOT_READY = ((-2146889712))
CRYPT_E_STREAM_INSUFFICIENT_DATA = ((-2146889711))
CRYPT_I_NEW_PROTECTION_REQUIRED = (593938)
CRYPT_E_BAD_LEN = ((-2146885631))
CRYPT_E_BAD_ENCODE = ((-2146885630))
CRYPT_E_FILE_ERROR = ((-2146885629))
CRYPT_E_NOT_FOUND = ((-2146885628))
CRYPT_E_EXISTS = ((-2146885627))
CRYPT_E_NO_PROVIDER = ((-2146885626))
CRYPT_E_SELF_SIGNED = ((-2146885625))
CRYPT_E_DELETED_PREV = ((-2146885624))
CRYPT_E_NO_MATCH = ((-2146885623))
CRYPT_E_UNEXPECTED_MSG_TYPE = ((-2146885622))
CRYPT_E_NO_KEY_PROPERTY = ((-2146885621))
CRYPT_E_NO_DECRYPT_CERT = ((-2146885620))
CRYPT_E_BAD_MSG = ((-2146885619))
CRYPT_E_NO_SIGNER = ((-2146885618))
CRYPT_E_PENDING_CLOSE = ((-2146885617))
CRYPT_E_REVOKED = ((-2146885616))
CRYPT_E_NO_REVOCATION_DLL = ((-2146885615))
CRYPT_E_NO_REVOCATION_CHECK = ((-2146885614))
CRYPT_E_REVOCATION_OFFLINE = ((-2146885613))
CRYPT_E_NOT_IN_REVOCATION_DATABASE = ((-2146885612))
CRYPT_E_INVALID_NUMERIC_STRING = ((-2146885600))
CRYPT_E_INVALID_PRINTABLE_STRING = ((-2146885599))
CRYPT_E_INVALID_IA5_STRING = ((-2146885598))
CRYPT_E_INVALID_X500_STRING = ((-2146885597))
CRYPT_E_NOT_CHAR_STRING = ((-2146885596))
CRYPT_E_FILERESIZED = ((-2146885595))
CRYPT_E_SECURITY_SETTINGS = ((-2146885594))
CRYPT_E_NO_VERIFY_USAGE_DLL = ((-2146885593))
CRYPT_E_NO_VERIFY_USAGE_CHECK = ((-2146885592))
CRYPT_E_VERIFY_USAGE_OFFLINE = ((-2146885591))
CRYPT_E_NOT_IN_CTL = ((-2146885590))
CRYPT_E_NO_TRUSTED_SIGNER = ((-2146885589))
CRYPT_E_MISSING_PUBKEY_PARA = ((-2146885588))
CRYPT_E_OSS_ERROR = ((-2146881536))

# Kerberos message types for LsaCallAuthenticationPackage (from ntsecapi.h)
KerbDebugRequestMessage = 0
KerbQueryTicketCacheMessage = 1
KerbChangeMachinePasswordMessage = 2
KerbVerifyPacMessage = 3
KerbRetrieveTicketMessage = 4
KerbUpdateAddressesMessage = 5
KerbPurgeTicketCacheMessage = 6
KerbChangePasswordMessage = 7
KerbRetrieveEncodedTicketMessage = 8
KerbDecryptDataMessage = 9
KerbAddBindingCacheEntryMessage = 10
KerbSetPasswordMessage = 11
KerbSetPasswordExMessage = 12
KerbVerifyCredentialsMessage = 13
KerbQueryTicketCacheExMessage = 14
KerbPurgeTicketCacheExMessage = 15
KerbRefreshSmartcardCredentialsMessage = 16
KerbAddExtraCredentialsMessage = 17
KerbQuerySupplementalCredentialsMessage = 18

# messages used with msv1_0 from ntsecapi.h
MsV1_0Lm20ChallengeRequest = 0
MsV1_0Lm20GetChallengeResponse = 1
MsV1_0EnumerateUsers = 2
MsV1_0GetUserInfo = 3
MsV1_0ReLogonUsers = 4
MsV1_0ChangePassword = 5
MsV1_0ChangeCachedPassword = 6
MsV1_0GenericPassthrough = 7
MsV1_0CacheLogon = 8
MsV1_0SubAuth = 9
MsV1_0DeriveCredential = 10
MsV1_0CacheLookup = 11
MsV1_0SetProcessOption = 12

SEC_E_OK = 0
