# goC.py
# get output Christiane (goC)



from wloop import *

def get_output_Christiane():
  L = get_list_df_conf_Wr() # list of gauge config data frame for W_r(t)
  Mtr = np.zeros((Nconf, (Lx-1)**2 ))
  col_names = []
  for i in range(Nconf):
    j = 0
    for t in range(Lx-1):
      for r in range(Lx-1):
        Mtr[i][j] = L[i]["r={r}".format(r=r+1)][t]
        if i==0:
          col_names.append("t={t},r={r}".format(r=r+1, t=t+1))
        j += 1
      ##
    ##
  ##
  df = pd.DataFrame(Mtr, columns = col_names)
  return df
##

goC = get_output_Christiane()
goC.to_csv("./goC.dat")
