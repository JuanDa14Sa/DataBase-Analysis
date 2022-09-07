import re
##Based on slides: https://faculty.ksu.edu.sa/sites/default/files/D-%20Computing%20Canonical%20Cover.pdf

def print_arrow_form(dependencias):
    for depend in dependencias:
        print(depend[0],' -> ',depend[1])

def prepro(dependencias):
    depend_list = []
    for depend in dependencias:
        left, right = depend.split(':')
        left_ = left.split(',')
        right_ = right.split(',')
        depend_list.append([left_,right_])
    return depend_list

def is_subset(A,B):
    return set(A).issubset(set(B))

def closure_attr(attribute,dependencias, preprocess= True):
    if preprocess:
        dependencias_ = prepro(dependencias)
    else:
        dependencias_ = dependencias.copy()
    result = attribute.copy()

    while True:
        result_ = result.copy()
        for depend in dependencias_:
            beta, gamma = depend[0], depend[1]
            # print('beta: ',beta, '     result: ',result) 
            # print(isSubset(beta,result))
            if is_subset(beta,result):
                for gamma_i in gamma:
                    if gamma_i not in result:
                        result.append(gamma_i) 
        if result_==result:
            break
    return result

def canonical_cover(depedencias):
    cover = prepro(depedencias)
    for depend in cover:   #Eliminamos atributos extraños a izquierda. 
        left, right = depend[0], depend[1]
        for a in left:
            left_tmp = left.copy()
            if left_tmp.remove(a) is not None and is_subset(right, closure_attr(left_tmp,cover,preprocess=False)):
                cover.remove([left,right])
                cover.append([left_tmp,right])

    for depend in cover:
        left, right = depend[0], depend[1]
        for b in right:
            right_tmp = right.copy()
            right_tmp.remove(b)
            cover_tmp = cover.copy()
            cover_tmp.remove([left,right])
            cover_tmp.append([left,right_tmp])
            if b in closure_attr(left, cover_tmp,preprocess=False):
                cover = cover_tmp
    return cover




# dependencias = ['A:B', 'A:C', 'C,G:H', 'C,G:I', 'B:H']
dependencias = [ 'B:C', 'A:B', 'A:B,C']
# attribute = ['A', 'G']
attribute = ['B','D']


print(canonical_cover(dependencias))

# print(closure_attr(attribute,dependencias))