# Annotation interface

## TODOS

- [] Find an existing annotation component and make it show the image by URL (e.g. [this](https://github.com/waoai/react-image-annotate))
- [] Add instructions (for eventual workers) in a modal (popup), you may need to integrate another existing component
- [] Make sure the annotations input in the component are saved in the state of the app
- [] Create an POST request against the endpoint `http://localhost:3000/annotation`; the body of the request should be a JSON string with the annotation (you can use the `fetch` API or `axios`)
