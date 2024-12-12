class GradeClass:
    def __init__(self, date, study, grade, studyNr, type, ects, sst, skz):
        self.date = date
        self.is_acknowledged = "(anerkannt)" in study
        if self.is_acknowledged:
            study = study.replace(" (annerkannt)", "")
        self.study = study.split(" (")[0]
        self.studyID = study.split(" ")[-1]
        self.grade = grade
        self.studyNr = studyNr
        self.type = type
        if self.type in ['VO', 'VL']:
            self.type = "VL"
        self.ects = float(ects.replace(",","."))
        self.sst = sst
        self.skz = skz
    def __str__(self):
        return f"{self.type} {self.study}: ({self.studyNr}): {self.ects} ECTS with Grade: {self.grade} {"(anerkannt)" if self.is_acknowledged else ""}"


def getGrades(skz):
    with open(r"resources\grades.in", 'r', encoding='utf-8') as file:
        grades = []
        lines = file.readlines()
        for line in lines:
            line = line.strip().replace("\t",";")
            if line.endswith(skz):
                data = line.split(";")
                grades.append(GradeClass(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7]))

    return sorted(grades, key=lambda x: x.study)

if __name__ == '__main__':
    print("="*75)
    grades = getGrades("521")
    for grade in grades:
        print(grade)
    ects = sum([float(grade.ects) for grade in grades])
    print(f"Total ECTS: {ects}")
    print("="*75)
    grades = getGrades("536")
    for grade in grades:
        print(grade)
    ects = sum([float(grade.ects) for grade in grades])
    print(f"Total ECTS: {ects}")
