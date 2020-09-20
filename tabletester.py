import tabula
import pandas as pd
#df = tabula.read_pdf("Course.pdf", pages='9')
#print(df[0])
tabula.convert_into("Course.pdf", r"output1.csv", output_format="csv", pages='9')

tabula.convert_into("Course.pdf", r"output2.csv", output_format="csv", pages='10')


#df2 = tabula.read_pdf("Course.pdf", pages='10')
#df2 = pd.DataFrame(df2)
#print(df2.head)