# vectorize_client is the module/package that lets us interact with the Vectorize API
import vectorize_client as v
import os
from typing import List, Dict, Any

# class definition for VectorizeWrapper
# creates a wrapper class to encapsulate Vectorize API functionality
class VectorizeWrapper:
    def __init__(self):
        # os.environ.get() is used to get the value of the environment variable
        # if the environment variable is not set, it will return None
        self.access_token = os.environ.get("VECTORIZE_PIPELINE_ACCESS_TOKEN")
        self.organization_id = os.environ.get("VECTORIZE_ORGANIZATION_ID")
        self.pipeline_id = os.environ.get("VECTORIZE_PIPELINE_ID")

        # check if all required variables are present in the environment
        # if not, raise an early exception if configuration is incomplete
        if not all([self.access_token, self.organization_id, self.pipeline_id]):
            raise ValueError("Missing required Vectorize environment variables")
        
        # configure the vectorize api
        api_config = v.Configuration(
            access_token=self.access_token,
            host="https://api.vectorize.io/v1"
        )
        self.api_client = v.ApiClient(api_config) # initializes API client with configuration above
        self.pipelines = v.PieplinesApi(self.api_client) # initializes pipelines API client with API client

    # retrieve_documents is a method that retrieves documents from the Vectorize API
    # it takes a question and a number of results as arguments
    # it returns a list of dictionaries containing the documents
    def retrieve_documents(self, question: str, num_results: int = 5) -> List[Dict[str, Any]]:
        try:
            response = self.pipelines.retrieve_documents(
                self.organization_id,
                self.pipeline_id,
                v.RetrieveDocumentsRequest(
                    question=question,
                    num_results=num_results,
                )
            )

            if hasattr(response, "documents"):
                return response.documents
            else:
                return []
            
        except Exception as e:
            print(f"Error retrieving documents: {e}")
            if hasattr(e, "body"):
                print(f"Error response body: {e.body}")
            return []
    
    def get_required_env_vars(self) -> List[str]:
        return [
            "VECTORIZE_PIPELINE_ACCESS_TOKEN",
            "VECTORIZE_ORGANIZATION_ID",
            "VECTORIZE_PIPELINE_ID"
        ]
        