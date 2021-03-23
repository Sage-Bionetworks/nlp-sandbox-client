# annotator.TextPhysicalAddressAnnotationApi

All URIs are relative to *http://example.com/api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_text_physical_address_annotations**](TextPhysicalAddressAnnotationApi.md#create_text_physical_address_annotations) | **POST** /textPhysicalAddressAnnotations | Annotate physical addresses in a clinical note


# **create_text_physical_address_annotations**
> TextPhysicalAddressAnnotationResponse create_text_physical_address_annotations()

Annotate physical addresses in a clinical note

Return the physical addresse annotations found in a clinical note

### Example

```python
import time
import annotator
from annotator.api import text_physical_address_annotation_api
from annotator.model.text_physical_address_annotation_response import TextPhysicalAddressAnnotationResponse
from annotator.model.error import Error
from annotator.model.text_physical_address_annotation_request import TextPhysicalAddressAnnotationRequest
from pprint import pprint
# Defining the host is optional and defaults to http://example.com/api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = annotator.Configuration(
    host = "http://example.com/api/v1"
)


# Enter a context with an instance of the API client
with annotator.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = text_physical_address_annotation_api.TextPhysicalAddressAnnotationApi(api_client)
    text_physical_address_annotation_request = TextPhysicalAddressAnnotationRequest(
        note=Note(
            identifier=NoteId("awesome-note"),
            text="text_example",
            type="type_example",
            patient_id=PatientId("awesome-patient"),
        ),
    ) # TextPhysicalAddressAnnotationRequest |  (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Annotate physical addresses in a clinical note
        api_response = api_instance.create_text_physical_address_annotations(text_physical_address_annotation_request=text_physical_address_annotation_request)
        pprint(api_response)
    except annotator.ApiException as e:
        print("Exception when calling TextPhysicalAddressAnnotationApi->create_text_physical_address_annotations: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **text_physical_address_annotation_request** | [**TextPhysicalAddressAnnotationRequest**](TextPhysicalAddressAnnotationRequest.md)|  | [optional]

### Return type

[**TextPhysicalAddressAnnotationResponse**](TextPhysicalAddressAnnotationResponse.md)

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

