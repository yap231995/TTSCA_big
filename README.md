# TTSCA_big

For full reference, refer to our paper:
[Peek into the Black-Box: Interpretable Neural Network using SAT equations in Side-Channel Analysis]()



This provides the code for $TTSCA_{big}$ and apply it on ASCADv1 and AES_HD_ext.<br>
TTDCNN_3 is the $TTSCA_{big}$ with no padding.<br>
TTDCNN_2 is the miniature $TTSCA_{big}$ with padding 25.<br> 
TTDCNN_ASCAD_rand_2 is $TTSCA_{big}$ with kernel size 75 for Conv1D_1 and average pooling of kernel size 75 and stride 150.
TTDCNN_ASCAD_rand_2 is used on ASCADv1\_r

The code uses Pytorch as it background.<br>
AES_HD folder consist of the traces we extracted from AES_HD_ext from http://aisylabdatasets.ewi.tudelft.nl/
obtained 50k profiling traces and the next 50k for attack traces which can use AES_HD/set_up_aes_hd_ext.py
to set up (download the .h5 format).

We use ASCADv1\_r in our code is ASCAD_variable which can be obtained from
https://github.com/ANSSI-FR/ASCAD by obtaining 
ascad-variable.h5.
and rename to ASCAD_variable.h5.

Note: We will update the repository soon. 