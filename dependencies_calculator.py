import re

def prepro(dependencias):
    depend_list = []
    for depend in dependencias:
        left, right = depend.split(':')
        left_ = left.split(',')
        right_ = right.split(',')
        depend_list.append([left_,right_])
    return depend_list

def subset(A,B):
    return set(A).issubset(set(B))

dependencias = ['A:B', 'A:C', 'C,G:H', 'C,G:I', 'B:H']
attribute=['A', 'G']


def closure_attr(attribute,dependencias):
    dependencias_ = prepro(dependencias)
    result = attribute.copy()

    while True:
        result_ = result.copy()
        for depend in dependencias_:
            # print(depend)
            beta, gamma = depend[0], depend[1]
            # print(beta,'->',gamma)
            # print(subset(beta,result))
            if subset(beta,result):
                for gamma_i in gamma:
                    if gamma_i not in result:
                        result.append(gamma_i) 
        # print(result)
        # print(result_)
        if result_==result:
            break
    return result

print(closure_attr(attribute,dependencias))

# print(subset([1,3,1,4],[1,3,5,4,5,6,1]))
