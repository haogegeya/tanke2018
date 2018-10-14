#矩形相交判断
def ju_ju(x1,y1,w1,h1,x2,y2,w2,h2):
    #矩形２在矩形１的左边
    if x2+w2<x1:
        return False
    #矩形2在矩形1的右边
    elif x2>x1+w1:
        return False
    #矩形２在矩形１的上边
    elif y2+h2<y1:
        return False
    elif y2>y1+h1:
        return False
    else:
        return True

#把所有矩形圆当成矩形点来处理
def ju_dian(x1,y1,w,h,x2,y2):
    if   x1<x2<x1+w and y1<y2<y1+h:
        return True
    else:
        return False
