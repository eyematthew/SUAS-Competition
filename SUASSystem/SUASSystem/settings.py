class GCSSettings(object):

    UAV_CONNECTION_STRING = "tcp:127.0.0.1:5760"#14551"

    INTEROP_URL = "http://10.10.130.10:80"
    INTEROP_USERNAME = "flint"
    INTEROP_PASSWORD = "8182105855"

    MSL_ALT = 446.42
    SDA_MIN_ALT = 110

    GENERATED_DATA_LOCATION = "image_data"
    '''
    BASE_LETTER_CATEGORIZER_PCA_PATH
    Vale's path: /Users/vtolpegin/Desktop/GENERATED FORCED WINDOW PCA
    '''
    VALE_BASE_LETTER_CATEGORIZER_PATH = "/Users/vtolpegin/Desktop/GENERATED FORCED WINDOW PCA"
    BASE_LETTER_CATEGORIZER_PCA_PATH = VALE_BASE_LETTER_CATEGORIZER_PATH
    '''
    BASE_ORIENTATION_CLASSIFIER_PCA_PATH:
    Vale's path: /Users/vtolpegin/Desktop/GENERATED 180 ORIENTATION PCA
    '''
    VALE_BASE_ORIENTATION_CLASSIFIER_PCA_PATH = "/Users/vtolpegin/Desktop/GENERATED 180 ORIENTATION PCA"
    BASE_ORIENTATION_CLASSIFIER_PCA_PATH = VALE_BASE_ORIENTATION_CLASSIFIER_PCA_PATH

    SD_CARD_NAME = "NX500"

    MIN_DIST_BETWEEN_TARGETS_KM = 30.0/1000.0
