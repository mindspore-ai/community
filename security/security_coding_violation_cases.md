# 典型违反安全编码案例

## 案例1：未对安全函数返回值进行校验

> 修改前：

进行内存拷贝过程中，未对拷贝函数返回值进行校验，导致拷贝失败时无法捕获失败信息。

```c
(void) memcpy_s(output_addr, output->size, input_addr, input->size);
```

> 修改后

```c
if (memcpy_s(output_addr, output->size, input_addr, input->size) != EOK) {
    ...
}
```

## 案例2：未对指针是否为空进行校验

> 修改前：

`primitive`由外部传入，使用指针`primitive`前，未对指针是否为空进行校验，若指针为空，则调用`name()`成员函数时会产生空指针引用导致程序挂死。

```c++
AbstractBasePtr InferImplPad(const AnalysisEnginePtr &, const PrimitivePtr &primitive,
                             const AbstractBasePtrList &args_spec_list) {
  const std::string op_name = primitive->name();  // 未对meta_graph_指针进行校验
  ...
}
```

> 修改后：

```C++
AbstractBasePtr InferImplPad(const AnalysisEnginePtr &, const PrimitivePtr &primitive,
                             const AbstractBasePtrList &args_spec_list) {
  MS_EXCEPTION_IF_NULL(primitive);
  const std::string op_name = primitive->name();  // 校验指针是否为空后再使用该指针
  ...
}
```
