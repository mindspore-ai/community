# MindSpore import方式推荐

文档样例代码推荐采用以下import方式编写。

```python
import mindspore as ms
import mindspore.dataset as ds
import mindspore.dataset.transforms as transforms
import mindspore.dataset.audio as audio
import mindspore.dataset.text as text
import mindspore.dataset.vision as vision
from mindspore.mindrecord import FileWriter
import mindspore.communication as comm
import mindspore.nn as nn
import mindspore.ops as ops
import mindspore.numpy as mnp
import mindspore.scipy as mscipy
import mindspore.boost as boost

import numpy as np
```

代码写作样例如下：

```python
ms.common.initializer.xxx
ms.Tensor
ms.Parameter
ms.train.Model
ms.float32
ms.set_context
```
