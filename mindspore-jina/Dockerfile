FROM mindspore/mindspore-cpu:1.0.0

# setup the workspace
COPY . /workspace
WORKDIR /workspace

# fix: add to path
ENV PATH="/root/.local/bin:${PATH}"

# install the third-party requirements
RUN pip install --user -r requirements.txt

RUN cd lenet && \
    python train.py --data_path data/fashion/ --ckpt_path ckpt --device_target="CPU" && \
    cd -

# for testing the image
RUN pip install --user pytest && pytest -s

ENTRYPOINT ["jina", "pod", "--uses", "config.yml"]