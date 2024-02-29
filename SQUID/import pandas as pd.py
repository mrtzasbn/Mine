import pandas as pd
import matplotlib.pyplot as plt



df_no_w = pd.read_csv(r"D:\MyData\Codes\Mine\Ac_No_Waiting.csv")
df_no_w.set_index('Field', inplace=True)
df_no_w = df_no_w.transpose()

df_w = pd.read_csv(r"D:\MyData\Codes\Mine\Ac_Waiting.csv")
df_w.set_index('Field', inplace=True)
df_w = df_w.transpose()


# Plot
plt.figure(figsize=(10, 6))
plt.plot(df_no_w.index, df_no_w[500], marker='o', label='500_Waiting')

plt.plot(df_w.index, df_w[500], marker='s', label='500_No_Waiting')

plt.plot(df_no_w.index, df_no_w[1000], marker='o', label='1000_Waiting')

plt.plot(df_w.index, df_w[1000], marker='s', label='1000_No_Waiting')






plt.xlabel('Try')
plt.ylabel('Difference')
# plt.title('Transposed DataFrame Plot')
plt.legend()
plt.grid(True)

plt.savefig("acdiffrenece" + 'com_w.pdf', format='pdf', bbox_inches='tight')
plt.savefig("acdiffrenece" + 'com_w.png', format='png', bbox_inches='tight')
plt.show()
