def kayit_donusturucu(kayit_girisi):
  kayit = kayit_girisi
  i = 0
  a = 1
  bosluk_listesi = []
  aranan_listesi = []
  for a in range(len(kayit)):
    if kayit.find(" ",i,len(kayit)) != -1 :
      bosluk_listesi.append(kayit.find(" ",i,len(kayit)))
      i = kayit.find(" ",i,len(kayit)) + 1
      a = a + 1
    else:
      if len(bosluk_listesi) == 0:
        bosluk_listesi.append(-1)
      else:   
        break

  for k in range(len(bosluk_listesi) + 1):
    if bosluk_listesi[0] == -1:
      aranan_listesi.append(kayit)
      break
    elif k == 0:
      aranan_listesi.append(kayit[0:bosluk_listesi[k]])
    elif k != len(bosluk_listesi):
      aranan_listesi.append(kayit[bosluk_listesi[k-1] + 1:bosluk_listesi[k]])
    else:  
      aranan_listesi.append(kayit[bosluk_listesi[k-1] + 1:])

  return aranan_listesi
