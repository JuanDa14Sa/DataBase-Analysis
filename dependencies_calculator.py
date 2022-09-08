import re
##Based on slides: https://faculty.ksu.edu.sa/sites/default/files/D-%20Computing%20Canonical%20Cover.pdf

def print_arrow_form(dependencias):
    for depend in dependencias:
        print(depend[0],' -> ',depend[1])

def prepro(dependencias):
    depend_list = []
    for depend in dependencias:
        left, right = depend.split('->')
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

def right_side_decomposition(dependencias):
    new_dependencias = dependencias.copy()
    for depend in new_dependencias:
        left, right = depend[0],depend[1]
        # found = False
        if len(right)!=1:
            for b in right:
                # print(b)
                new_dependencias.append([left,[b]]) 
                # found = True
                if b==right[-1]:
                    new_dependencias.remove(depend)
                    # found = False

    return new_dependencias




def canonical_cover(depedencias):
    cover = prepro(depedencias)
    cover = right_side_decomposition(cover)
    for depend in cover:   #Eliminamos atributos extraños a izquierda. 
        left, right = depend[0], depend[1]
        for a in left:
            left_tmp = left.copy()
            left_tmp.remove(a)
            # print(left_tmp)
            # print(left)
            # print(cover)
            # print('Closure of',left_tmp,':   ',closure_attr(left_tmp,cover,preprocess=False))
            if left_tmp is not None and is_subset(right, closure_attr(left_tmp,cover,preprocess=False)):
                cover.remove([left,right])
                cover.append([left_tmp,right])
                break
    # print('Cover after left reduction: ')
    # print_arrow_form(cover)

    for depend in cover: #Eliminamos atributos extraños a derecha
        left, right = depend[0], depend[1]
        for b in right:
            right_tmp = right.copy()
            right_tmp.remove(b)
            cover_tmp = cover.copy()
            # print('Right_tmp:',right_tmp)
            # print('Right:',right)
            # print(b)
            # print(left,right)
            # print_arrow_form(cover_tmp)
            cover_tmp.remove([left,right])
            cover_tmp.insert(0,[left,right_tmp])
            # print('After remove:')
            # print_arrow_form(cover_tmp)
            # print('Closure of',left,':   ',closure_attr(left,cover_tmp,preprocess=False))
            if b in closure_attr(left, cover_tmp,preprocess=False):
                cover = cover_tmp
    # print(cover)

    # print(len(cover))
    cover_ = cover.copy()
    for depend in cover:
        # print(depend)
        right = depend[1]
        # print(right==[])
        if right==[] or right is None:
            cover_.pop(0)
    cover = cover_    
    return cover





# dependencias = ['A->B,C', 'B->C', 'A->B', 'A,B->C']
# dependencias = [ 'B->C','A->B','A->B,C']
dependencias = ['A,C->G', 'D->E,G', 'B,C->D', 'C,G->B,D','A,C,D->B','C,E->A,G']
# attribute = ['A', 'G']
# attribute = ['B','D']


# print_arrow_form(right_side_union(prepro(dependencias)))

print_arrow_form(canonical_cover(dependencias))
# print(closure_attr(attribute,dependencias))
# print(tmp[0][1]==[])
