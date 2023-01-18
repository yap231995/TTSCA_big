import h5py
import os
from src.utils import AES_sbox
import numpy as np
from matplotlib import pyplot as plt

os.chdir("..")
ascad_database_file = "ASCAD/ASCAD.h5"

f = h5py.File(ascad_database_file, "r")
# meta_attack = f['Profiling_traces/metadata'][()]
meta_attack = f['Attack_traces/metadata'][()]
# print(meta_attack)
real_key = meta_attack['key'][0, 2] #0 because all have the same key , 2 is the 3rd byte of the plaintext.
pt_profiling = meta_attack['plaintext'][:,2] #All the 3rd byte plaintext
mask_values_overall = meta_attack['masks']#All the 3rd byte r_out
#[r3,...r14,r_in,r_out]
r_in = mask_values_overall[:,14] #14 - r_in
r_out = mask_values_overall[:,15] #15 - r_out
r_3 = mask_values_overall[:,0] #0 - r_3
# mask_values = pt_profiling^ real_key^r_in
mask_values = r_in

# r_in = mask_values_overall[:,1]

print(mask_values)
print(mask_values.shape)
# labels = f['Profiling_traces/labels'][()]
labels = f['Attack_traces/labels'][()]
print(labels.shape)
print(labels)

def HW(x):
    return bin(int(x)).count("1")
fig, ax = plt.subplots(figsize=(15, 7))
for index, mask_values in enumerate([r_out]): #r_out, r_3
# for i in range(11,16):
#     mask_name = "r_{"+str(i) +"}"
#     if i == 14:
#         mask_name = "r_{in}"
#     if i == 15:
#         mask_name = "r_{out}"
#     mask_values = pt_profiling ^ real_key ^ mask_values_overall[:,i]
    if index == 0:
        mask_name = "r_{out}"
    elif index == 1:
        mask_name = "r"
    # HW_leakage_model = np.fromiter(map(lambda pt, r_out: HW(AES_sbox[pt ^ real_key] ^ r_out), pt_profiling, mask_values), int)
    HW_leakage_model = np.zeros(pt_profiling.shape[0], dtype=int)
    HW_R_outs = np.zeros(pt_profiling.shape[0], dtype=int)
    for i in range(pt_profiling.shape[0]):
        pt  =pt_profiling[i]
        r_out = mask_values[i]
        HW_leakage_model[i] = HW(labels[i] ^r_out)
        # HW_leakage_model[i] = labels[i] ^r_out
        # print(pt,r_out,HW_leakage_model[i])
        HW_R_outs[i] = HW(mask_values[i])
        # HW_R_outs[i] = mask_values[i]
    # X_profiling = f['Profiling_traces/traces'][()]
    X_profiling = f['Attack_traces/traces'][()]
    print(X_profiling.shape)

    Corr_Rout = np.zeros(X_profiling.shape[1])
    c = np.zeros(X_profiling.shape[1])

    for t in range(X_profiling.shape[1]):
        Corr_Rout[t] = abs(np.corrcoef(HW_R_outs, X_profiling[:,t])[1,0])
        c[t] = abs(np.corrcoef(HW_leakage_model, X_profiling[:,t])[1,0])

    plt.ylim(0, 1)
    plt.plot(c, label ="$SBox(pt \oplus k^*) \oplus "+mask_name+"$")
    print("c")
    print(c)
    plt.plot(Corr_Rout, label="$" + mask_name + "$")
    print("Corr_Rout")
    print(Corr_Rout)

fig.subplots_adjust(bottom=0.2)
# plt.title("Max Absolute Correlation")
plt.xlabel("")
plt.ylabel("")
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
ax2.set_xticks(np.array([250/700,525/700,625/700]))
ax2.set_xticklabels(np.array(["$x_2$", "$x_5$","$x_6$"]))
ax2.set_xlabel("Literals", fontsize=20)
#fig, ax = plt.subplots(figsize=(15, 7))
# plt.legend()
for label in (ax.get_xticklabels() + ax.get_yticklabels() + ax2.get_xticklabels()):
    label.set_fontsize(20)

ax.legend(bbox_to_anchor=(1, 1), loc=1, borderaxespad=0, prop={'size': 25})
#plt.title("Max absolute correlation with R_out")
# ax.set_xlabel("Sample Point")
# plt.ylabel("(Absolute) Correlation")
plt.savefig('./ASCAD/CPA_attack_traces_exact_value(HW).png')
plt.show()
# maxValue = np.max(c)
# arg_maxValue = np.argmax(c)
# print("maxValue: %f  arg_maxValue: %d"% (maxValue,arg_maxValue))
# maxValue_rout = np.max(Corr_Rout)
# arg_maxValue_rout = np.argmax(Corr_Rout)
# print("maxValue_rout: %f  arg_maxValue_rout: %d" % (maxValue_rout,arg_maxValue_rout))




