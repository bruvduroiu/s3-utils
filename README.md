# S3 File I/O utils
_(specialised for matplotlib/numpy files)_

These utility methods were created to help with saving files and matplotlib figures when running Deep Learning models in a Dockerized environment on AWS.

## 1. Installation

Clone this repository locally, then:

```bash
$ pip install -e s3_utils/
```

### Setting AWS environment variables when running Docker container

```bash
$ docker run --rm -e AWS_ACCESS_KEY_ID=$(aws --profile default configure get aws_access_key_id) -e AWS_SECRET_ACCESS_KEY=$(aws --profile default configure get aws_secret_access_key) <docker-image>
```

## 2. Examples

### Saving a matplotlib figure
```python
import matplotlib.pyplot as plt

from s3.file_utils import *

fig = plt.figure()
ax = fig.add_subplots(111)
ax.scatter(arr[:,0], arr[:,1])

save_fig(fig, s3_file_key='path/to/s3/file.png', s3_bucket='mock-bucket')
```

### Saving a generic file
```python
import numpy as np

from s3.file_utils import *

arr = np.random.normal(3, 1.25, 100)
np.save('my_array', arr)

save_file('my_array.npy', s3_file_key='path/to/s3/my_array.npy', s3_bucket='mock-bucket')
```
