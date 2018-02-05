n,m=map(int,input().split())
ar=[]
for i in range(n):
    a,b=map(int,input().split())
    ar.append(a/b*m)
print("%.6f",min(ar))
