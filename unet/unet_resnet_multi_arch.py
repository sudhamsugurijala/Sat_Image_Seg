from unet.unet_helper import *

###################### UNET WITH RESNET ENCODER #######################################

resnet = tf.keras.applications.ResNet101(
        include_top=False,
        weights='imagenet',
        input_shape=(256, 256, 3),
        pooling=max
    )
# FREEZE layers
resnet.trainable = False

def uNetResnet(img_height=IMG_HEIGHT, img_width=IMG_WIDTH, nclasses=NUM_CLASSES, filters=64):
    input_layer = resnet.input
    
    # Contraction path
    conv1 = resnet.get_layer('conv1_relu').output # 64 filters
    conv2 = resnet.get_layer('conv2_block3_out').output # 256
    conv3 = resnet.get_layer('conv3_block4_out').output # 512
    conv4 = resnet.get_layer('conv4_block23_out').output # 1024
    conv5 = resnet.get_layer('conv5_block3_out').output # 2048
    conv5 = Dropout(0.5)(conv5)
    
    # Expansion Path
    deconv4 = deconv_block(conv5, residual=conv4, nfilters=filters*16)
    deconv4 = Dropout(0.3)(deconv4)
    deconv3 = deconv_block(deconv4, residual=conv3, nfilters=filters*8)
    deconv3 = Dropout(0.5)(deconv3)
    deconv2 = deconv_block(deconv3, residual=conv2, nfilters=filters*4)
    deconv1 = deconv_block(deconv2, residual=conv1, nfilters=filters)
    
    # Output
    output_layer = Conv2DTranspose(filters//2, kernel_size=(3, 3), strides=(2, 2), padding='same')(deconv1)
    output_layer = conv_block(output_layer, nfilters=filters//4)
    output_layer = Conv2D(filters=NUM_CLASSES, kernel_size=(1, 1))(output_layer)
    output_layer = BatchNormalization()(output_layer)
    output_layer = Activation('softmax')(output_layer)
    
    model = Model(inputs=input_layer, outputs=output_layer, name='Unet')
    return model

