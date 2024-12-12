
class LVA_category:
    def __init__(self, name, ects, lvas):
        self.name = name
        self.ects = float(ects.replace(",","."))
        self.lvas = lvas
        self.done_ects = 0.0

    def __str__(self):
        txt = f"{self.name} - Total: {self.ects} ECTS - Finished: {self.done_ects} ECTS - Missing: {self.ects - self.done_ects}\n"
        for lva in self.lvas:
            if type(lva) == LVA_category:
                txt += "\n".join([f"\t{line}" for line in str(lva).split("\n")])
            else:
                txt += f"\t{lva}\n"
        return txt

    def markdown(self):
        txt = f"{'- [x]' if self.ects - self.done_ects <= 0 and self.ects !=0 else '- [ ]'} {self.name}:\tTotal: {self.ects} ECTS - Finished: {self.done_ects} ECTS - Missing: {self.ects - self.done_ects}\n"
        for lva in self.lvas:
            if type(lva) == LVA_category:
                txt += "\n".join([f"\t{line}" for line in lva.markdown().split("\n")[:-1]]) +"\n"
            else:
                txt += f"\t{'- [x]' if lva.done else '- [ ]'} {lva.markdown()}\n"
        return txt[:-1]



class LVA:
    def __init__(self, study, ects):
        date = study.split(" ", 1)
        self.study = date[1]
        self.type = date[0]
        if self.type in ['VO', 'VL']:
            self.type = "VL"
        self.ects = float(ects.replace(",","."))
        self.done = False
        self.grade = ""

    def __asText(self):
        return f"{self.type} {self.study} - {self.ects} ECTS"

    def __str__(self):
        if self.done:
            return self.__strike(self.__asText())
        return self.__asText()

    def markdown(self):
        if self.done:
            return self.__asText() + " with Grade: " + self.grade
        return self.__asText()

    def __strike(self, text):
        return ''.join([u'\u0336{}'.format(c) for c in text])+ '\u0336' + " with Grade: " + self.grade


def findStudies(filename):
    with open(fr"resources\{filename}.in", 'r', encoding='utf-8') as file:
        categories = []
        lines = file.readlines()[:-1]
        active = []
        name, ects = "", ""
        lines = [line.replace("........", ";") for line in lines]
        blocks = [i for i in range(len(lines)) if lines[i].startswith("\t")]
        subblock = False
        for line in lines:
            if line.startswith("\t;"):
                # start new sub block
                data = line.strip().split("; ")[1].split("\t")
                active.append([(data[0], data[1])])
                subblock = True
            elif line.startswith("\t"):
                # start new block
                subblock = False
                if active:
                    lva = LVA_category(name, ects, [])
                    for ac in active:
                        if type(ac) == list:
                            lva.lvas.append(LVA_category(ac[0][0], ac[0][1], ac[1:]))
                        else:
                            lva.lvas.append(ac)
                    categories.append(lva)
                    active = []
                data = line.strip().split("\t")
                name, ects = data[0], data[1]
            elif subblock and line.startswith("; "):
                # end sub block
                subblock = False
                data = line.split(" ",1)[1].strip().split("\t")
                lva = LVA(data[0], data[1])
                active.append(lva)
            else:
                data = line.split(" ",1)[1].strip().split("\t")
                lva = LVA(data[0], data[1])
                if subblock:
                    active[-1].append(lva)
                else:
                    active.append(lva)
    if active:
        lva = LVA_category(name, ects, [])
        for ac in active:
            if type(ac) == list:
                lva.lvas.append(LVA_category(ac[0][0], ac[0][1], ac[1:]))
            else:
                lva.lvas.append(ac)
        categories.append(lva)
    return categories


if __name__ == '__main__':
    # handbuch = findStudies("ai_handbuch")
    # for category in handbuch:
    #     print(category)
    handbuch = findStudies("inf_handbuch")
    for category in handbuch:
        print(category)
