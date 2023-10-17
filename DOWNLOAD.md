Dataset **Goat Image** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://assets.supervisely.com/supervisely-supervisely-assets-public/teams_storage/p/P/nW/WPW94w89kuJtLNqVP3NikWZeYKJSGkwfkcq6b0vxuHhAuHoCbl05IuvMtQtnstpS4pxQv6tu555Ts2bwKB7dqYbrQuWaAcBRhYL9WpvDL3jjEeDpaMqTU8SJTWOU.tar)

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