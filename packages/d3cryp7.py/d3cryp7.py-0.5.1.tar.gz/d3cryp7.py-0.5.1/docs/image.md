Image
=====

This module defines functions for image processing. The RESTful API uses these
functions to generate a result. See the documentation for each function and the
unit tests for more information.

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

**Functions:**
------------

### recognize(image)

Recognizes text in an image by using Google's Tesseract engine and returns a
dictionary containing the result and any error messages that occurred

**Args:**

| Name  |  Type  |      Description       |
|-------|--------|------------------------|
| image | String | A base64 encoded image |

**Returns:**

|    Type    |                        Description                        |
|------------|-----------------------------------------------------------|
| Dictionary | A dictionary containing the result and any error messages |

This function does not use file IO. Instead, the image is recognized by
first decoding the base64 image and then piping the data directly to
Tesseract. If the result from Tesseract is empty, the result will be None.
If no error occurred, the dictionary will not contain an error.

### tag(image)

Uses various machine learning services to tag the contents of an image and
returns a dictionary containing the result and any error messages that occurred

**Args:**

|    Name    |         Description         |
|------------|-----------------------------|
| image      | A base64 encoded image      |
| app_id     | The app ID for Clarifai     |
| app_secret | The app secret for Clarifai |

**Returns:**

|    Type    |                        Description                        |
|------------|-----------------------------------------------------------|
| Dictionary | A dictionary containing the result and any error messages |
