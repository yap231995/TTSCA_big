import h5py
import os

from tqdm import tqdm

from src.CPA_class import CPA
from src.utils import AES_sbox, load_aes_hd,AES_sbox_inv
import numpy as np
from matplotlib import pyplot as plt

os.chdir("..")



fig, ax = plt.subplots(figsize=(15, 7))
database_file = "./AES_HD/AES_HD_ext_modified_dataset/"
# X_profiling, Y_profiling, X_attack, targets, real_key = load_aes_hd(database_file)
X_attack = np.load(database_file + 'attack_traces_AES_HD_ext_modified.npy').astype('uint8')[:50000,:]
ct_attack = np.load(database_file + 'attack_ciphertext_AES_HD_ext_modified.npy').astype('uint8')[:50000]
print("Creating all target labels for the attack traces:")
targets = np.zeros((X_attack.shape[0], 256), dtype='uint8')
for i in tqdm(range(X_attack.shape[0])):
    for k in range(256):
        targets[i, k] = AES_sbox_inv[k ^ ct_attack[i, 15]] ^ ct_attack[i, 11]
real_key = 0xa6
real_key_target = targets[:, real_key]
CPA_class = CPA(None)
X = X_attack
# Y = np.array(real_key_target)


flag = False
# for k in tqdm(range(256)):
k = real_key
print("real_key:",real_key)

for k in range(256):
    print(k)
    Y = np.array(targets[:, k])
    Y = CPA_class.HW_masked_values(Y)
    c = CPA_class.CPA_method(X, Y)
    if k == real_key:
        c_key =c
        # plt.plot(c, "blue", label="$k_{15}$")
    else:
        if flag == False:
            plt.plot(c, "grey", label = "other keys")
            flag = True
        else:
            plt.plot(c, "grey")
    print("c in CPA:")
    print(c)
plt.plot(c_key, "blue", label="$k_{15}$")
fig.subplots_adjust(bottom=0.2)
plt.ylim(0, 1)
plt.xlim([0,1250])
plt.xticks(np.arange(0, 1250, 100))
# plt.title("Max absolute correlation for hardware traces")
ax.set_xlabel('Sample Points', fontsize=20)
ax.set_ylabel('(Absolute) Correlation', fontsize=20)


ax2 = ax.twiny()
ax2.xaxis.set_ticks_position("bottom")
ax2.xaxis.set_label_position("bottom")
ax2.spines["bottom"].set_position(("axes", -0.15))
ax2.set_frame_on(True)
ax2.patch.set_visible(False)

# for sp in ax2.spines.values():
#     sp.set_visible(False)
ax2.spines["bottom"].set_visible(True)
ax2.set_xticks(np.array([750/1250,1050/1250,1150/1250]))
ax2.set_xticklabels(np.array(["$x_7$", "$x_{10}$","$x_{11}$"]))
ax2.set_xlabel("Literals", fontsize=20)
#fig, ax = plt.subplots(figsize=(15, 7))
# plt.legend()
for label in (ax.get_xticklabels() + ax.get_yticklabels() + ax2.get_xticklabels()):
    label.set_fontsize(20)

ax.legend(bbox_to_anchor=(1, 1), loc=1, borderaxespad=0, prop={'size': 25})
image_path = os.path.join("./AES_HD/", '../../InterpretableNN_SATEqn_SCA/AES_HD/AES_HD_ext_modified_dataset/CPA_attack_traces_AES_HD_other_key.png')
plt.savefig(image_path)
plt.show()


