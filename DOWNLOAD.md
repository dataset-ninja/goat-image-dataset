Dataset **Goat Image** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://assets.supervisely.com/supervisely-supervisely-assets-public/teams_storage/6/A/q1/3S324wg5DCSj6k6dBFYgnZULLGUii0RlW99OMnv02SKp7G3eBIE5TtbPhqrJFGUJINvpPcVxbvHhzrC0lESiQU6wTEiRgloiA2iHQWIrmKeMpOcBxhh20xS4YRLN.tar)

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