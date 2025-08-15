Dataset **Goat Image** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://assets.supervisely.com/remote/eyJsaW5rIjogInMzOi8vc3VwZXJ2aXNlbHktZGF0YXNldHMvMjE5N19Hb2F0IEltYWdlL2dvYXQtaW1hZ2UtRGF0YXNldE5pbmphLnRhciIsICJzaWciOiAiL2xnOGhqY0xFelhBVVFvb3hXTnQ0S0c4NDZjM3gyc3pZVm5YT2tDOG1jOD0ifQ==?response-content-disposition=attachment%3B%20filename%3D%22goat-image-DatasetNinja.tar%22)

As an alternative, it can be downloaded with *dataset-tools* package:
``` bash
pip install --upgrade dataset-tools
```

... using following python code:
``` python
import dataset_tools as dtools

dtools.download(dataset='Goat Image', dst_dir='~/dataset-ninja/')
```
Make sure not to overlook the [python code example](https://developer.supervisely.com/getting-started/python-sdk-tutorials/iterate-over-a-local-project) available on the Supervisely Developer Portal. It will give you a clear idea of how to effortlessly work with the downloaded dataset.

The data in original format can be [downloaded here](https://prod-dcd-datasets-cache-zipfiles.s3.eu-west-1.amazonaws.com/4skwhnrscr-2.zip).