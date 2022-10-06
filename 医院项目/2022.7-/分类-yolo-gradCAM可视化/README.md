https://tf-explain.readthedocs.io/en/latest/methods.html#grad-cam

https://keras.io/examples/vision/grad_cam/

https://blog.csdn.net/chenvvei/article/details/116087445

https://github.com/jacobgil/keras-grad-cam

https://github.com/withtimesgo1115/gradCAM-YOLOv3-pytorch

https://github.com/utkuozbulak/pytorch-cnn-visualizations

**----------------------

from tf_explain.callbacks.grad_cam import GradCAMCallback

model = [...]

callbacks = [
    GradCAMCallback(
        validation_data=(x_val, y_val),
        layer_name="activation_1",
        class_index=0,
        output_dir=output_dir,
    )
]

model.fit(x_train, y_train, batch_size=2, epochs=2, callbacks=callbacks)

