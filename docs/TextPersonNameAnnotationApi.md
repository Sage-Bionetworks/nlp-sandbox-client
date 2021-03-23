# annotator.TextPersonNameAnnotationApi

All URIs are relative to *http://example.com/api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_text_person_name_annotations**](TextPersonNameAnnotationApi.md#create_text_person_name_annotations) | **POST** /textPersonNameAnnotations | Annotate person names in a clinical note


# **create_text_person_name_annotations**
> TextPersonNameAnnotationResponse create_text_person_name_annotations()

Annotate person names in a clinical note

Return the person name annotations found in a clinical note

### Example

```python
import time
import annotator
from annotator.api import text_person_name_annotation_api
from annotator.model.error import Error
from annotator.model.text_person_name_annotation_request import TextPersonNameAnnotationRequest
from annotator.model.text_person_name_annotation_response import TextPersonNameAnnotationResponse
from pprint import pprint
# Defining the host is optional and defaults to http://example.com/api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = annotator.Configuration(
    host = "http://example.com/api/v1"
)


# Enter a context with an instance of the API client
with annotator.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = text_person_name_annotation_api.TextPersonNameAnnotationApi(api_client)
    text_person_name_annotation_request = TextPersonNameAnnotationRequest(
        note=Note(
            identifier=NoteId("awesome-note"),
            text="text_example",
            type="type_example",
            patient_id=PatientId("awesome-patient"),
        ),
    ) # TextPersonNameAnnotationRequest |  (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Annotate person names in a clinical note
        api_response = api_instance.create_text_person_name_annotations(text_person_name_annotation_request=text_person_name_annotation_request)
        pprint(api_response)
    except annotator.ApiException as e:
        print("Exception when calling TextPersonNameAnnotationApi->create_text_person_name_annotations: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **text_person_name_annotation_request** | [**TextPersonNameAnnotationRequest**](TextPersonNameAnnotationRequest.md)|  | [optional]

### Return type

[**TextPersonNameAnnotationResponse**](TextPersonNameAnnotationResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |
**400** | Invalid request |  -  |
**500** | The request cannot be fulfilled due to an unexpected server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

