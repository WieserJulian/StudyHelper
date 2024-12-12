from SplitHandbuch import findStudies, LVA_category
from SplitStudys import getGrades


def compare(filename, skz):
    lva_categories = findStudies(filename)
    done = getGrades(skz)
    done_name = [grade.study for grade in done]
    un_done_categories= []
    for categorie in lva_categories:
        cat = LVA_category(categorie.name, str(categorie.ects), [])
        done_ects = 0.0
        for lva in categorie.lvas:
            if type(lva) == LVA_category:
                sub_cat = LVA_category(lva.name, str(lva.ects), [])
                sub_done_ects = 0.0
                for sub_lva in lva.lvas:
                    if sub_lva.study not in done_name:
                        sub_cat.lvas.append(sub_lva)
                    else:
                        sub_done_ects += float(sub_lva.ects)
                sub_cat.done_ects = sub_done_ects
                done_ects += sub_done_ects
                if sub_done_ects >= float(lva.ects) > 0:
                    sub_cat.lvas = []
                cat.lvas.append(sub_cat)
            else:
                if lva.study not in done_name:
                    cat.lvas.append(lva)
                else:
                    done_ects += float(lva.ects)
                    if done_ects == float(categorie.ects) and float(categorie.ects) > 0:
                        break
        cat.done_ects = done_ects
        un_done_categories.append(cat)
    return un_done_categories

def show_all_compared(filename, skz):
    lva_categories = findStudies(filename)
    done = getGrades(skz)
    done_name = [grade.study for grade in done]
    for categorie in lva_categories:
        for lva in categorie.lvas:
            if type(lva) == LVA_category:
                for sub_lva in lva.lvas:
                    if sub_lva.study in done_name:
                        sub_lva.done = True
                        sub_lva.grade = [grade.grade for grade in done if grade.study == sub_lva.study and grade.type == sub_lva.type][0]
                        lva.done_ects += float(sub_lva.ects)
                categorie.done_ects += lva.done_ects
            else:
                if lva.study in done_name:
                    lva.done = True
                    if not [grade.grade for grade in done if grade.study == lva.study and grade.type == lva.type]:
                        pass
                    lva.grade = [grade.grade for grade in done if grade.study == lva.study and grade.type == lva.type][0]
                    categorie.done_ects += float(lva.ects)
    return lva_categories




if __name__ == '__main__':
    # not_done = compare("ai_handbuch", "536")
    # for lva in not_done:
    #     print(lva)

    # not_done = compare("inf_handbuch", "521")
    # for lva in not_done:
    #     print(lva)


    not_done = show_all_compared("ai_handbuch", "536")
    for lva in not_done:
        print(lva.markdown())


    # not_done = show_all_compared("inf_handbuch", "521")
    # for lva in not_done:
    #     print(lva.markdown())