# ml_metadata_testing
Purpose: This is middleware code for OpenStack Swift. that allows a Swift users to leverage Google Vision API to update metadata for images within your OpenStack Swift Bucket.  This metadata uses Googles ML/AI to automatically update the image metadata with 

# This setup currently does the following:
1. Uses your Google credentials with your Google Vision API account to access this service
2. This service allows you to generate ML data for these images that are in your OpenStack Swift container
3. Returns that data and generates a command that posts the metadata from Google Vision API to the objects metadata inside your container

Resource links:
1. https://cloud.google.com/vision/docs/reference/rest/
2. https://cloud.google.com/vision/docs/before-you-begin
3. https://cloud.google.com/vision/docs/libraries

*Sample command generated from code:*
1. swift post test_images unnamed.png -m mldata0:Display_advertising  -m mldata1:Brand  -m mldata2:Graphic_design  -m mldata3:Advertising  -m mldata4:Organization  -m mldata5:Design  -m mldata6:Font  -m mldata7:Line  -m mldata8:Graphics  -m mldata9:Product

